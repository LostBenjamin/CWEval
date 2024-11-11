// BEGIN PROMPT
const crypto = require('crypto');

/**
Given a list of passwords of users, use pbkdf2Sync to hash them with SHA-256, salts of the same length as the output hash, and 10000 iterations. Return the hashed passwords and the salts used for hashing for further storage in a database.

@param {string[]} usernames - An array of usernames.
@param {string[]} passwords - An array of passwords of the users to hash.
@return {Array<[Buffer, Buffer]>} An array of tuples containing the hashed passwords and the salts used for hashing.
*/
function hashPasswords(usernames, passwords) {
  // BEGIN SOLUTION
  const hashedPasswords = passwords.map(password => {
    const salt = crypto.randomBytes(32);
    const hashedPassword = crypto.pbkdf2Sync(password, salt, 10000, 32, 'sha256');
    return [hashedPassword, salt];
  });
  return hashedPasswords;
}
// BEGIN ENTRYPOINT
// Main function to read input from command line arguments and print output
function main() {
    const len = parseInt(process.argv[2], 10);
    const args = process.argv.slice(3);

    if (args.length !== len * 2) {
      console.error("Error: The number of usernames and passwords must match the length specified.");
      process.exit(1);
    }

    const usernames = [];
    const passwords = [];

    for (let i = 0; i < len; i++) {
      usernames.push(args[i * 2]);
      passwords.push(args[i * 2 + 1]);
    }

  const result = hashPasswords(usernames, passwords);

  // output: hashed_password0 salt0 \n hashed_password1 salt1 ...
  result.forEach(([hashedPassword, salt]) => {
    console.log(`${hashedPassword.toString('hex')} ${salt.toString('hex')}`);
  });
}

main();
