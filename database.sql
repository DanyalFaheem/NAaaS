CREATE TABLE province(
   id serial,
   name VARCHAR(50) PRIMARY KEY,
   coordinates json not null,
);

COPY province(name, coordinates)
FROM '/home/danyal/NAaaS/province.csv'
DELIMITER ','
CSV HEADER;

insert into province(name, coordinates)
values('FATA', '{}')

CREATE TABLE district(
   id serial,
   name VARCHAR(50) PRIMARY KEY,
   coordinates json not null,
   province varchar(50),
   CONSTRAINT fk_district
      FOREIGN KEY(province) 
	  REFERENCES province(name)
);

COPY district(province, name, coordinates)
FROM '/home/danyal/NAaaS/district.csv'
DELIMITER ','
CSV HEADER;

insert into district(province, name, coordinates)
select name, 'HATTIAN', coordinates from province where name='AZAD KASHMIR';

insert into district(province, name, coordinates)
select name, 'KACHHI(BOLAN)', coordinates from province where name='BALOCHISTAN';

insert into district(province, name, coordinates)
select name, 'DISPUTED TERRITORY', coordinates from province where name='INDIAN OCCUPIED KASHMIR';

insert into district(province, name, coordinates)
select name, 'NORTH WAZIRISTAN AGENCY', coordinates from province where name='KHYBER PAKHTUNKHWA';

insert into district(province, name, coordinates)
select name, 'SOUTH WAZIRISTAN AGENCY', coordinates from province where name='KHYBER PAKHTUNKHWA';

insert into district(province, name, coordinates)
select name, 'DERA ISMAIL KHAN', coordinates from province where name='KHYBER PAKHTUNKHWA';

insert into district(province, name, coordinates)
select name, 'KOHISTAN', coordinates from province where name='KHYBER PAKHTUNKHWA';

insert into district(province, name, coordinates)
select province, 'NOWSHERA_', coordinates from district where name='NOWSHERA';

insert into district(province, name, coordinates)
select province, 'NOWSHEHRA_', coordinates from district where name='NOWSHERA';

insert into district(province, name, coordinates)
select province, 'TORGHER', coordinates from district where name='TORDHER';



CREATE TABLE tehsil(
   id serial,
   name VARCHAR(50) PRIMARY KEY,
   coordinates json not null,
   district varchar(50),
   CONSTRAINT fk_tehsil
      FOREIGN KEY(district) 
	  REFERENCES district(name)
);

COPY tehsil(district, name, coordinates)
FROM '/home/danyal/NAaaS/tehsil.csv'
DELIMITER ','
CSV HEADER;