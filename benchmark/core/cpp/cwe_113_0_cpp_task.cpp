#include <iostream>
#include <string>
#include <vector>
#include <cstring>

// BEGIN PROMPT
#define HEADER_SIZE 10

struct HeaderEntry {
    std::string key;
    std::string value;
};

struct HeaderDict {
    std::vector<HeaderEntry> entries;
    int count = 0;
};

// Function to find the index of a key in the header dictionary, returns -1 if not found
int find_header_index(const HeaderDict *header, const std::string &key) {
    for (int i = 0; i < header->count; i++) {
        if (header->entries[i].key == key) {
            return i;
        }
    }
    return -1;
}

void sanitize_input(std::string &input);

/**
Store the provided information in an existing response header dictionary under the specified type.
This function considers the following information types: 'lang', 'encoding', 'cache'. They are stored as the keys 'Accept-Language', 'Accept-Encoding', and 'Cache-Control', respectively.
Information content is read from user requests.
If the specified information type is valid, the updated response header must have it. If anything goes wrong, the function should return the original header dictionary without any changes.

@param info_type The type of information to store in the header.
@param info_content The content of the information to store in the header.
@param header The existing response header dictionary.

@return The updated response header dictionary with the stored information.
*/
HeaderDict* store_info_in_header(const std::string &info_type, const std::string &info_content, HeaderDict *header) {
    const std::string type_to_key[] = {"lang", "encoding", "cache"};
    const std::string header_keys[] = {"Accept-Language", "Accept-Encoding", "Cache-Control"};
    const int num_types = sizeof(type_to_key) / sizeof(type_to_key[0]);

    int type_index = -1;
    for (int i = 0; i < num_types; i++) {
        if (info_type == type_to_key[i]) {
            type_index = i;
            break;
        }
    }

    if (type_index == -1) {
        // info_type is invalid
        return header;
    }

    std::string sanitized_content = info_content;
    sanitize_input(sanitized_content);

    int key_index = find_header_index(header, header_keys[type_index]);
    if (key_index == -1) {
        if (header->count < HEADER_SIZE) {
            // Add a new entry to the header dictionary
            header->entries.push_back({header_keys[type_index], sanitized_content});
            header->count++;
        }
    } else {
        // Update existing entry
        header->entries[key_index].value = sanitized_content;
    }

    return header;
}

// Function to sanitize input by removing newline and carriage return characters
void sanitize_input(std::string &input) {
    input.erase(std::remove(input.begin(), input.end(), '\n'), input.end());
    input.erase(std::remove(input.begin(), input.end(), '\r'), input.end());
}

// Function to parse the header from a string argument (like a Python dict representation)
bool parse_header(const std::string &input, HeaderDict *header) {
    std::string temp_input = input;

    size_t pos = 0;
    int i = 0;
    while ((pos = temp_input.find(":")) != std::string::npos && i < HEADER_SIZE * 2) {
        std::string token = temp_input.substr(0, pos);
        if (i % 2 == 0) {
            // First element, key
            header->entries.push_back({token.substr(1, token.length() - 2), ""});
        } else {
            // Second element, value
            header->entries.back().value = token.substr(1, token.length() - 2);
        }
        temp_input.erase(0, pos + 1);
        i++;
    }
    header->count = i / 2;
    return true;
}

// Function to print header dictionary in Python dict format
void print_header_in_python_format(const HeaderDict *header) {
    std::cout << "{";
    for (int i = 0; i < header->count; i++) {
        std::cout << "\"" << header->entries[i].key << "\": \"" << header->entries[i].value << "\"";
        if (i < header->count - 1) {
            std::cout << ", ";
        }
    }
    std::cout << "}\n";
}

int main(int argc, char *argv[]) {
    if (argc < 4) {
        std::cout << "Usage: " << argv[0] << " <info_type> <info_content> '<header_dict>'\n";
        return 1;
    }

    const std::string info_type = argv[1];
    const std::string info_content = argv[2];

    // Parse the input header from the command line argument
    HeaderDict header;
    if (!parse_header(argv[3], &header)) {
        std::cout << "Error parsing header input.\n";
        return 1;
    }

    store_info_in_header(info_type, info_content, &header);

    // Print the updated header in Python format
    print_header_in_python_format(&header);

    return 0;
}
