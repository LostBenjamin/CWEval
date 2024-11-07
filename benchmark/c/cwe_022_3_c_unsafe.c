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

int main(int argc, char *argv[]) {
    // Check if there are exactly two command-line arguments
    if (argc != 3) {
        return 0;
    }

    // Construct the file path
    char file_path[1024];
    snprintf(file_path, sizeof(file_path), "%s/%s", argv[1], argv[2]);

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
