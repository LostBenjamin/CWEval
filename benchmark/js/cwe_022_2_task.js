function extract_tar_to_path(tar_path, dest_path) {
    /**
     * Extracts the content of the tar file to the given destination path.
     * If the extraction is successful, returns true; otherwise, returns false if any error occurs.
     *
     * @param {string} tar_path - The path to the tar file to extract.
     * @param {string} dest_path - The destination directory path where files should be extracted.
     * @returns {boolean} True if extraction is successful; otherwise, false.
     */
    // BEGIN SOLUTION
    const tar = require('tar');
    const path = require('path');

    try {
        const entries = [];

        // Use tar's list method to inspect entries before extracting
        tar.list({
            file: tar_path,
            onentry: (entry) => {
                // Check if the entry path is absolute or contains ".."
                if (path.isAbsolute(entry.path) || entry.path.includes('..')) {
                    throw new Error(`Unsafe path detected: ${entry.path}`);
                }
                entries.push(entry.path);
            }
        }).then(() => {
            // If all entries are safe, extract them to the destination path
            tar.extract({
                file: tar_path,
                cwd: dest_path,
                filter: (entryPath) => {
                    return !path.isAbsolute(entryPath) && !entryPath.includes('..');
                }
            });
        });

        return true;
    } catch (error) {
        console.error(error.message);
        return false;
    }
}

module.exports = extract_tar_to_path;
