#CREATE A NEW USER TO MYSQL DB - LOCAL USER
CREATE USER '[machineName]'@localhost IDENTIFIED WITH auth_socket; #BY 'GET_THE_PASSWORD'

CREATE USER '[WRITE_HIS_NAME]'@*.*.*.* WITH mysql_native_password BY 'GET_THE_PASSWORD';

GRANT ALL PRIVILEGES ON ["database_name"].* TO '[WRITE_HIS_NAME]'@*.*.*.* WITH GRANT OPTION;

FLUSH PRIVILEGES;

#TO CREATE DATABASE
CREATE DATABASE railDB;

#TO CRETE TABLES INT HE DATABASE
USE railDB;


#CREATE ADMIN TABLE TO STORE ADMIN DETAILS
CREATE TABLE adminDetails(
	slno INT NOT NULL AUTO_INCREMENT,
	admin_name VARCHAR(50) NOT NULL,
	sex CHAR(1) NOT NULL,
	date_of_birth DATE,
	date_of_account_creation DATE,
	phone_number VARCHAR(10),
	email VARCHAR(50) NOT NULL,
	password VARCHAR(20) NOT NULL,
	admin_id VARCHAR(20),
	PRIMARY KEY (slno));

#alter table adminDetails MODIFY COLUMN admin_name VARCHAR(50);

INSERT INTO adminDetails(admin_name,sex,date_of_birth,date_of_account_creation,phone_number,email,password,admin_id) 
	VALUES("Prof.Mahadevaiah Siddaiah","M","1961-12-21","2018-10-17","9845796186","railatsk@gmail.com","rail123",NULL);



#CREATE STUDENT TABLE TO STORE ALL THE BASIC DATA
CREATE TABLE students(
	slno INT NOT NULL AUTO_INCREMENT,
	student_name VARCHAR(50) NOT NULL,
	sex CHAR(1) NOT NULL,
	date_of_birth DATE,
	date_of_account_creation DATE NOT NULL,
	phone_number VARCHAR(10) NOT NULL,
	email VARCHAR(30) NOT NULL,
	password VARCHAR(20) NOT NULL,
	rail_id VARCHAR(11) NOT NULL,
	usn VARCHAR(11) NOT NULL,
	branch VARCHAR(5) NOT NULL,
	year_of_joining_rail YEAR(4) NOT NULL,
	associated_team VARCHAR(20),
	login_status VARCHAR(3) NOT NULL,
	component_status VARCHAR(3) NOT NULL,
	PRIMARY KEY (slno));

#alter table students MODIFY COLUMN email VARCHAR(50);

INSERT INTO students(student_name,sex,date_of_birth,date_of_account_creation,phone_number,email,password,rail_id,usn,branch,year_of_joining,associated_team,login_status,component_status) 
	VALUES("Tarun Gopalkrishna A","M","1999-05-1","2018-10-17","8296177426","tarungopalkrishna@gmail.com","tarun1999","RSK17CS036","1SK17CS036","CSE","2017","A","NO","NO");


#CREATE STUDENT_ATTENDENCE TABLE TO TRACK STUDENTS ATTENDANCE
CREATE TABLE studentsAttendence(
	slno INT NOT NULL AUTO_INCREMENT,
	student_name VARCHAR(50) NOT NULL,
	rail_id VARCHAR(20),
	time_in DATETIME,
	time_out DATETIME,
	associated_team CHAR(1),
	cause TEXT,
	PRIMARY KEY (slno)
	);

INSERT INTO studentsAttendence (student_name,rail_id,time_in,time_out,associated_team,cause) 
	VALUES("Tarun Gopalkrishna A","RSK17CS036","2018-01-21 10:09:51","2018-01-21 05:30:00","A","SIH");

CREATE TABLE testtable(
	slno INT NOT NULL AUTO_INCREMENT,
	testInformation TEXT,PRIMARY KEY (slno));


INSERT INTO current_students(
	rail_id,
	student_name,
	gender,
	date_of_birth,
	time_of_joining_rail,
	phone_number,
	email,
	associated_team,
	branch,
	usn,
	current_highest_role
) 
VALUES(
	'RSK17CS036',
	'TGK',
	'M',
	'1999-05-01',
	'1999-05-01 12:00:00',
	'8956233145',
	'TGK@TGK.COM',
	'1',
	'CS',
	'1SK17CS036',
	'member'
)




delete from current_students where CHAR_LENGTH(rail_id) = 9;
delete from current_students where email = 'NULL';