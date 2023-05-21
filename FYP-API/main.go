package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/gorilla/mux"
	"github.com/lib/pq"
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

type locations struct {
	Name          string `json:"name"`
	Location_type string `json:"location_type"`
}

type initialData struct {
	StartTime string      `json:"startTime"`
	EndTime   string      `json:"endTime"`
	Location  []locations `json:"locations"`
	Topics    []string    `json:"topics"`
}

type request struct {
	StartDate string   `json:"startDate"`
	EndDate   string   `json:"endDate"`
	Location  string   `json:"location"`
	Topics    []string `json:"topics"`
}

type dataRequest struct {
	Source string `json:"source"`
}

type newsData struct {
	FocusTime     string `json:"focusTime"`
	FocusLocation string `json:"focusLocation"`
	Header        string `json:"header"`
	Link          string `json:"link"`
	Category      string `json:"category"`
	Coordinates   string `json:"coordinates"`
	Topics        string `json:"topics"`
	LocationType  string `json:"locationType"`
	Sentiment     string `json:"sentiment"`
	CreationDate  string `json:"creationDate"`
}

type newsDataTribune struct {
	FocusTime     string `json:"focusTime"`
	FocusLocation string `json:"focusLocation"`
	Header        string `json:"header"`
	Link          string `json:"link"`
	Category      string `json:"category"`
	Coordinates   string `json:"coordinates"`
	Topics        string `json:"topics"`
	LocationType  string `json:"locationType"`
	Picture       string `json:"picture"`
	Sentiment     string `json:"sentiment"`
	CreationDate  string `json:"creationDate"`
}

func main() {
	fmt.Println("Welcome to building an api inn GOLANG")
	r := mux.NewRouter()

	// routing
	r.HandleFunc("/", PostData).Methods("POST")
	// Get Requests
	r.HandleFunc("/SearchDawn/{keywords}", getKeywords).Methods("GET")
	r.HandleFunc("/SearchTribune/{location}", getLocation).Methods("GET")
	r.HandleFunc("/SearchNews/{timeframe}", getTimeFrame).Methods("GET")
	r.HandleFunc("/getData/{initialData}", getInitialData).Methods("GET")
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
	var req request
	params := mux.Vars(r)
	param := params["keywords"]

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
		location_type  string
		topics         string
		sentiment      string
		creationDate   string
	)

	defer db.Close()
	var rows *sql.Rows
	if req.Location == "" {
		if len(req.Topics) > 0 {
			rows, err = db.Query(`   SELECT n.header, n.focus_time::date, n.category, n.link, n.topics, n.location_type, n.sentiment, n.creation_date,
			CASE 
			WHEN n.location_type = 'Province' THEN p.name 
			WHEN n.location_type = 'District' THEN d.name
			WHEN n.location_type = 'Tehsil' THEN t.name 
			
			ELSE NULL 
			END AS location, 
			CASE 
			WHEN n.location_type = 'Province' THEN p.coordinates 
			WHEN n.location_type = 'District' THEN d.coordinates
			WHEN n.location_type = 'Tehsil' THEN t.coordinates 
			ELSE NULL 
			END AS coordinates 
			FROM 
			news_dawn n 
			LEFT JOIN province p ON n.focus_location = p.name AND n.location_type = 'Province' 
			LEFT JOIN district d ON n.focus_location = d.name AND n.location_type = 'District'
			LEFT JOIN tehsil t ON n.focus_location = t.name AND n.location_type = 'Tehsil'
			where n.focus_time::date between $1 and $2 and $3 && n.topics;`, req.StartDate, req.EndDate, pq.Array(req.Topics))
		} else {
			rows, err = db.Query(`   SELECT n.header, n.focus_time::date, n.category, n.link, n.topics, n.location_type, n.sentiment, n.creation_date,
			CASE 
			WHEN n.location_type = 'Province' THEN p.name 
			WHEN n.location_type = 'District' THEN d.name
			WHEN n.location_type = 'Tehsil' THEN t.name 
			
			ELSE NULL 
			END AS location, 
			CASE 
			WHEN n.location_type = 'Province' THEN p.coordinates 
			WHEN n.location_type = 'District' THEN d.coordinates
			WHEN n.location_type = 'Tehsil' THEN t.coordinates 
			ELSE NULL 
			END AS coordinates 
			FROM 
			news_dawn n 
			LEFT JOIN province p ON n.focus_location = p.name AND n.location_type = 'Province' 
			LEFT JOIN district d ON n.focus_location = d.name AND n.location_type = 'District'
			LEFT JOIN tehsil t ON n.focus_location = t.name AND n.location_type = 'Tehsil'
			where n.focus_time::date between $1 and $2;`, req.StartDate, req.EndDate)
		}
	} else {
		err = db.QueryRow("select location_type from locations where name= $1", req.Location).Scan(&location_type)
		if len(req.Topics) > 0 {
			query := fmt.Sprintf(`   SELECT n.header, n.focus_time::date, n.category, n.link, n.topics, n.location_type, n.sentiment, n.creation_date,
			CASE 
			WHEN n.location_type = 'Province' THEN p.name 
			WHEN n.location_type = 'District' THEN d.name
			WHEN n.location_type = 'Tehsil' THEN t.name 
			
			ELSE NULL 
			END AS location,
			CASE 
			WHEN n.location_type = 'Province' THEN p.coordinates 
			WHEN n.location_type = 'District' THEN d.coordinates
			WHEN n.location_type = 'Tehsil' THEN t.coordinates 
			ELSE NULL 
			END AS coordinates 
			FROM 
			news_dawn n 
			LEFT JOIN province p ON n.focus_location = p.name AND n.location_type = 'Province' 
			LEFT JOIN district d ON n.focus_location = d.name AND n.location_type = 'District'
			LEFT JOIN tehsil t ON n.focus_location = t.name AND n.location_type = 'Tehsil'
			where n.%s = $1 and n.focus_time::date between $2 and $3 and $4 && n.topics;`, location_type)

			rows, err = db.Query(query, req.Location, req.StartDate, req.EndDate, pq.Array(req.Topics))
		} else {
			query := fmt.Sprintf(`   SELECT n.header, n.focus_time::date, n.category, n.link, n.topics, n.location_type, n.sentiment, n.creation_date,
			CASE 
			WHEN n.location_type = 'Province' THEN p.name 
			WHEN n.location_type = 'District' THEN d.name
			WHEN n.location_type = 'Tehsil' THEN t.name 
			
			ELSE NULL 
			END AS location,
			CASE 
			WHEN n.location_type = 'Province' THEN p.coordinates 
			WHEN n.location_type = 'District' THEN d.coordinates
			WHEN n.location_type = 'Tehsil' THEN t.coordinates 
			ELSE NULL 
			END AS coordinates 
			FROM 
			news_dawn n 
			LEFT JOIN province p ON n.focus_location = p.name AND n.location_type = 'Province' 
			LEFT JOIN district d ON n.focus_location = d.name AND n.location_type = 'District'
			LEFT JOIN tehsil t ON n.focus_location = t.name AND n.location_type = 'Tehsil'
			where n.%s = $1 and n.focus_time::date between $2 and $3;`, location_type)
			fmt.Println(query)

			rows, err = db.Query(query, req.Location, req.StartDate, req.EndDate)
		}
	}
	if err != nil {
		log.Fatal(err)

	}
	defer rows.Close()
	var news []newsData
	for rows.Next() {
		err := rows.Scan(&header, &focus_time, &category, &link, &topics, &location_type, &sentiment, &creationDate, &focus_location, &coordinates)
		if err != nil {
			log.Fatal(err)
		}
		var temp newsData
		temp.Header = header
		temp.FocusLocation = focus_location
		temp.FocusTime = focus_time[:10]
		temp.Coordinates = coordinates
		temp.LocationType = location_type
		temp.Topics = topics
		temp.Category = category
		temp.Link = link
		temp.Sentiment = sentiment
		temp.CreationDate = creationDate[:10]
		// fmt.Println(coordinates)
		// json.Unmarshal([]byte(coordinates), &temp.Coordinates)
		news = append(news, temp)
	}
	json.NewEncoder(w).Encode(news)
	// params := mux.Vars(r)
	// fmt.Println("Keywords : ", params["keywords"])
	// json.NewEncoder(w).Encode(params["keywords"])
}

// Function to get the timeframe when user inputs
func getTimeFrame(w http.ResponseWriter, r *http.Request) {
	var req request
	params := mux.Vars(r)
	param := params["timeframe"]

	json.Unmarshal([]byte(param), &req)
	fmt.Println(req.Location, req)
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
		location_type  string
	)
	var rows *sql.Rows
	if req.Location == "" {
		if req.StartDate != "" && req.EndDate != "" {
			rows, err = db.Query("select distinct(n.header), n.focus_time::date, n.category, n.link, n.focus_location, concat (p.coordinates, d.coordinates) as coordinates from news as n left join district as d on d.name = n.focus_location left join province as p on p.name = n.focus_location where n.focus_time::date between $1 and $2 ;", req.StartDate, req.EndDate)
		}
	} else {
		err = db.QueryRow("select location_type from locations where name= $1", req.Location).Scan(&location_type)
		query := fmt.Sprintf("select distinct(n.header), n.focus_time::date,  n.category, n.link, n.focus_location, concat (p.coordinates, d.coordinates) as coordinates from news as n left join tehsil as t on t.name = n.focus_location left join district as d on d.name = n.focus_location left join province as p on p.name = n.focus_location where n.%s = $1;", location_type)
		query_time := fmt.Sprintf("select distinct(n.header), n.focus_time::date,  n.category, n.link, n.focus_location, concat (p.coordinates, d.coordinates) as coordinates from news as n left join tehsil as t on t.name = n.focus_location left join district as d on d.name = n.focus_location left join province as p on p.name = n.focus_location where n.%s = $1 and n.focus_time::date between $2 and $3 ;", location_type)
		if req.Location != "" && (req.EndDate == "" || req.StartDate == "") {
			rows, err = db.Query(query, req.Location)
		} else if req.Location != "" && req.EndDate != "" && req.StartDate != "" {
			// fmt.Println("Query was run till here")
			rows, err = db.Query(query_time, req.Location, req.StartDate, req.EndDate)
		}
	}
	// if location_type == "Province" {
	// 	if req.Location == "" {
	// 		if req.StartDate != "" && req.EndDate != "" {
	// 			rows, err = db.Query("select distinct(n.header), n.focus_time::date, n.category, n.link, n.focus_location, p.coordinates as coordinates from news as n left join province as p on p.name = n.focus_location where n.focus_time::date between $1 and $2 ;", req.StartDate, req.EndDate)
	// 		}
	// 	} else if req.Location != "" && (req.EndDate == "" || req.StartDate == "") {
	// 		rows, err = db.Query(query, req.Location)
	// 	} else if req.Location != "" && req.EndDate != "" && req.StartDate != "" {
	// 		fmt.Println("Query was run till here")
	// 		rows, err = db.Query(query_time, req.Location, req.StartDate, req.EndDate)
	// 	}
	// } else if location_type == "District" {
	// 	if req.Location == "" {
	// 		if req.StartDate != "" && req.EndDate != "" {
	// 			rows, err = db.Query("select distinct(n.header), n.focus_time::date, n.category, n.link, n.focus_location, concat (p.coordinates, d.coordinates) as coordinates from news as n left join district as d on d.name = n.focus_location left join province as p on p.name = n.focus_location where n.focus_time::date between $1 and $2 ;", req.StartDate, req.EndDate)
	// 		}
	// 	} else if req.Location != "" && (req.EndDate == "" || req.StartDate == "") {
	// 		rows, err = db.Query("select distinct(n.header), n.focus_time::date,  n.category, n.link, n.focus_location, concat (p.coordinates, d.coordinates) as coordinates from news as n left join district as d on d.name = n.focus_location left join province as p on p.name = n.focus_location where n.district = $1 ;", req.Location)
	// 	} else if req.Location != "" && req.EndDate != "" && req.StartDate != "" {
	// 		rows, err = db.Query("select distinct(n.header), n.focus_time::date, n.category, n.link, n.focus_location, concat (p.coordinates, d.coordinates) as coordinates from news as n left join district as d on d.name = n.focus_location left join province as p on p.name = n.focus_location where n.district = $1 and n.focus_time::date between $2 and $3 ;", req.Location, req.StartDate, req.EndDate)
	// 	}
	// } else if location_type == "Tehsil" {
	// 	if req.Location == "" {
	// 		if req.StartDate != "" && req.EndDate != "" {
	// 			rows, err = db.Query("select distinct(n.header), n.focus_time::date, n.category, n.link, n.focus_location, concat (p.coordinates, d.coordinates) as coordinates from news as n left join district as d on d.name = n.focus_location left join province as p on p.name = n.focus_location where n.focus_time::date between $1 and $2 ;", req.StartDate, req.EndDate)
	// 		}
	// 	} else if req.Location != "" && (req.EndDate == "" || req.StartDate == "") {
	// 		rows, err = db.Query("select distinct(n.header), n.focus_time::date,  n.category, n.link, n.focus_location, concat (p.coordinates, d.coordinates) as coordinates from news as n left join district as d on d.name = n.focus_location left join province as p on p.name = n.focus_location where n.district = $1 ;", req.Location)
	// 	} else if req.Location != "" && req.EndDate != "" && req.StartDate != "" {
	// 		rows, err = db.Query("select distinct(n.header), n.focus_time::date, n.category, n.link, n.focus_location, concat (p.coordinates, d.coordinates) as coordinates from news as n left join district as d on d.name = n.focus_location left join province as p on p.name = n.focus_location where n.district = $1 and n.focus_time::date between $2 and $3 ;", req.Location, req.StartDate, req.EndDate)
	// 	}
	// }
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
		// fmt.Println(coordinates)
		// json.Unmarshal([]byte(coordinates), &temp.Coordinates)
		temp.Category = category
		temp.Link = link

		news = append(news, temp)
	}
	json.NewEncoder(w).Encode(news)
}

// Function to get the user input location
func getLocation(w http.ResponseWriter, r *http.Request) {
	var req request
	params := mux.Vars(r)
	param := params["location"]

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
		location_type  string
		topics         string
		picture        string
		sentiment      string
		creationDate   string
	)

	defer db.Close()
	var rows *sql.Rows
	if req.Location == "" {
		if len(req.Topics) > 0 {
			rows, err = db.Query(`   SELECT n.header, n.focus_time::date, n.category, n.link, n.topics, n.location_type, n.picture, n.sentiment, n.creation_date,
			CASE 
			WHEN n.location_type = 'Province' THEN p.name 
			WHEN n.location_type = 'District' THEN d.name
			WHEN n.location_type = 'Tehsil' THEN t.name 
			
			ELSE NULL 
			END AS location, 
			CASE 
			WHEN n.location_type = 'Province' THEN p.coordinates 
			WHEN n.location_type = 'District' THEN d.coordinates
			WHEN n.location_type = 'Tehsil' THEN t.coordinates 
			ELSE NULL 
			END AS coordinates 
			FROM 
			news_tribune n 
			LEFT JOIN province p ON n.focus_location = p.name AND n.location_type = 'Province' 
			LEFT JOIN district d ON n.focus_location = d.name AND n.location_type = 'District'
			LEFT JOIN tehsil t ON n.focus_location = t.name AND n.location_type = 'Tehsil'
			where n.focus_time::date between $1 and $2 and $3 && n.topics;`, req.StartDate, req.EndDate, pq.Array(req.Topics))
		} else {
			rows, err = db.Query(`   SELECT n.header, n.focus_time::date, n.category, n.link, n.topics, n.location_type, n.picture, n.sentiment, n.creation_date,
			CASE 
			WHEN n.location_type = 'Province' THEN p.name 
			WHEN n.location_type = 'District' THEN d.name
			WHEN n.location_type = 'Tehsil' THEN t.name 
			
			ELSE NULL 
			END AS location, 
			CASE 
			WHEN n.location_type = 'Province' THEN p.coordinates 
			WHEN n.location_type = 'District' THEN d.coordinates
			WHEN n.location_type = 'Tehsil' THEN t.coordinates 
			ELSE NULL 
			END AS coordinates 
			FROM 
			news_tribune n 
			LEFT JOIN province p ON n.focus_location = p.name AND n.location_type = 'Province' 
			LEFT JOIN district d ON n.focus_location = d.name AND n.location_type = 'District'
			LEFT JOIN tehsil t ON n.focus_location = t.name AND n.location_type = 'Tehsil'
			where n.focus_time::date between $1 and $2;`, req.StartDate, req.EndDate)
		}
	} else {
		err = db.QueryRow("select location_type from locations where name= $1", req.Location).Scan(&location_type)
		if len(req.Topics) > 0 {
			query := fmt.Sprintf(`   SELECT n.header, n.focus_time::date, n.category, n.link, n.topics, n.location_type, n.picture, n.sentiment, n.creation_date,
			CASE 
			WHEN n.location_type = 'Province' THEN p.name 
			WHEN n.location_type = 'District' THEN d.name
			WHEN n.location_type = 'Tehsil' THEN t.name 
			
			ELSE NULL 
			END AS location,
			CASE 
			WHEN n.location_type = 'Province' THEN p.coordinates 
			WHEN n.location_type = 'District' THEN d.coordinates
			WHEN n.location_type = 'Tehsil' THEN t.coordinates 
			ELSE NULL 
			END AS coordinates 
			FROM 
			news_tribune n 
			LEFT JOIN province p ON n.focus_location = p.name AND n.location_type = 'Province' 
			LEFT JOIN district d ON n.focus_location = d.name AND n.location_type = 'District'
			LEFT JOIN tehsil t ON n.focus_location = t.name AND n.location_type = 'Tehsil'
			where n.%s = $1 and n.focus_time::date between $2 and $3 and $4 && n.topics;`, location_type)

			rows, err = db.Query(query, req.Location, req.StartDate, req.EndDate, pq.Array(req.Topics))
		} else {
			query := fmt.Sprintf(`   SELECT n.header, n.focus_time::date, n.category, n.link, n.topics, n.location_type, n.picture, n.sentiment, n.creation_date,
			CASE 
			WHEN n.location_type = 'Province' THEN p.name 
			WHEN n.location_type = 'District' THEN d.name
			WHEN n.location_type = 'Tehsil' THEN t.name 
			
			ELSE NULL 
			END AS location,
			CASE 
			WHEN n.location_type = 'Province' THEN p.coordinates 
			WHEN n.location_type = 'District' THEN d.coordinates
			WHEN n.location_type = 'Tehsil' THEN t.coordinates 
			ELSE NULL 
			END AS coordinates 
			FROM 
			news_tribune n 
			LEFT JOIN province p ON n.focus_location = p.name AND n.location_type = 'Province' 
			LEFT JOIN district d ON n.focus_location = d.name AND n.location_type = 'District'
			LEFT JOIN tehsil t ON n.focus_location = t.name AND n.location_type = 'Tehsil'
			where n.%s = $1 and n.focus_time::date between $2 and $3;`, location_type)
			fmt.Println(query)

			rows, err = db.Query(query, req.Location, req.StartDate, req.EndDate)
		}
	}
	if err != nil {
		log.Fatal(err)

	}
	defer rows.Close()
	var news []newsDataTribune
	for rows.Next() {
		err := rows.Scan(&header, &focus_time, &category, &link, &topics, &location_type, &picture, &sentiment, &creationDate, &focus_location, &coordinates)
		if err != nil {
			log.Fatal(err)
		}
		var temp newsDataTribune
		temp.Header = header
		temp.FocusLocation = focus_location
		temp.FocusTime = focus_time[:10]
		temp.Coordinates = coordinates
		temp.LocationType = location_type
		temp.Topics = topics
		temp.Category = category
		temp.Link = link
		temp.Picture = picture
		temp.Sentiment = sentiment
		temp.CreationDate = creationDate[:10]
		// fmt.Println(coordinates)
		// json.Unmarshal([]byte(coordinates), &temp.Coordinates)
		news = append(news, temp)
	}
	json.NewEncoder(w).Encode(news)
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
	var req dataRequest
	params := mux.Vars(r)
	param := params["initialData"]

	json.Unmarshal([]byte(param), &req)
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
		name          string
		startTime     string
		endTime       string
		topic         string
		frequency     int
		location_type string
	)
	query := fmt.Sprintf("SELECT distinct(focus_location), location_type from news_%s where focus_location is not null;", req.Source)
	rows, err := db.Query(query)
	if err != nil {
		log.Fatal(err)

	}

	defer rows.Close()
	var poke initialData
	for rows.Next() {
		err := rows.Scan(&name, &location_type)
		if err != nil {
			log.Fatal(err)
		}
		var location locations
		location.Name = name
		location.Location_type = location_type
		poke.Location = append(poke.Location, location)
	}
	query = fmt.Sprintf("Select min(focus_time)::date, max(focus_time)::date from NEWS_%s;", req.Source)
	rows, err = db.Query(query)
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
	query = fmt.Sprintf(`SELECT 
	topic, COUNT(*) AS frequency 
  FROM 
	(SELECT 
	  (UNNEST(topics)) AS topic 
	FROM 
	  news_%s n) 
	AS extracted_topics 
  GROUP BY topic 
  ORDER BY frequency DESC;`, req.Source)
	rows, err = db.Query(query)
	if err != nil {
		log.Fatal(err)

	}
	defer rows.Close()
	for rows.Next() {
		err := rows.Scan(&topic, &frequency)
		if err != nil {
			log.Fatal(err)
		}
		poke.Topics = append(poke.Topics, topic)
	}
	// fmt.Println(poke)
	json.NewEncoder(w).Encode(poke)
}
