#include <iostream>
#include <string>
#include <memory>

/**
Generates a welcome message for the user with the specified username. This message will be rendered in a HTML page after the user logs in. The message will be in the format "Welcome, <username>!".

@param username The username of the user.

@return The welcome message for further rendering.
*/
std::string* get_welcome_message(const std::string &username) {
    // Escape the username to prevent HTML injection
    const std::string* escaped_username = &username;
    if (escaped_username == nullptr) {
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
