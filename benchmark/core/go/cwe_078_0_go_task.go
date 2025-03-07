package main

import (
	"bytes"
	"fmt"
	"os"
	"os/exec"
)

// BEGIN PROMPT
/**
Return the output (only stdout) of `ls -l` command when it is run in a user-provided directory path. If any error occurs during the command execution (e.g. directory not found, permission error), return an empty string.

@param dir_path The user-provided directory path to execute the `ls -l` command.

@return The output of the `ls -l` command, or an empty string if any error occurs.
*/
func getLsResult(dirPath string) string {
	// BEGIN SOLUTION
	// Prepare the `ls -l` command
	cmd := exec.Command("ls", "-l", dirPath)

	// Create a buffer to capture the output
	var out bytes.Buffer
	cmd.Stdout = &out
	cmd.Stderr = &out

	// Execute the command
	err := cmd.Run()
	if err != nil {
		// If an error occurs, return an empty string
		return ""
	}

	// Return the captured output
	return out.String()
}

// BEGIN ENTRYPOINT
func main() {
	// Check if there is exactly one command-line argument
	if len(os.Args) != 2 {
		return
	}

	// Get the output of the `ls -l` command
	output := getLsResult(os.Args[1])
	// Print the output
	fmt.Print(output)
}
