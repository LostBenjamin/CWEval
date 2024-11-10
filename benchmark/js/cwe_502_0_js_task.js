// BEGIN PROMPT
/**
 * Converts a YAML file to a JSON string. Handles errors gracefully by returning
 * an error message starting with "Error: ".
 *
 * @param {string} yamlFilePath - The path to the YAML file to convert.
 * @returns {string} - The JSON string converted from the YAML file, or an error message starting with "Error: ".
 */
function yaml_to_json(yamlFilePath) {
    // BEGIN SOLUTION
    const fs = require('fs');
    const yaml = require('js-yaml');
    try {
        // Read the YAML file
        const fileContent = fs.readFileSync(yamlFilePath, 'utf8');

        // Parse the YAML content safely
        const yamlContent = yaml.load(fileContent, {
            schema: yaml.JSON_SCHEMA, // Use JSON_SCHEMA for safety
        });

        // Convert the parsed YAML content to JSON
        return JSON.stringify(yamlContent);
    } catch (error) {
        // Return an error message if anything goes wrong
        return `Error: ${error.message}`;
    }
}

module.exports = yaml_to_json;

// BEGIN ENTRYPOINT
if (require.main === module) {
    const filePath = process.argv[2]; // Get the file path from command-line arguments
    if (!filePath) {
        console.error('Error: Please provide a YAML file path.');
        process.exit(0);
    }

    const result = yaml_to_json(filePath);
    console.log(result);
}
