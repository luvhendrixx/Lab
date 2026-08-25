package main

import (
	"fmt"      // for printing stuff
	"io"       // for reading the response and the body
	"net/http" // making HTTP requests

	// to measure time
	"os"
)

func runPime() {
	resp, err := http.Get("https://github.com")
	if err != nil {
		fmt.Println("Error making request:", err)
		os.Exit(1)
	}

	// always close the response body when done
	defer resp.Body.Close()

	// read the response body
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("Error reading the response:", err)
		os.Exit(1)
	}

	// print the status code and body string
	fmt.Println("Status code:", resp.StatusCode)
	fmt.Println("Response Body:\n", string(body))
}
