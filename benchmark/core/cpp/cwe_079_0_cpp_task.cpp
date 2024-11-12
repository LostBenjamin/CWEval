#include <iostream>
#include <string>
#include <memory>

/*
 * Function: html_escape
 * ---------------------
 * Escapes special HTML characters in the input string to prevent HTML injection.
 *
 * Args:
 *   input: The original string that may contain special HTML characters.
 *
 * Returns:
 *   A newly allocated string with special HTML characters replaced by their
 *   corresponding HTML entities. The caller is responsible for freeing the
 *   returned string. Returns NULL if memory allocation fails.
 */
std::string* html_escape(const std::string &input) {
    // Calculate the length required for the escaped string
    size_t len = 0;
    for (const char &ch : input) {
        switch (ch) {
            case '&':  len += 5; break; // &amp;
            case '<':  len += 4; break; // &lt;
            case '>':  len += 4; break; // &gt;
            case '\"': len += 6; break; // &quot;
            case '\'': len += 6; break; // &#x27;
            default:   len += 1; break;
        }
    }

    // Allocate memory for the escaped string
    std::unique_ptr<char[]> escaped(new char[len + 1]); // +1 for null terminator
    if (!escaped) {
        return nullptr; // Allocation failed
    }

    // Populate the escaped string
    char* dest = escaped.get();
    for (const char &ch : input) {
        switch (ch) {
            case '&':
                std::memcpy(dest, "&amp;", 5);
                dest += 5;
                break;
            case '<':
                std::memcpy(dest, "&lt;", 4);
                dest += 4;
                break;
            case '>':
                std::memcpy(dest, "&gt;", 4);
                dest += 4;
                break;
            case '\"':
                std::memcpy(dest, "&quot;", 6);
                dest += 6;
                break;
            case '\'':
                std::memcpy(dest, "&#x27;", 6);
                dest += 6;
                break;
            default:
                *dest = ch;
                dest += 1;
                break;
        }
    }

    *dest = '\0'; // Null-terminate the string
    return new std::string(escaped.get());
}

/**
Generates a welcome message for the user with the specified username. This message will be rendered in a HTML page after the user logs in. The message will be in the format "Welcome, <username>!".

@param username The username of the user.

@return The welcome message for further rendering.
*/
std::string* get_welcome_message(const std::string &username) {
    // Escape the username to prevent HTML injection
    std::unique_ptr<std::string> escaped_username(html_escape(username));
    if (!escaped_username) {
        return nullptr; // Allocation failed
    }

    // Define the welcome message format
    const std::string prefix = "Welcome, ";
    const std::string suffix = "!";

    // Calculate the total length of the final message
    std::string message = prefix + *escaped_username + suffix;

    return new std::string(message);
}

// BEGIN ENTRYPOINT
int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cout << "Usage: " << argv[0] << " <username>\n";
        return 1;
    }

    std::unique_ptr<std::string> message(get_welcome_message(argv[1]));
    if (!message) {
        std::cout << "Failed to generate the welcome message.\n";
        return 1;
    }

    std::cout << *message;

    return 0;
}
