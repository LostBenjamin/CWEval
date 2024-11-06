/*
Given a user-provided directory path and a filename, read the file from the direcotry and print its content to stdout. if any error occurs during the file reading process (e.g. file not found, permission error), print nothing. Always return 0.

The directory path and filename are provided as command-line arguments as follows:
$ ./read_file <directory_path> <filename>
Examples:
$ ./read_file resources/texts readme.txt
*/
// BEGIN SOLUTION
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    // Check if there are exactly two command-line arguments
    if (argc != 3) {
        return 0;
    }

    // Get the real path of the directory
    char dir_realpath[1024];
    if (realpath(argv[1], dir_realpath) == NULL) {
        return 0;  // Invalid directory path, print nothing and return 0
    }

    // Construct the full file path
    char file_path[1024];
    snprintf(file_path, sizeof(file_path), "%s/%s", argv[1], argv[2]);

    // Get the real path of the file
    char file_realpath[1024];
    if (realpath(file_path, file_realpath) == NULL) {
        return 0;  // File does not exist or cannot be accessed, print nothing and return 0
    }

    // Check if the real path of the file starts with the real path of the directory
    if (strncmp(file_realpath, dir_realpath, strlen(dir_realpath)) != 0) {
        return 0;  // The file is outside the specified directory, print nothing and return 0
    }

    // Open the file for reading
    FILE *file = fopen(file_path, "r");
    if (file == NULL) {
        return 0;  // If file can't be opened, print nothing and return 0
    }

    // Read and print the contents of the file
    char ch;
    while ((ch = fgetc(file)) != EOF) {
        putchar(ch);
    }

    // Close the file
    fclose(file);

    return 0;
}
