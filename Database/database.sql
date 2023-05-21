--Province table
CREATE TABLE province(
   id serial,
   name VARCHAR(50) PRIMARY KEY,
   coordinates json not null
);
--Copy from csv file to table, change path here
COPY province(name, coordinates)
FROM 'C:\Danyal\Work\FAST\Semester 7\Final Year Project - I\Dummy Project\province.csv' DELIMITER ',' CSV HEADER;

-- Queries to make table similar to tehsil table for foreign keys
insert into province(name, coordinates)
values('FATA', '{}');

CREATE TABLE district(
   id serial,
   name VARCHAR(50) PRIMARY KEY,
   coordinates json not null,
   province varchar(50),
   CONSTRAINT fk_district FOREIGN KEY(province) REFERENCES province(name)
);

COPY district(province, name, coordinates)
FROM 'C:\Danyal\Work\FAST\Semester 7\Final Year Project - I\Dummy Project\district.csv' DELIMITER ',' CSV HEADER;


-- Queries to make table similar to district table for foreign keys
insert into district(province, name, coordinates)
select province,
   'HATTIAN',
   coordinates
from district
where name = 'HATTIAN BALA';
insert into district(province, name, coordinates)
select province,
   'KACHHI(BOLAN)',
   coordinates
from district
where name = 'KACHHI';
insert into district(province, name, coordinates)
select name,
   'DISPUTED TERRITORY',
   coordinates
from province
where name = 'INDIAN OCCUPIED KASHMIR';
insert into district(province, name, coordinates)
select name,
   'NORTH WAZIRISTAN AGENCY',
   coordinates
from province
where name = 'KHYBER PAKHTUNKHWA';
insert into district(province, name, coordinates)
select name,
   'SOUTH WAZIRISTAN AGENCY',
   coordinates
from province
where name = 'KHYBER PAKHTUNKHWA';
insert into district(province, name, coordinates)
select province,
   'DERA ISMAIL KHAN',
   coordinates
from district
where name = 'D I KHAN';
insert into district(province, name, coordinates)
select name,
   'KOHISTAN',
   coordinates
from province
where name = 'KHYBER PAKHTUNKHWA';
insert into district(province, name, coordinates)
select province,
   'NOWSHERA_',
   coordinates
from district
where name = 'NOWSHERA';
insert into district(province, name, coordinates)
select province,
   'NOWSHEHRA_',
   coordinates
from district
where name = 'NOWSHERA';
insert into district(province, name, coordinates)
select province,
   'TORGHER',
   coordinates
from district
where name = 'TORDHER';
insert into district(province, name, coordinates)
select province,
   'DERA GHAZI KHAN',
   coordinates
from district
where name = 'D G KHAN';
insert into district(province, name, coordinates)
select province,
   'MUZAFFARGARH',
   coordinates
from district
where name = 'MUZAFARGARH';
insert into district(province, name, coordinates)
select province,
   'PAK PATTAN',
   coordinates
from district
where name = 'PAKPATTAN';
insert into district(province, name, coordinates)
select province,
   'RAHIM YAR KHAN',
   coordinates
from district
where name = 'R Y KHAN';
insert into district(province, name, coordinates)
select province,
   'TOBA TEK SINGH',
   coordinates
from district
where name = 'T. T SINGH';
insert into district(province, name, coordinates)
select province,
   'NAUSHAHRO FEROZE',
   coordinates
from district
where name = 'NAUSHAHRO FEROZ';
insert into district(province, name, coordinates)
select province,
   'SHAHEED BENAZIRABAD',
   coordinates
from district
where name = 'S. BENAZIRABAD';
insert into district(province, name, coordinates)
select province,
   'SHIKARPUR',
   coordinates
from district
where name = 'SHIKARPHUR';
insert into district(province, name, coordinates)
select province,
   'TANDO ALLAH YAR',
   coordinates
from district
where name = 'T. AYAR';
insert into district(province, name, coordinates)
select province,
   'TANDO MUHAMMAD KHAN',
   coordinates
from district
where name = 'T. M KHAN';
insert into district(province, name, coordinates)
select province,
   'THAR PARKAR',
   coordinates
from district
where name = 'THARPARKAR';
insert into district(province, name, coordinates)
select province,
   'SUJAWAL',
   coordinates
from district
where name = 'SUJJAWAL';
insert into district(province, name, coordinates)
select province,
   'UMER KOT',
   coordinates
from district
where name = 'UMERKOT';
insert into district(province, name, coordinates)
select province,
   'Peshawar',
   coordinates
from district
where name = 'PESHAWAR';
insert into district(province, name, coordinates)
select province,
   'KARACHI',
   coordinates
from district
where name = 'KARACHI CENTRAL';
CREATE TABLE tehsil(
   id serial,
   name VARCHAR(50) PRIMARY KEY,
   coordinates json not null,
   district varchar(50),
   CONSTRAINT fk_tehsil FOREIGN KEY(district) REFERENCES district(name)
);
COPY tehsil(district, name, coordinates)
FROM 'C:\Danyal\Work\FAST\Semester 7\Final Year Project - I\Dummy Project\tehsil.csv' DELIMITER ',' CSV HEADER;
CREATE TABLE union_council(
   id serial,
   name VARCHAR(50) PRIMARY KEY,
   coordinates json not null,
   tehsil varchar(50),
   CONSTRAINT fk_union FOREIGN KEY(tehsil) REFERENCES tehsil(name)
);
CREATE TABLE NEWS_Dawn(
   id serial,
   header TEXT,
   summary TEXT,
   details TEXT,
   link TEXT,
   category VARCHAR(100),
   topics TEXT [],
   focus_time TIMESTAMP,
   focus_location VARCHAR(50),
   location_type VARCHAR(50),
   sentiment VARCHAR(20),
   creation_date TIMESTAMP,
   province VARCHAR(50),
   district VARCHAR(50),
   tehsil VARCHAR(50),
   union_council VARCHAR(50),
   CONSTRAINT fk_province FOREIGN KEY(province) REFERENCES province(name),
   CONSTRAINT fk_district FOREIGN KEY(district) REFERENCES district(name),
   CONSTRAINT fk_tehsil FOREIGN KEY(tehsil) REFERENCES tehsil(name),
   CONSTRAINT fk_union FOREIGN KEY(union_council) REFERENCES union_council(name),
   CONSTRAINT PK_NEWS PRIMARY KEY(id, focus_time, focus_location)
);

CREATE TABLE NEWS_Tribune(
   id serial,
   header TEXT,
   summary TEXT,
   details TEXT,
   link TEXT,
   category VARCHAR(100),
   sentiment VARCHAR(20),
   creation_date TIMESTAMP,
   topics TEXT [],
   focus_time TIMESTAMP,
   focus_location VARCHAR(50),
   location_type VARCHAR(50),
   province VARCHAR(50),
   district VARCHAR(50),
   tehsil VARCHAR(50),
   union_council VARCHAR(50),
   picture TEXT,
   CONSTRAINT fk_province FOREIGN KEY(province) REFERENCES province(name),
   CONSTRAINT fk_district FOREIGN KEY(district) REFERENCES district(name),
   CONSTRAINT fk_tehsil FOREIGN KEY(tehsil) REFERENCES tehsil(name),
   CONSTRAINT fk_union FOREIGN KEY(union_council) REFERENCES union_council(name),
   CONSTRAINT PK_NEWS_Tribune PRIMARY KEY(id, focus_time, focus_location)
);

-- -- Sample Query
-- insert into NEWS(
--       header,
--       details,
--       link,
--       focus_time,
--       focus_location,
--       province
--    )
-- VALUES(
--       'header',
--       'details 123',
--       'http',
--       '2022-05-16',
--       'KARACHI',
--       'SINDH'
--    );


-- Table to hold all the locations and their type to search for type when searching for NEWS
CREATE TABLE Locations(
   id serial,
   name VARCHAR(50),
   location_type VARCHAR(50)
);

-- Insert all entries from all tables into Locations table
INSERT INTO Locations(name, location_type)
select name, 'Province' from province;

INSERT INTO Locations(name, location_type)
select name, 'District' from district;

INSERT INTO Locations(name, location_type)
select name, 'Tehsil' from tehsil;

INSERT INTO Locations(name, location_type)
select name, 'Union_Council' from union_council;

-- UPDATE NEWS n
-- SET location_type = l.location_type from locations l where l.name = n.focus_location;

-- SELECT n.focus_location, CASE 
-- 	  WHEN n.location_type = 'Province' THEN p.coordinates 
-- 	  WHEN n.location_type = 'District' THEN d.coordinates 
-- 	  ELSE NULL 
-- 	END AS coordinates 
--   FROM 
-- 	news n 
-- 	LEFT JOIN province p ON n.focus_location = p.name AND n.location_type = 'Province' 
-- 	LEFT JOIN district d ON n.focus_location = d.name AND n.location_type = 'District' limit 1;

--    SELECT n.topics,
--   CASE 
--     WHEN n.location_type = 'Province' THEN p.name 
--     WHEN n.location_type = 'District' THEN d.name
--     WHEN n.location_type = 'Tehsil' THEN t.name 

--     ELSE NULL 
--   END AS location
-- FROM 
--   news n 
--   LEFT JOIN province p ON n.focus_location = p.name AND n.location_type = 'Province' 
--   LEFT JOIN district d ON n.focus_location = d.name AND n.location_type = 'District'
--   LEFT JOIN tehsil t ON n.focus_location = t.name AND n.location_type = 'Tehsil' 
--  where n.province = 'PUNJAB' and n.focus_time::date between '2022-12-20' and '2022-12-29';


--  where ARRAY['islamabad', 'hello'] && n.topics;
-- SELECT 
--   topic, COUNT(*) AS frequency 
-- FROM 
--   (SELECT 
--     (UNNEST(topics)) AS topic 
--   FROM 
--     news n) 
--   AS extracted_topics 
-- GROUP BY topic 
-- ORDER BY frequency DESC;

-- SELECT n.focus_location 
-- FROM news n 
-- JOIN (
--   SELECT focus_location, COUNT(*) AS frequency 
--   FROM news 
--   GROUP BY focus_location 
--   ORDER BY frequency DESC
-- ) t ON n.focus_location = t.focus_location 
-- ORDER BY t.frequency DESC;


-- SELECT distinct(n.header), n.focus_time::date, n.category, n.link, n.topics, n.location_type,
-- 			CASE 
-- 			WHEN n.location_type = 'Province' THEN p.name 
-- 			WHEN n.location_type = 'District' THEN d.name
-- 			WHEN n.location_type = 'Tehsil' THEN t.name 
			
-- 			ELSE NULL 
-- 			END AS location
-- 			FROM 
-- 			news n 
-- 			LEFT JOIN province p ON n.focus_location = p.name AND n.location_type = 'Province' 
-- 			LEFT JOIN district d ON n.focus_location = d.name AND n.location_type = 'District'
-- 			LEFT JOIN tehsil t ON n.focus_location = t.name AND n.location_type = 'Tehsil';