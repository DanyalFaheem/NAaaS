--Province table
CREATE TABLE province(
   id serial,
   name VARCHAR(50) PRIMARY KEY,
   coordinates json not null,
);
--Copy from csv file to table, change path here
COPY province(name, coordinates)
FROM '/home/danyal/NAaaS/province.csv' DELIMITER ',' CSV HEADER;

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
FROM '/home/danyal/NAaaS/district.csv' DELIMITER ',' CSV HEADER;


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
FROM '/home/danyal/NAaaS/tehsil.csv' DELIMITER ',' CSV HEADER;
CREATE TABLE union_council(
   id serial,
   name VARCHAR(50) PRIMARY KEY,
   coordinates json not null,
   tehsil varchar(50),
   CONSTRAINT fk_union FOREIGN KEY(tehsil) REFERENCES tehsil(name)
);
CREATE TABLE NEWS(
   id serial,
   header TEXT,
   details TEXT,
   link TEXT,
   focus_time TIMESTAMP,
   focus_location VARCHAR(50),
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

-- Sample Query
insert into NEWS(
      header,
      details,
      link,
      focus_time,
      focus_location,
      province
   )
VALUES(
      'header',
      'details 123',
      'http',
      '2022-05-16',
      'KARACHI',
      'SINDH'
   );