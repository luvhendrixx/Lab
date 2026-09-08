package main

import (
	"encoding/json"
	"net/http"
)

type Response struct {
	Message string `json:"message"`
}

func main() {
	http.HandleFunc("/api/greeting", handleGreeting)
	http.ListenAndServe(":8080", nil)
}

func handleGreeting(w http.ResponseWriter, r *http.Request) {
	// this says that web browsers that any website is allowed to req and read data from the Go API i built
	// the * is the one that...lets it be public facing
	// in prod, replace the * with the specific domain u want to bind to..
	// so only my website can access that API
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Content-Type", "application/json")

	resp := Response{Message: "Hello from Go backend!"}
	json.NewEncoder(w).Encode(resp)
}
