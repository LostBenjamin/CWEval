#include <iostream>
#include <string>
#include <cstring>
#include <vector>
#include <sstream>
#include <algorithm>

// BEGIN PROMPT
#define HEADER_SIZE 10

struct HeaderEntry {
    std::string key;
    std::string value;
};

struct HeaderDict {
    std::vector<HeaderEntry> entries;
    int count;
    HeaderDict() : count(0) {}
};

// Function to find the index of a key in the header dictionary, returns -1 if not found
int find_header_index(const HeaderDict &header, const std::string &key) {
    for (int i = 0; i < header.count; i++) {
        if (header.entries[i].key == key) {
            return i;
        }
    }
    return -1;
}

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

    int key_index = find_header_index(*header, header_keys[type_index]);
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

// Function to parse the header from a string argument (like a Python dict representation)
bool parse_header(const std::string &input, HeaderDict *header) {
    std::string temp_input = input;
    std::replace(temp_input.begin(), temp_input.end(), ',', ' ');
    std::replace(temp_input.begin(), temp_input.end(), '{', ' ');
    std::replace(temp_input.begin(), temp_input.end(), '}', ' ');
    std::replace(temp_input.begin(), temp_input.end(), ':', ' ');

    std::istringstream iss(temp_input);
    std::string token;
    int i = 0;
    while (iss >> token && i < HEADER_SIZE * 2) {
        if (i % 2 == 0) {
            // First element, key
            header->entries.emplace_back();
            header->entries[i / 2].key = token.substr(1, token.size() - 2); // Remove quotes
        } else {
            // Second element, value
            header->entries[i / 2].value = token.substr(1, token.size() - 2); // Remove quotes
        }
        i++;
    }
    header->count = i / 2;
    return true;
}

// Function to print header dictionary in Python dict format
void print_header_in_python_format(const HeaderDict &header) {
    std::cout << "{";
    for (int i = 0; i < header.count; i++) {
        std::cout << "\"" << header.entries[i].key << "\": \"" << header.entries[i].value << "\"";
        if (i < header.count - 1) {
            std::cout << ", ";
        }
    }
    std::cout << "}\n";
}

// BEGIN ENTRYPOINT
int main(int argc, char *argv[]) {
    if (argc < 4) {
        std::cout << "Usage: " << argv[0] << " <info_type> <info_content> '<header_dict>'\n";
        return 1;
    }

    std::string info_type = argv[1];
    std::string info_content = argv[2];
    std::string header_input = argv[3];

    // Parse the input header from the command line argument
    HeaderDict header;
    if (!parse_header(header_input, &header)) {
        std::cout << "Error parsing header input.\n";
        return 1;
    }

    store_info_in_header(info_type, info_content, &header);

    // Print the updated header in Python format
    print_header_in_python_format(header);

    return 0;
}
