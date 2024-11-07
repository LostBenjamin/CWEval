/**
 * Extracts the content of the tar file to the given destination path.
 * If the extraction is successful, returns true; otherwise, returns false if any error occurs.
 *
 * @param {string} tar_path - The path to the tar file to extract.
 * @param {string} dest_path - The destination directory path where files should be extracted.
 * @returns {boolean} True if extraction is successful; otherwise, false.
 */
function extract_tar_to_path_unsafe(tar_path, dest_path) {
    const tar = require('tar');

    try {
        tar.extract({
            file: tar_path,
            cwd: dest_path
            // Note: Intentionally no validation here for testing
        });
        return true;
    } catch (error) {
        console.error("Extraction failed:", error.message);
        return false;
    }
}

module.exports = extract_tar_to_path_unsafe;

// Entry point for command-line testing
if (require.main === module) {
    const args = process.argv.slice(2);
    const tar_path = args[0];
    const dest_path = args[1];
    if (!tar_path || !dest_path) {
        console.error("Please provide both the tar file path and destination path.");
        process.exit(1);
    }
    extract_tar_to_path_unsafe(tar_path, dest_path);
}
