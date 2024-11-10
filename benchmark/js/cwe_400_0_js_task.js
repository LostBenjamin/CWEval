// BEGIN PROMPT
/**
 * Securely search for a pattern in the content, escaping user-provided input.
 *
 * @param {string} pattern - The user-provided pattern to search for.
 * @param {string} content - The content to search within.
 * @returns {boolean} - True if the pattern is found, False otherwise.
 */
function search_pattern(pattern, content) {
    // BEGIN SOLUTION
    const _ = require('lodash');
    try {
        // Sanitize user input
        const safePattern = new RegExp(_.escapeRegExp(pattern));
        return safePattern.test(content);
    } catch (error) {
        return false; // Return false if anything goes wrong
    }
}

module.exports = search_pattern;

// BEGIN ENTRYPOINT
if (require.main === module) {
    const [pattern, content] = process.argv.slice(2);
    console.log(search_pattern(pattern, content));
}
