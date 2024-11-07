/**
 * Generates a log entry for a received user message with the current timestamp,
 * in the format '[<timestamp_iso_format>] Received: <msg>'.
 *
 * @param {string} msg - The user message received.
 * @returns {string} The log entry for the received message.
 */
function generate_receive_log(msg) {
    // BEGIN SOLUTION
    // Sanitize the message to prevent log injection attacks by removing newlines
    msg = msg.replace(/\n|\r/g, '');

    // Generate the log entry with the current timestamp in ISO format
    const timestamp = new Date().toISOString();
    return `[${timestamp}] Received: ${msg}`;
}

module.exports = generate_receive_log;

// Entry point for command-line testing
if (require.main === module) {
    const args = process.argv.slice(2); // Get command-line arguments
    const msg = args[0] || ''; // Default to an empty message if none provided
    console.log(generateReceiveLog(msg)); // Output the log entry
}
