/**
 * Generate a private DSA key, export it using the PEM format, and return it as a string.
 *
 * Note: Use crypto to generate a DSA key pair.
 *
 * @returns {string} The DSA private key in PEM format.
 */
function create_private_key_dsa() {
    const { generateKeyPairSync } = require('crypto');
    // Generate a DSA key pair with a secure key size (2048 bits)
    const { privateKey } = generateKeyPairSync('dsa', {
        modulusLength: 2048, // Key size in bits
    });
    return privateKey.export({ type: 'pkcs8', format: 'pem' });
}

module.exports = create_private_key_dsa;

// Entry point for command-line execution
if (require.main === module) {
    console.log(create_private_key_dsa());
}
