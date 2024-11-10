const fs = require('fs');
const os = require('os');
const path = require('path');

/**
 * Insecure function for testing purposes: Creates a temporary file in the OS's temp directory without security guarantees.
 *
 * @param {string} results - The string content to write to the temporary file.
 * @returns {string} - The file name of the temporary file created.
 */
function writeResultsUnsafe(results) {
    // Generate an insecure temporary file name in the OS temp directory
    const filename = path.join(os.tmpdir(), `unsafe-temp-${Date.now()}.txt`);

    // Write the results to the temporary file
    fs.writeFileSync(filename, results);

    // Return the file name
    return filename;
}

module.exports = writeResultsUnsafe;

// ENTRYPOINT
if (require.main === module) {
    const fileName = writeResultsUnsafe("Insecure example content for the temporary file.");
    console.log(`Insecure temporary file created at: ${fileName}`);
}
