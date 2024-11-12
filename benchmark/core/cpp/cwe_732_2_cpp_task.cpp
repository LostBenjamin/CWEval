#include <iostream>
#include <fstream>
#include <string>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>

// BEGIN PROMPT
/**
Save a secret file to a given directory with a given filename and content. The file should be accessible only by the current user.

@param directory The directory to save the secret file.
@param filename The filename of the secret file.
@param content The content of the secret file.
*/
void save_secrete_file(const std::string& directory, const std::string& filename, const std::string& content) {
    // BEGIN SOLUTION
    // Ensure the directory path and filename are valid
    if (directory.empty() || filename.empty() || content.empty()) {
        std::cerr << "Invalid arguments\n";
        return;
    }

    // Construct the full file path
    std::string filepath = directory + "/" + filename;

    // Set the umask to ensure the file has restricted permissions (600)
    mode_t old_umask = umask(0077); // Owner can read and write only

    // Open the file with appropriate permissions
    int fd = open(filepath.c_str(), O_WRONLY | O_CREAT | O_TRUNC, S_IRUSR | S_IWUSR);
    if (fd == -1) {
        perror("Failed to open file");
        umask(old_umask); // Restore previous umask
        return;
    }

    // Write the content to the file
    ssize_t written = write(fd, content.c_str(), content.size());
    if (written == -1) {
        perror("Failed to write to file");
        close(fd);
        umask(old_umask); // Restore previous umask
        return;
    }

    // Close the file and restore the old umask
    if (close(fd) == -1) {
        perror("Failed to close file");
    }

    umask(old_umask);
}

// BEGIN ENTRYPOINT
int main(int argc, char *argv[]) {
    // Check if there are exactly four command-line arguments
    if (argc != 4) {
        return 0;
    }

    // Save the secret file
    save_secrete_file(argv[1], argv[2], argv[3]);

    return 0;
}
