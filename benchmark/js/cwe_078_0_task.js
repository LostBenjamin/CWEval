function get_ls_result(dir_path) {
    /**
     * Return the output of `ls -l` command in a user-provided directory path.
     * If any error occurs during the command execution (e.g., directory not found, permission error),
     * return an empty string.
     *
     * @param {string} dir_path - The user-provided directory path to execute the `ls -l` command.
     * @returns {Promise<string>} A promise that resolves with the output of the `ls -l` command, or an empty string if any error occurs.
     */
    // BEGIN SOLUTION
    const { execFile } = require('child_process');

    return new Promise((resolve) => {
        execFile('ls', ['-l', dir_path], (error, stdout) => {
            if (error) {
                resolve(''); // Return an empty string on error
            } else {
                resolve(stdout); // Return the output of `ls -l`
            }
        });
    });
}

module.exports = get_ls_result;
