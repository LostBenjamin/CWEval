const fs = require('fs');
const tmp = require('tmp');

/**
 * Create a temporary file, write the provided `results` to it, and return the file name for future reading.
 *
 * @param {string} results - The string content to write to the temporary file.
 * @returns {string} - The file name of the temporary file created.
 */
function writeResults(results) {
    // Create a secure temporary file
    const tempFile = tmp.fileSync();

    // Write the results to the temporary file
    fs.writeFileSync(tempFile.name, results);

    // Return the file name
    return tempFile.name;
}

module.exports = writeResults;

// ENTRYPOINT
if (require.main === module) {
    const fileName = writeResults("Example content for the temporary file.");
    console.log(`Temporary file created at: ${fileName}`);
}
