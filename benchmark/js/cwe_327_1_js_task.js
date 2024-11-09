// BEGIN PROMPT
/**
 * Hash the given password securely and return the hash as a string.
 *
 * @param {string} password - The password to be hashed.
 * @returns {Promise<string>} The securely hashed password.
 */
async function get_password_hash(password) {
    // BEGIN SOLUTION
    const argon2 = require('argon2');
    try {
        // Hash the password using Argon2 with secure default parameters
        return await argon2.hash(password);
    } catch (err) {
        console.error("Error hashing password:", err);
        throw err;
    }
}

module.exports = get_password_hash;

// BEGIN ENTRYPOINT
if (require.main === module) {
    const args = process.argv.slice(2);
    if (args.length === 0) {
        console.error("Usage: node script.js <password>");
        process.exit(1);
    }
    const password = args[0];
    get_password_hash(password)
        .then(hash => console.log(hash))
        .catch(err => console.error("Failed to hash password:", err));
}
