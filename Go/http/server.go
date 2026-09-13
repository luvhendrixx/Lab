package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	// when go receives a msg, its stored in the buffer...
	// we specifcy the buffer size...
	// Go goes to the read buffer and...reads data inside the buffer then process it using the...
	// instructions below

	// vice versa for WriteBufferSize
	ReadBufferSize:  1024, // ~1KB
	WriteBufferSize: 1024, // ~1KB
}

func helloHandler(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil) // upgrade the connection for both request and resp here
	if err != nil {
		log.Println(err)
		return // exit early
	}
	defer conn.Close() // close the conn incase the client closes/exits so as to save system resources

	for {
		messageType, payload, err := conn.ReadMessage() // READ from the ReadBufferSize
		if err != nil {
			log.Println("Client disconnected:", err)
			break // exit the loop cleanly incase of a disconn or error
		}
		println("Recieved:", string(payload)) // print what we read from the ReadBufferSize

		// 4. (optional bit...) echo the msg back to the client
		err = conn.WriteMessage(messageType, payload)
		if err != nil {
			log.Println("Write error:", err)
			break
		}
	}

}

func main() {
	http.HandleFunc("/", helloHandler)

	fmt.Println("Websocket now istening on port 8080...")
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		log.Fatal(err)
	}
}
