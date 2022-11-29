package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

type InputVars struct {
	Timeframe string   `json:"timeframe"`
	Location  []string `json:"location"`
	Keywords  []string `json:"keywords"`
}

// // fake DB
// var db []InputVars

// // Store words
// var words []string

func main() {
	fmt.Println("Welcome to building an api inn GOLANG")
	r := mux.NewRouter()

	// // seeding
	// courses = append(courses, Course{CourseID: "2", CourseName: "GOLANG", CoursePrice: 299, Author: &Author{Fullname: "Mehmood Amjad", Website: "securiti.go"}})
	// courses = append(courses, Course{CourseID: "4", CourseName: "Docker", CoursePrice: 399, Author: &Author{Fullname: "Mehmood Amjad", Website: "foundri.go"}})
	// routing
	r.HandleFunc("/", serveHome).Methods("GET")
	r.HandleFunc("/SearchKeywords/{keywords}", getKeywords).Methods("GET")
	r.HandleFunc("/SearchLocation/{location}", getLocation).Methods("GET")
	r.HandleFunc("/SearchTime/{timeframe}", getTimeFrame).Methods("GET")
	r.HandleFunc("/PostedData", PostData).Methods("POST")

	// r.HandleFunc("/courses", getAllCourses).Methods("GET")
	// r.HandleFunc("/course/{courseid}", getOneCourse).Methods("GET")
	// r.HandleFunc("/course", createOneCourse).Methods("POST")
	// r.HandleFunc("/course/{courseid}", updateOneCourse).Methods("PUT")
	// r.HandleFunc("/course/{courseid}", deleteOneCourse).Methods("DELETE")

	// listen to port
	log.Fatal(http.ListenAndServe(":4000", r))
	// log.Fatal(http.ListenAndServeTLS(":4000", "cert.pem", "key.pem", r))
}

// serve home route
func serveHome(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("<h1>Welcome to API</h1>"))
}

func getKeywords(w http.ResponseWriter, r *http.Request) {
	fmt.Println("Get Keywords")
	w.Header().Set("Content=Type", "application/json")
	// grab id from request
	params := mux.Vars(r)
	// // loop through db and find matchingn keyword then return the reponse
	// for _, word := range words {
	// 	if word == params["keywords"] {
	// 		json.NewEncoder(w).Encode(word)
	// 		return
	// 	}
	// }
	fmt.Println("Keywords : ", params["keywords"])
	json.NewEncoder(w).Encode(params["keywords"])
}
func getTimeFrame(w http.ResponseWriter, r *http.Request) {
	fmt.Println("Get Time Frame")
	w.Header().Set("Content=Type", "application/json")
	// grab id from request
	params := mux.Vars(r)
	fmt.Println("TimeFrame : ", params["timeframe"])
	json.NewEncoder(w).Encode(params["timeframe"])
}
func getLocation(w http.ResponseWriter, r *http.Request) {
	fmt.Println("Get Location")
	w.Header().Set("Content=Type", "application/json")
	// grab id from request
	params := mux.Vars(r)
	fmt.Println("Location : ", params["location"])
	json.NewEncoder(w).Encode(params["location"])
}
func PostData(w http.ResponseWriter, r *http.Request) {
	// Allow CORS here By * or specific origin
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
	w.Header().Set("Content=Type", "application/json")
	fmt.Println("Post Data")

	// what if body is empty
	if r.Body == nil {
		json.NewEncoder(w).Encode("Please send some data")
	}

	var temp InputVars
	data := json.NewDecoder(r.Body).Decode(&temp)

	json.NewEncoder(w).Encode(data)
}
