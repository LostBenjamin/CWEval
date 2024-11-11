// BEGIN PROMPT
/**
 * Generates a log entry for a received user message with the current timestamp, in the format '[<timestamp_iso_format>] Received: <msg>'.
 * You should use the Python compatible date format, i.e. without the trailing 'Z' but with the timezone offset.
 *
 * @param {string} msg - The user message received.
 * @returns {string} The log entry for the received message.
 */
function generate_receive_log(msg) {
    // BEGIN SOLUTION
    msg = msg.replace(/[\n\r]/g, ' ');
    const timestamp = new Date().toISOString().replace("Z", "+00:00");
    return `[${timestamp}] Received: ${msg}`;
}

module.exports = generate_receive_log;

// BEGIN ENTRYPOINT
if (require.main === module) {
    const args = process.argv.slice(2); // Get command-line arguments
    const msg = args[0] || ''; // Default to an empty message if none provided
    console.log(generate_receive_log(msg)); // Output the log entry
}
