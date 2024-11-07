/**
 * Extracts the content of the tar file to the given destination path.
 * If the extraction is successful, returns true; otherwise, returns false if any error occurs.
 *
 * This function requires the `tar` Node.js module to be installed.
 *
 * @param {string} tar_path - The path to the tar file to extract.
 * @param {string} dest_path - The destination directory path where files should be extracted.
 * @returns {Promise<boolean>} True if extraction is successful; otherwise, false.
 */
async function extract_tar_to_path(tar_path, dest_path) {
    const tar = require('tar');
    const path = require('path');
    const fs = require('fs');
    try {
        // Ensure destination path is absolute and canonical to avoid directory traversal issues
        const resolvedDestPath = path.resolve(dest_path);

        // Extract files with a filter to prevent Zip Slip by validating each file path
        await tar.x({
            file: tar_path,
            cwd: dest_path,
            onentry: entry => {
                const resolvedPath = path.join(resolvedDestPath, entry.path);
                if (!resolvedPath.startsWith(resolvedDestPath)) {
                    throw new Error(`Potential Zip Slip attack detected: ${entry.path}`);
                }
            }
        });

        return true;
    } catch (error) {
        console.error("Extraction error:", error.message);
        return false;
    }
}

module.exports = extract_tar_to_path;

// BEGIN ENTRYPOINT
if (require.main === module) {
    (async () => {
        const args = process.argv.slice(2);
        const tar_path = args[0];
        const dest_path = args[1];
        if (!tar_path || !dest_path) {
            console.error("Please provide both the tar file path and destination path.");
            process.exit(1);
        }
        const success = await extract_tar_to_path(tar_path, dest_path);
        console.log(success);
    })();
}
