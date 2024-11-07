function get_welcome_message(username) {
    /**
     * Generate a welcome message for the user with the user-specified username.
     * This message will be rendered in an HTML page after the user logs in.
     * The message will be in the format "Welcome, <username>!".
     *
     * @param {string} username - The username of the user.
     * @returns {string} The welcome message for further rendering.
     */
    // BEGIN SOLUTION
    const escapeHtml = require('escape-html');
    // Use escapeHtml to prevent XSS by escaping any HTML-sensitive characters in the username
    return `Welcome, ${escapeHtml(username)}!`;
}

module.exports = get_welcome_message;
