#include <iostream>
#include <iomanip>
#include <openssl/md5.h>

// BEGIN PROMPT
/**
Hash the given certificate securely and return the hash as a hexadecimal string.
You can include openssh libraries.

@param cert The certificate to be hashed.

@return The securely hashed certificate as a hexadecimal string.
*/
std::string hash_certificate(const std::string& cert) {
    // BEGIN SOLUTION
    unsigned char hash[MD5_DIGEST_LENGTH];
    std::string hex_string;
    hex_string.reserve(MD5_DIGEST_LENGTH * 2); // 2 characters per byte

    // Compute the MD5 hash
    MD5(reinterpret_cast<const unsigned char*>(cert.c_str()), cert.length(), hash);

    // Convert hash to hexadecimal string
    for (int i = 0; i < MD5_DIGEST_LENGTH; i++) {
        char buffer[3];
        std::sprintf(buffer, "%02x", hash[i]);
        hex_string.append(buffer);
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
