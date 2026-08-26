package main // tells go this programme isn't a lib but an actual exe programme

import (
	"context"
	"fmt"
	"io"
	"log"
	"os"

	"github.com/joho/godotenv"
	"google.golang.org/genai"
)

// entry point required by Go exe runner
func main() {
	err := godotenv.Load()
	if err != nil {
		log.Println("WARNING!! Error loading .env file")
	}

	if err := generareWithText(os.Stdout); err != nil {
		log.Fatalf("Execution failed: %v", err)
	}
}

// generareWithText shows how to generate text using a text prompt
func generareWithText(w io.Writer) error {
	ctx := context.Background()

	client, err := genai.NewClient(ctx, &genai.ClientConfig{
		HTTPOptions: genai.HTTPOptions{APIVersion: "v1"},
	})
	if err != nil {
		return fmt.Errorf("Failed to create a genai client: %w", err)
	}

	resp, err := client.Models.GenerateContent(ctx,
		"gemini-2.5-flash",
		genai.Text("How does AI work?"),
		nil,
	)
	if err != nil {
		return fmt.Errorf("Failed to generate content: %w", err)
	}

	respText := resp.Text()

	fmt.Fprintln(w, respText)
	// example response:
	// that's a greate question! Understanding how AI works can feel like...
	// ....
	// **1 The foundation: Data and Algorithms
	// ...
	return nil
}
