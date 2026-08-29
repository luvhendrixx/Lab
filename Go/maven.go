package main

import (
	"encoding/json"
	"fmt"
	"net/http" // provides tools for building web servers
	"strconv"  // helps convert strings to numbers
	"sync"     // used for safe concurrent access to shared data
)

// to store users in mem
type User struct {
	Name string `json:"name"`
}

// every...struct tag(.e.g Name is a struct tag cuz its inside the struct) is assigned an int
var userCache = make(map[int]User)
var cacheMutex sync.RWMutex // cacheMutex ensures safe read/write access to userCache since multiple req could come in at once
// starts at 0
var lastID int

func main() {
	mux := http.NewServeMux() // creating the router (only job is to handle requests to their appropriate "rooms")
	fmt.Println("Server is running on port 8080")

	// a simple handler to test if the server is running
	// r *http.Request is info sent from the browser(client) to me(the server) (URL params, headers, JSON body sent by the USER)
	// w.http.ResponseWriter is OUTGOING DATA..the tool you use to write headers, status codes and text back to the browser(USER)
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		// byte thingy means take the world "hello world" and convett it to raw bytes (the internet speaks in raw bytes so...we gotta convert)
		w.Write([]byte("hello world\n"))
	})

	mux.HandleFunc("POST /users", func(w http.ResponseWriter, r *http.Request) {
		var user User
		// the below line takes incoming JSON txt from the user's browser and translates it directly to the User struct we created
		// json.NewDecoder reads and "translates" incoming data on the fly instead of waiting for everything to arrive then start reading and "translating"
		// .Decode((&user)) tells the Deocder to "read the JSON from the network stream and parse("translate") its fields into the Go struct we created"
		err := json.NewDecoder(r.Body).Decode((&user))
		// if the error isn't valid JSON.e.g broken syntax, return a 400 (bad request) error to the client (USER)
		if err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}
		// if the user didn't provide a name..bad request...return it to the USER
		if user.Name == "" {
			http.Error(w, "Name is required", http.StatusBadRequest)
			return
		}

		// safe MuTEX write
		// allows for A SINGLE WRITER and 0 READERS
		cacheMutex.Lock()
		defer cacheMutex.Unlock()
		lastID++ // ID strictly goes 1, 2, 3... and never resets
		userCache[lastID] = user

		w.WriteHeader(http.StatusCreated)
		w.Write([]byte("User created successfully\n"))
	})

	mux.HandleFunc("GET /users/{id}", func(w http.ResponseWriter, r *http.Request) {
		// Atoi ('ASCII' to interger) converts the id we got from the user to an int (remeber, we mapped struct tags to ints..but users sends strings, so go won't allow it and that's why we have to convert)
		// this also checks for...weird requests.e.g /users/abc where abc can't be converted to a int which ought to trigger the 400 Bad Request
		id, err := strconv.Atoi(r.PathValue("id"))
		if err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}
		// RLock() [read lock] allows for MANY READERS but 0 WRITERS
		cacheMutex.RLock()
		defer cacheMutex.RUnlock() // a "sticky" note to auto update the "chalkboard" for readers inside when coming in and going out
		// userCache[id] gives use back a key(.e.g Name from the struct) and a boolean(True or False)
		user, ok := userCache[id]
		if !ok {
			// fixed this bug where there was StatusFound instead of StatusNotFound (404)
			http.Error(w, "User not found\n", http.StatusNotFound)
			return // immediately exit here
		}
		// we're telling the client(user's browser) that we're returning data in form of JSON, not HTML or plain text or XML
		// so the browser can auto-parse and display the JSON structure on the clients side on their browser
		w.Header().Set("Content-Type", "application/json")
		// j is now a byte slice: []byte(`{"name":"Alice"}`)
		// marshal takes a Go data structure like struct, map or slice and converts it into a byte slice []byte formatted a JSON txt
		// .e.g User struct has {Name: "Alice"} json.Marshal turns it into -> `{"name":"Alice"}`
		j, err := json.Marshal(user)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		w.WriteHeader(http.StatusOK)
		// for clean output without the % thingy
		w.Write(append(j, '\n'))

		/*
			To save some keystrokes, you could actually write...
			w.Header().Set("Content-Type", "application/json")
			w.WriteHeader(http.StatusOk)
			json.NewEncoder(w).Encode(user) <- this convers user directly to JSON and write its to 'w'
		*/
	})

	mux.HandleFunc("DELETE /users/{id}", func(w http.ResponseWriter, r *http.Request) {
		id, err := strconv.Atoi(r.PathValue("id"))
		if err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}
		// the _ means this is a throw away value
		if _, ok := userCache[id]; !ok {
			http.Error(w, "User not found\n", http.StatusNotFound)
			return
		}
		cacheMutex.Lock()
		defer cacheMutex.Unlock()
		delete(userCache, id)
		w.WriteHeader(http.StatusOK)
		// 204 (http.StatusNoContent) means the server is sending 0 bytes...so it was odd and i changed it to http.StatusOk (200)
		w.Write([]byte("User Deleted Successfully\n"))
	})
	http.ListenAndServe(":8080", mux)
}
