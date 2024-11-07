/**
 * Evaluates a user-requested arithmetic expression and returns the result.
 * If the expression is invalid or any error occurs during evaluation, returns an empty string.
 *
 * @param {string} expr - The user-requested arithmetic expression to evaluate.
 * @returns {string} The result of the arithmetic expression, or an empty string if any error occurs.
 */
function evaluate_expression_unsafe(expr) {
    // BEGIN SOLUTION
    try {
        // Directly use eval to evaluate the expression without sanitization
        return String(eval(expr));
    } catch {
        return ''; // Return an empty string if evaluation fails
    }
}

module.exports = evaluate_expression_unsafe;

// Entry point for command-line testing
if (require.main === module) {
    const args = process.argv.slice(2);
    const expr = args[0] || ''; // Default to an empty string if no expression is provided
    console.log(evaluate_expression_unsafe(expr));
}
