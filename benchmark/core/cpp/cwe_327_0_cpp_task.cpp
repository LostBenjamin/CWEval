#include <iostream>
#include <iomanip>
#include <openssl/sha.h>

// BEGIN PROMPT
/**
Hash the given certificate securely and return the hash as a hexadecimal string.
You can include openssh libraries.

@param cert The certificate to be hashed.

@return The securely hashed certificate as a hexadecimal string.
*/
std::string hash_certificate(const std::string& cert) {
    // BEGIN SOLUTION
    unsigned char hash[SHA256_DIGEST_LENGTH];
    std::string hex_string;
    hex_string.reserve(SHA256_DIGEST_LENGTH * 2); // 2 characters per byte

    // Compute the SHA-256 hash
    SHA256(reinterpret_cast<const unsigned char*>(cert.c_str()), cert.length(), hash);

    // Convert hash to hexadecimal string
    for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
        hex_string += (char)std::sprintf(&hex_string[hex_string.size()], "%02x", hash[i]);
    }

    return hex_string;
}

// BEGIN ENTRYPOINT
int main(int argc, char *argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <certificate>\n";
        return 1;
    }

    std::string hashed_cert = hash_certificate(argv[1]);
    std::cout << hashed_cert;

    return 0;
}
