package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/gorilla/mux"
	_ "github.com/lib/pq"
	"github.com/rs/cors"
)

const (
	host     = "localhost"
	port     = 8008
	user     = "postgres"
	password = "1234"
	dbname   = "NAaaS"
)

// Defining different structs that'll be used in the api
type InputVars struct {
	Timeframe string `json:"timeframe"`
	Location  string `json:"location"`
	Keywords  string `json:"keywords"`
}

type initialData struct {
	StartTime string   `json:"startTime"`
	EndTime   string   `json:"endTime"`
	Location  []string `json:"locations"`
}

type requestDate struct {
	StartDate string `json:"startDate"`
	EndDate   string `json:"endDate"`
	Location  string `json:"location"`
}

type newsData struct {
	FocusTime     string `json:"focusTime"`
	FocusLocation string `json:"focusLocation"`
	Header        string `json:"header"`
	Link          string `json:"link"`
	Category      string `json:"category"`
	Coordinates   string `json:"coordinates"`
}

func main() {
	fmt.Println("Welcome to building an api inn GOLANG")
	r := mux.NewRouter()

	// routing
	r.HandleFunc("/", PostData).Methods("POST")
	// Get Requests
	r.HandleFunc("/SearchKeywords/{keywords}", getKeywords).Methods("GET")
	r.HandleFunc("/SearchLocation/{location}", getLocation).Methods("GET")
	r.HandleFunc("/SearchNews/{timeframe}", getTimeFrame).Methods("GET")
	r.HandleFunc("/getData", getInitialData).Methods("GET")
	// Post Requests
	r.HandleFunc("/PostedData", PostData).Methods("POST")
	// Setting up of CORS and giving access
	c := cors.New(cors.Options{
		AllowedOrigins:   []string{"http://localhost:8080"},
		AllowCredentials: true,
	})

	handler := c.Handler(r)
	// listen to port
	log.Fatal(http.ListenAndServe(":4000", handler))

}

// Function to get the keywords when user enters them
func getKeywords(w http.ResponseWriter, r *http.Request) {
	fmt.Println("Get Keywords")
	w.Header().Set("Content=Type", "application/json")
	params := mux.Vars(r)
	fmt.Println("Keywords : ", params["keywords"])
	json.NewEncoder(w).Encode(params["keywords"])
}

// Function to get the timeframe when user inputs
func getTimeFrame(w http.ResponseWriter, r *http.Request) {
	var req requestDate
	params := mux.Vars(r)
	param := params["timeframe"]

	json.Unmarshal([]byte(param), &req)
	fmt.Println(req)
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
	w.Header().Set("Content=Type", "application/json")
	psqlInfo := fmt.Sprintf("host=%s port=%d user=%s "+
		"password=%s dbname=%s sslmode=disable",
		host, port, user, password, dbname)
	db, err := sql.Open("postgres", psqlInfo)
	if err != nil {
		panic(err)
	}
	defer db.Close()
	var (
		header         string
		focus_time     string
		focus_location string
		link           string
		category       string
		coordinates    string
	)
	var rows *sql.Rows
	if req.Location == "" {
		if req.StartDate != "" && req.EndDate != "" {
			rows, err = db.Query("select distinct(n.header), n.focus_time::date, n.category, n.link, n.focus_location, concat (p.coordinates, d.coordinates) as coordinates from news as n left join district as d on d.name = n.focus_location left join province as p on p.name = n.focus_location where n.focus_time::date between $1 and $2 ;", req.StartDate, req.EndDate)
		}
	} else if req.Location != "" && (req.EndDate == "" || req.StartDate == "") {
		rows, err = db.Query("select distinct(n.header), n.focus_time::date,  n.category, n.link, n.focus_location, concat (p.coordinates, d.coordinates) as coordinates from news as n left join district as d on d.name = n.focus_location left join province as p on p.name = n.focus_location where n.district = $1 ;", req.Location)
	} else if req.Location != "" && req.EndDate != "" && req.StartDate != "" {
		fmt.Println("THIS QUERY WAS RAN Here")
		rows, err = db.Query("select distinct(n.header), n.focus_time::date, n.category, n.link, n.focus_location, concat (p.coordinates, d.coordinates) as coordinates from news as n left join district as d on d.name = n.focus_location left join province as p on p.name = n.focus_location where n.district = $1 and n.focus_time::date between $2 and $3 ;", req.Location, req.StartDate, req.EndDate)
	}
	if err != nil {
		log.Fatal(err)

	}
	defer rows.Close()
	var news []newsData
	for rows.Next() {
		err := rows.Scan(&header, &focus_time, &category, &link, &focus_location, &coordinates)
		if err != nil {
			log.Fatal(err)
		}
		var temp newsData
		temp.Header = header
		temp.FocusLocation = focus_location
		temp.FocusTime = focus_time[:10]
		temp.Coordinates = coordinates
		temp.Category = category
		temp.Link = link
		news = append(news, temp)
	}
	json.NewEncoder(w).Encode(news)
}

// Function to get the user input location
func getLocation(w http.ResponseWriter, r *http.Request) {
	fmt.Println("Get Location")
	w.Header().Set("Content=Type", "application/json")
	// grab id from request
	params := mux.Vars(r)
	fmt.Println("Location : ", params["location"])
	json.NewEncoder(w).Encode(params["location"])
}

// Function to allow user to post some data
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
	_ = json.NewDecoder(r.Body).Decode(&temp)

	json.NewEncoder(w).Encode(temp)
	fmt.Println("Keywords :", temp.Keywords)
	fmt.Println("Location :", temp.Location)
	fmt.Println("Time frame : ", temp.Timeframe)
}

// Function to get all the data from the user in the initialData struct and generate a query based on that data
func getInitialData(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
	w.Header().Set("Content=Type", "application/json")
	psqlInfo := fmt.Sprintf("host=%s port=%d user=%s "+
		"password=%s dbname=%s sslmode=disable",
		host, port, user, password, dbname)
	db, err := sql.Open("postgres", psqlInfo)
	if err != nil {
		panic(err)
	}
	defer db.Close()
	// var data initialData
	var (
		name      string
		startTime string
		endTime   string
	)
	rows, err := db.Query("SELECT distinct(district) from news where district is not null;")
	if err != nil {
		log.Fatal(err)

	}
	defer rows.Close()
	var poke initialData
	for rows.Next() {
		err := rows.Scan(&name)
		if err != nil {
			log.Fatal(err)
		}
		poke.Location = append(poke.Location, name)
	}
	rows, err = db.Query("Select min(focus_time)::date, max(focus_time)::date from NEWS;")
	defer rows.Close()
	for rows.Next() {
		err := rows.Scan(&startTime, &endTime)
		if err != nil {
			log.Fatal(err)
		}
		startTime = startTime[:10]
		endTime = endTime[:10]
	}
	poke.StartTime = startTime
	poke.EndTime = endTime
	json.NewEncoder(w).Encode(poke)
}
