#include <iostream>
#include <sqlite3.h>
#include <string.h>

char* get_user(sqlite3* db, const std::string& username, const std::string& password) {
    sqlite3_stmt* stmt;
    char query[256];
    char* userInfo = NULL;

    // Use snprintf with std::string to format the query
    snprintf(query, sizeof(query), "SELECT userInfo FROM users WHERE username = '%s' AND password = '%s'", username.c_str(), password.c_str());

    if (sqlite3_prepare_v2(db, query, -1, &stmt, NULL) != SQLITE_OK) {
        std::cerr << "Failed to prepare statement: " << sqlite3_errmsg(db) << std::endl;
        return NULL;
    }

    // Execute the query
    if (sqlite3_step(stmt) == SQLITE_ROW) {
        const unsigned char* result = sqlite3_column_text(stmt, 0);
        userInfo = strdup(reinterpret_cast<const char*>(result));  // Copy the result to userInfo
    }

    // Clean up
    sqlite3_finalize(stmt);
    return userInfo;
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        std::cerr << "Usage: " << argv[0] << " <db_path> <username> <password>" << std::endl;
        return 1;
    }

    const std::string username = argv[2];
    const std::string password = argv[3];

    sqlite3* db;
    if (sqlite3_open(argv[1], &db) != SQLITE_OK) {
        std::cerr << "Cannot open database: " << sqlite3_errmsg(db) << std::endl;
        return 1;
    }

    char* userInfo = get_user(db, username, password);

    if (userInfo) {
        std::cout << userInfo;
        free(userInfo);
    } else {
        // std::cout << "User not found or incorrect credentials.\n";
    }

    sqlite3_close(db);
    return 0;
}
