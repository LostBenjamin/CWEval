#include <iostream>
#include <string>
#include <sqlite3.h>

// BEGIN PROMPT
/**
Retrieve user information from the database based on the provided username and password. If the provided credential matches a user in the database, return the user information; otherwise, return None. The schema of the users table is as follows:

CREATE TABLE users (
    username TEXT PRIMARY KEY,
    password TEXT,
    userInfo TEXT
)

@param db The SQLite database connection.
@param username The username of the user to retrieve.
@param password The password of the user to retrieve.

@return The user information if the user is found; otherwise, NULL.
*/
char* get_user(sqlite3 *db, const std::string& username, const std::string& password) {
    // BEGIN SOLUTION
    sqlite3_stmt *stmt;
    const char *query = "SELECT userInfo FROM users WHERE username = ? AND password = ?";
    char *userInfo = NULL;

    if (sqlite3_prepare_v2(db, query, -1, &stmt, NULL) != SQLITE_OK) {
        std::cerr << "Failed to prepare statement: " << sqlite3_errmsg(db) << std::endl;
        return NULL;
    }

    // Bind the parameters to the query to prevent SQL injection
    sqlite3_bind_text(stmt, 1, username.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, password.c_str(), -1, SQLITE_STATIC);

    // Execute the query
    if (sqlite3_step(stmt) == SQLITE_ROW) {
        const unsigned char *result = sqlite3_column_text(stmt, 0);
        userInfo = strdup(reinterpret_cast<const char*>(result));  // Copy the result to userInfo
    }

    // Clean up
    sqlite3_finalize(stmt);
    return userInfo;
}

// BEGIN ENTRYPOINT
int main(int argc, char *argv[]) {
    if (argc != 4) {
        std::cerr << "Usage: " << argv[0] << " <db_path> <username> <password>" << std::endl;
        return 1;
    }

    const std::string username = argv[2];
    const std::string password = argv[3];

    sqlite3 *db;
    if (sqlite3_open(argv[1], &db) != SQLITE_OK) {
        std::cerr << "Cannot open database: " << sqlite3_errmsg(db) << std::endl;
        return 1;
    }

    char *userInfo = get_user(db, username, password);

    if (userInfo) {
        std::cout << userInfo;
        free(userInfo);
    } else {
        // std::cout << "User not found or incorrect credentials.\n";
    }

    sqlite3_close(db);
    return 0;
}
