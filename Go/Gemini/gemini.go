package main

import (
	"bufio"
	"context"
	"fmt"
	"io"
	"log"
	"os"
	"os/user"
	"strings"
	"time"

	"google.golang.org/genai"
)

func main() {
	// fetch current user exe-ing the programme
	currentUser, err := user.Current()
	if err != nil {
		log.Fatalf("Failed to get current user: %v", err)
	}
	// prompt user for input
	reader := bufio.NewReader(os.Stdin)
	fmt.Printf("Whatchu looking for %s ? ", currentUser.Username)

	input, err := reader.ReadString('\n') // read till you see a \n (when the user hits enter)
	if err != nil {
		fmt.Println("Hmm..something went wrong, maybe try again?", err)
		os.Exit(1)
	}
	input = strings.TrimSpace(input) // trims all whitespace

	// open file..if it don't exist, CREATE IT, open it in WRITEONLY and APPEND to it
	// 0644 is the POSIX file permission mode
	file, err := os.OpenFile("output.json", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0644)
	if err != nil {
		log.Fatalf("Failed to create file: %v", err)
	}
	defer file.Close() // free up sys resources when done creating

	// io.MultiWriter sends output to BOTH the terminal (os.Stdout) and the file simulateneously
	multWriter := io.MultiWriter(os.Stdout, file)

	// run the stream generator once
	if err := generateStream(multWriter, input); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}
	// TODO: ADD A RESPONSE CACHING SYSTEM USING THIS STARTER PACK!!
	// THAT THE PROGRAMME CAN QUERY IF IT ALREADY EXISTS IN OUTPUT.TXT
	// TODO: MAKE THE SYSTEM TO STORE DATA IN KEY-VALUE FORM .i.e USER: ... MODEL: ...
}

func generateStream(w io.Writer, prompt string) error {
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel() // release sys resources when done

	client, err := genai.NewClient(ctx, &genai.ClientConfig{
		HTTPOptions: genai.HTTPOptions{APIVersion: "v1"},
	})
	if err != nil {
		return fmt.Errorf("Failed to create client: %w", err)
	}

	iter := client.Models.GenerateContentStream(ctx,
		"gemini-2.5-flash",
		genai.Text(prompt),
		nil,
	)

	// loop over incoming bytes as they arrive from the server
	for resp, err := range iter {
		if err != nil {
			return fmt.Errorf("Error during stream: %w", err)
		}
		// print each chunk to the terminal without adding extra new lines
		fmt.Fprint(w, resp.Text())
	}
	fmt.Println() // adds a new line at the end of the response
	return nil
}
