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
	// Link          string `json:"link"`
	Coordinates string `json:"coordinates"`
}

// // fake DB

// // Store words
// var words []string
func main() {
	fmt.Println("Welcome to building an api inn GOLANG")
	r := mux.NewRouter()

	// // seeding
	// courses = append(courses, Course{CourseID: "2", CourseName: "GOLANG", CoursePrice: 299, Author: &Author{Fullname: "Mehmood Amjad", Website: "securiti.go"}})
	// courses = append(courses, Course{CourseID: "4", CourseName: "Docker", CoursePrice: 399, Author: &Author{Fullname: "Mehmood Amjad", Website: "foundri.go"}})
	// routing
	r.HandleFunc("/", PostData).Methods("POST")
	r.HandleFunc("/SearchKeywords/{keywords}", getKeywords).Methods("GET")
	r.HandleFunc("/SearchLocation/{location}", getLocation).Methods("GET")
	r.HandleFunc("/SearchTime/{timeframe}", getTimeFrame).Methods("GET")
	r.HandleFunc("/PostedData", PostData).Methods("POST")
	r.HandleFunc("/Pokemon", getInitialData).Methods("GET")
	// r.HandleFunc("/courses", getAllCourses).Methods("GET")
	// r.HandleFunc("/course/{courseid}", getOneCourse).Methods("GET")
	// r.HandleFunc("/course", createOneCourse).Methods("POST")
	// r.HandleFunc("/course/{courseid}", updateOneCourse).Methods("PUT")
	// r.HandleFunc("/course/{courseid}", deleteOneCourse).Methods("DELETE")

	// listen to port
	// log.Fatal(http.ListenAndServeTLS(":4000", "cert.pem", "key.pem", r))

	// var err error
	// db, err := sql.Open("postgres", psqlInfo)
	// if err != nil {
	// 	panic(err)
	// }
	// defer db.Close()

	// err = db.Ping()
	// if err != nil {
	// 	panic(err)
	// }

	// fmt.Println("Successfully connected!")

	// db.Query("SELECT name from Province;")
	// fmt.Println("Here")
	// getInitialData()
	c := cors.New(cors.Options{
		AllowedOrigins:   []string{"http://localhost:8080"},
		AllowCredentials: true,
	})

	handler := c.Handler(r)
	log.Fatal(http.ListenAndServe(":4000", handler))

}

// serve home route
// func serveHome(w http.ResponseWriter, r *http.Request) {
// 	w.Write([]byte("<h1>Welcome to API</h1>"))
// }

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
	// fmt.Println("Get Time Frame")
	// w.Header().Set("Content=Type", "application/json")
	// grab id from request
	var req requestDate
	params := mux.Vars(r)
	param := params["timeframe"]
	// json.NewDecoder(params["timeFrame"]).Decode(req)
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
	// var data initialData
	var (
		header         string
		focus_time     string
		focus_location string
		// link           string
		coordinates string
	)
	// // db.Query("select n.*, p.* from news as n left join province as p on p.name = (select province from news where focus_time >= startTime and focus_time <= endTime);")
	// select n.header, n.link, n.focus_time, n.focus_location, d.name from news as n left join district as d on d.name = n.focus_location and n.focus_time >= '2022-02-01' and n.focus_time <= '2022-03-27';
	rows, err := db.Query("select distinct(n.header), n.focus_time::date, n.focus_location, concat (p.coordinates, d.coordinates) as coordinates from news as n left join district as d on d.name = n.focus_location left join province as p on p.name = n.focus_location where n.focus_time::date between $1 and $2 ;", req.StartDate, req.EndDate)
	if err != nil {
		log.Fatal(err)

	}
	defer rows.Close()
	var news []newsData
	for rows.Next() {
		err := rows.Scan(&header, &focus_time, &focus_location, &coordinates)
		if err != nil {
			log.Fatal(err)
		}
		// fmt.Println(header, focus_time)
		var temp newsData
		temp.Header = header
		temp.FocusLocation = focus_location
		temp.FocusTime = focus_time[:10]
		temp.Coordinates = coordinates
		news = append(news, temp)
		// fmt.Println("TimeFrame : ", temp)
	}
	json.NewEncoder(w).Encode(news)
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
	_ = json.NewDecoder(r.Body).Decode(&temp)

	json.NewEncoder(w).Encode(temp)
	fmt.Println("Keywords :", temp.Keywords)
	fmt.Println("Location :", temp.Location)
	fmt.Println("Time frame : ", temp.Timeframe)
	// w.Write([]byte(temp))
}

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
	// fmt.Println("Here")
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
		// fmt.Println(name)
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
