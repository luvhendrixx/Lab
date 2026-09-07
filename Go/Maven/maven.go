package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	_ "github.com/mattn/go-sqlite3"
)

type User struct {
	Name string `json:"name"`
	ID   int    `json:"id"`
}

// helper func that takes the shared DB handle and name to insert to the db
func createUser(db *sql.DB, name string) (int64, error) {
	// do the insertion
	// btw, columns are always enclosed in ()
	// .e.g (name) column
	stmt, err := db.Prepare("INSERT INTO users (name) VALUES (?)")
	if err != nil {
		return 0, err
	}
	defer stmt.Close()

	res, err := stmt.Exec(name)
	if err != nil {
		return 0, err
	}

	lastID, err := res.LastInsertId()
	if err != nil {
		return 0, err
	}

	return lastID, nil
}

func main() {
	// create the router
	mux := http.NewServeMux()

	// init the DB once the programme starts
	database, err := sql.Open("sqlite3", "./maven.db")
	if err != nil {
		log.Fatalf("Failed to open DB: %v", err)
	}
	defer database.Close()

	// create the table ONCE at startup of the programme as well
	query := "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)"

	if _, err := database.Exec(query); err != nil {
		log.Fatalf("Failed to create the table: %v", err)
	}

	// create the handlers (ROOT)
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		// this looks at the web addr (url) send by the client and grabs the value..
		// of a specific param named username
		// .e.g localhost:8080/?username=Alex ...
		// it'll grab Alex and display Hey there Alex 👋
		username := r.URL.Query().Get("username")
		if username == "" {
			username = "Guest"
		}
		// fmt.sprintf creates a formatted string(plain text bts[the string]) instead of printing to stdout
		// the reason we return plain txt is cuz we typed a plain phrase...("Hey there..")...
		// without any HTML tags or JSON fmting
		greeting := fmt.Sprintf("Hey there %s 👋\n", username)

		// write the resp back to the client http stream
		// this tells the client that the server (me) is sending back plain ordinary text encoded in UTF-8
		// the "Content-Type" tells the clients browser or so how to handle the response data from the server
		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.Write([]byte(greeting))
	})

	// create the handler (POST) -> creation of users
	mux.HandleFunc("POST /users", func(w http.ResponseWriter, r *http.Request) {
		var user User

		// decodes the 1s and 0s(the body of the req) from the client into JSON...
		// then appends/adds them to the User struct
		err := json.NewDecoder(r.Body).Decode((&user))
		if err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return // exit early
		}
		// if the user didn't provide a name..= bad req so we return (tell them)..
		// input validation to see if they provided a name
		if user.Name == "" {
			http.Error(w, "Hey, you didn't provide a name :-(", http.StatusBadRequest)
			return
		}

		// insert into the DB if they did everything right
		id, err := createUser(database, user.Name)
		if err != nil {
			http.Error(w, "Failed to create your user in the DB, try again please", http.StatusInternalServerError)
			log.Printf("DB error: %v", err)
			return
		}

		// update the struct with the newly generated ID (gets added/appended to the User struct)
		user.ID = int(id)

		// send the JSON response back to the client (Marshalling -> pulling data out of the USER STRUCT, parsing it to json and streaming it back to the user)
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusCreated) // this must always be called after setting headers BUT before writing the body
		json.NewEncoder(w).Encode(user)   // targets the stream resp (w) goes to the User struct and encodes/parses it to JSON then streams it back to the client
	})

	// start the server
	fmt.Println("Server is running on port 8080")
	// turns out this is a blocking operation so..it gets added at the very last of this code...
	// so it doesn't block anything
	if err := http.ListenAndServe(":8080", mux); err != nil {
		log.Fatalf("Server failed: %v", err)
	}

}
