package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/gorilla/mux"
	_ "github.com/lib/pq"
)

const (
	host     = "localhost"
	port     = 8008
	user     = "postgres"
	password = "1234"
	dbname   = "NAaaS"
)

type InputVars struct {
	Timeframe string   `json:"timeframe"`
	Location  []string `json:"location"`
	Keywords  []string `json:"keywords"`
}

type initialData struct {
	startTime string   `json:"startTime"`
	endTime   string   `json:"endTime"`
	Location  []string `json:"location"`
}

// // fake DB
var db sql.DB

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
	// log.Fatal(http.ListenAndServeTLS(":4000", "cert.pem", "key.pem", r))
	psqlInfo := fmt.Sprintf("host=%s port=%d user=%s "+
		"password=%s dbname=%s sslmode=disable",
		host, port, user, password, dbname)
	db, err := sql.Open("postgres", psqlInfo)
	if err != nil {
		panic(err)
	}
	defer db.Close()

	err = db.Ping()
	if err != nil {
		panic(err)
	}

	fmt.Println("Successfully connected!")
	getInitialData()
	log.Fatal(http.ListenAndServe(":4000", r))
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
	// // db.Query("select n.*, p.* from news as n left join province as p on p.name = (select province from news where focus_time >= startTime and focus_time <= endTime);")
	// db.Query("select n.*, p.* from news as n left join province as p on p.name = n.province and n.focus_time >= '2022-02-01' and n.focus_time <= '2022-03-27';")

	fmt.Println("TimeFrame : ", params["timeframe"])
	json.NewEncoder(w).Encode(params["timeframe"])
}
func getLocation(w http.ResponseWriter, r *http.Request) {
	fmt.Println("Get Location")
	w.Header().Set("Content=Type", "application/json")
	// grab id from request
	params := mux.Vars(r)
	// db.Query("select * from news where province=params")
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

func getInitialData() {
	// w.Header().Set("Content=Type", "application/json")
	// db, err := sql.Open("postgres", psqlInfo)
	// rows, err := db.Query("SELECT name from Province;")
	// var data initialData
	var (
		name string
	)
	var rows, err = db.Query("SELECT name from Province;")
	if err != nil {
		log.Fatal(err)

	}
	defer rows.Close()
	for rows.Next() {
		err := rows.Scan(&name)
		if err != nil {
			log.Fatal(err)
		}
		fmt.Println(name)
	}
	// db.Query("Select name from Province")
	// db.Query("Select min(focus_time) from NEWS")
	// db.Query("Select max(focus_time) from NEWS")

}
