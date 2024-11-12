#include <iostream>
#include <iomanip>
#include <string>
#include <vector>
#include <openssl/aes.h>
#include <openssl/rand.h>

// Function to pad data to AES block size
std::vector<unsigned char> pad_data(const std::vector<unsigned char>& data, size_t* padded_len) {
    size_t data_len = data.size();
    size_t padding = AES_BLOCK_SIZE - (data_len % AES_BLOCK_SIZE);
    *padded_len = data_len + padding;

    std::vector<unsigned char> padded_data(*padded_len);
    memcpy(padded_data.data(), data.data(), data_len);
    memset(padded_data.data() + data_len, (unsigned char)padding, padding);

    return padded_data;
}


// BEGIN PROMPT
#include <openssl/aes.h>
// Structure to hold the return values
struct encryption_result {
    std::vector<unsigned char> encrypted_data;
    size_t encrypted_len;
    std::vector<unsigned char> iv;
    std::vector<unsigned char> key;
};

/**
Encrypt the data with the key using AES and CBC mode.
The provided key bytes is long enough (>= 64 bytes). Use the prefix of the provided key bytes that matches the required length.
Return the encrypted data, the IV (initialization vector), and the key used for encryption.

@param key The bytes to generate the encryption key.
@param data The data to encrypt.

@return The encrypted data, the IV, and the key used for encryption.
*/
encryption_result encrypt_data(
    const std::vector<unsigned char>& key, size_t key_len,
    const std::vector<unsigned char>& data
) {
    // BEGIN SOLUTION
    encryption_result result;

    // Validate input parameters
    if (key.empty() || data.empty() || key_len < 16) {
        return result;
    }

    // Generate random IV
    result.iv.resize(AES_BLOCK_SIZE);
    if (RAND_bytes(result.iv.data(), AES_BLOCK_SIZE) != 1) {
        return result;
    }

    // Copy first 16 bytes of key
    result.key.resize(16);
    memcpy(result.key.data(), key.data(), 16);

    // Pad the input data
    size_t padded_len;
    std::vector<unsigned char> padded_data = pad_data(data, &padded_len);
    result.encrypted_len = padded_len;

    // Initialize AES encryption
    AES_KEY aes_key;
    if (AES_set_encrypt_key(result.key.data(), 128, &aes_key) != 0) {
        return result;
    }

    // Perform CBC mode encryption
    std::vector<unsigned char> iv_copy = result.iv;
    result.encrypted_data.resize(padded_len);
    AES_cbc_encrypt(padded_data.data(), result.encrypted_data.data(), padded_len,
                    &aes_key, iv_copy.data(), AES_ENCRYPT);

    return result;
}

// BEGIN ENTRYPOINT
int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <key_hex> <data_hex>" << std::endl;
        return 1;
    }

    // Convert hex strings to bytes
    size_t key_len = strlen(argv[1]) / 2;
    size_t data_len = strlen(argv[2]) / 2;
    std::vector<unsigned char> key(key_len);
    std::vector<unsigned char> data(data_len);

    if (key.empty() || data.empty()) {
        std::cerr << "Memory allocation failed" << std::endl;
        return 1;
    }

    // Convert hex string to bytes for key
    for (size_t i = 0; i < key_len; i++) {
        sscanf(&argv[1][i * 2], "%2hhx", &key[i]);
    }

    // Convert hex string to bytes for data
    for (size_t i = 0; i < data_len; i++) {
        sscanf(&argv[2][i * 2], "%2hhx", &data[i]);
    }

    // Perform encryption
    encryption_result result = encrypt_data(key, key_len, data);

    if (result.encrypted_data.empty() || result.iv.empty() || result.key.empty()) {
        std::cerr << "Encryption failed" << std::endl;
        return 1;
    }

    // Print results in hex format
    for (size_t i = 0; i < result.encrypted_len; i++) {
        std::cout << std::setw(2) << std::setfill('0') << std::hex << (int)result.encrypted_data[i];
    }
    std::cout << std::endl;

    for (size_t i = 0; i < AES_BLOCK_SIZE; i++) {
        std::cout << std::setw(2) << std::setfill('0') << std::hex << (int)result.iv[i];
    }
    std::cout << std::endl;

    for (size_t i = 0; i < 16; i++) {
        std::cout << std::setw(2) << std::setfill('0') << std::hex << (int)result.key[i];
    }
    std::cout << std::endl;

    return 0;
}
