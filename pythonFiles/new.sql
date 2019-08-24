DROP DATABASE testdatabase;

CREATE DATABASE testdatabase;

USE testdatabase;


-- SHOULD THE ENTRIES IN THE cur_studs BE PRESENT IN all_studs AT THE START OR SHOULD IT ADDED TO
-- all_studs WHEN DELETED FROM cur_studs?
-- Should I create a table that contains all the unique ID's of everyone associated with RAIL?

CREATE TABLE all_studs(
	/* Removed slno	*/
	`usn` CHAR(10) NOT NULL,						/* Debate whether usn or rail_id must be PRIMARY KEY */
	`rail_id` CHAR(10) NOT NULL,
	`student_name` VARCHAR(100) NOT NULL,			/* Is 100 too much? */
	`gender` CHAR(1) NOT NULL,
	`date_of_birth` DATE NOT NULL,
	`time_of_joining_rail` DATETIME DEFAULT NOW(),	/* Should I add the DEFAULT condition? */
	`phone_number` CHAR(10) NOT NULL,
	`email` VARCHAR(40) NOT NULL,
	`associated_team` VARCHAR(20) NOT NULL,			/* Why does this have 20 characters? */
	`projects_done` INT UNSIGNED DEFAULT 0,
	`branch` VARCHAR(5) NOT NULL,					/* I guess for this varchar(3) is fine */
	`time_in_rail` TIME	NOT NULL,					/* Debate on which format must this be in */
	PRIMARY KEY(`usn`)
);

CREATE TABLE cur_studs(
	`usn` CHAR(10) NOT NULL PRIMARY KEY,			/* Debate whether usn or rail_id must be PRIMARY KEY */
	`rail_id` CHAR(10) NOT NULL,
	`student_name` VARCHAR(100) NOT NULL,			/* Is 100 too much? */
	`gender` CHAR(1) NOT NULL,
	`date_of_birth` DATE NOT NULL,
	`time_of_joining_rail` DATETIME DEFAULT NOW(),	/* Should I add the DEFAULT condition? */
	`phone_number` VARCHAR(10) NOT NULL,
	`email` VARCHAR(40) NOT NULL,
	`associated_team` VARCHAR(20) NOT NULL,			/* Why does this have 20 characters? becuase he can be associated with more than one project */
	`projects_done` INT UNSIGNED DEFAULT 0,
	`branch` VARCHAR(5) NOT NULL,					/* I guess VARCHAR(3) is fine for this */
	`login_status` BOOLEAN DEFAULT 0,
	`component_status` BOOLEAN DEFAULT 0,
	`most_recent_login` DATETIME DEFAULT NULL,
	`time_in_rail` VARCHAR(20) DEFAULT NULL,		/* Debate on which format must this be in */
	`current_role` VARCHAR(20) NOT NULL,
	INDEX(`rail_id`)
);

-- CREATE TABLE all_teams(
	-- ADD A COLUMN WITH A PRIMARY KEY
--	`team_hash` CHAR(8) NOT NULL PRIMARY KEY,		/* Probably generated as a hash of concatination of usn's/rsn's with current datetime stamp */
--	`team_letter` CHAR(1) NOT NULL,
--	`team_name` CHAR(30) NOT NULL,
--	`associated_projects` VARCHAR(100) NOT NULL,
--	`number_of_members` TINYINT UNSIGNED NOT NULL,
--	`team_members` VARCHAR(55) NOT NULL,			/* Supports only upto 4 members in a team */
--	`date_of_team_creation` DATETIME DEFAULT NOW()
-- );

CREATE TABLE cur_teams(
	-- ADD A COLUMN WITH A PRIMARY KEY
	`team_hash` CHAR(8) NOT NULL PRIMARY KEY,		/* Probably generated as a hash of concatination of usn's/rsn's with current datetime stamp */
	`team_letter` CHAR(1) NOT NULL,
	`team_name` CHAR(30) NOT NULL,
	`associated_projects` VARCHAR(100) NOT NULL,
	`number_of_members` TINYINT UNSIGNED NOT NULL,
	`team_members` VARCHAR(55) NOT NULL,			/* Supports only upto 4 members in a team */
	`date_of_team_creation` DATETIME DEFAULT NOW()
);

CREATE TABLE all_projs(
	`team_hash` CHAR(8) NOT NULL PRIMARY KEY,
	`project_name` VARCHAR(30) NOT NULL,
	`associated_team` CHAR(1) NOT NULL,
	`project_description` VARCHAR(200) NOT NULL,
	`mentor` VARCHAR(50) DEFAULT NULL,
	`team_lead` VARCHAR(50) NOT NULL,
	`guide` VARCHAR(50) DEFAULT NULL,
	`idea_by` VARCHAR(50) NOT NULL,
	`type_of_project` VARCHAR(30) NOT NULL,
	`expected_duration` VARCHAR(20) NOT NULL,
	`date_start` DATETIME NOT NULL DEFAULT NOW(),
	`date_end` DATETIME DEFAULT NULL,
	`status` VARCHAR(20) NOT NULL,
	`priority` VARCHAR(20) NOT NULL,
	`technology_stack` VARCHAR(50) NOT NULL,
	FOREIGN KEY(`team_hash`) REFERENCES cur_teams(`team_hash`)
);

CREATE TABLE cur_projs(
	`team_hash` CHAR(8) NOT NULL PRIMARY KEY,
	`project_name` VARCHAR(30) NOT NULL,
	`associated_team` CHAR(1) NOT NULL,
	`project_description` VARCHAR(200) NOT NULL,
	`number_of_members` TINYINT UNSIGNED NOT NULL,
	`mentor` VARCHAR(50),
	`team_lead` VARCHAR(50) NOT NULL,
	`guide` VARCHAR(50),
	`idea_by` VARCHAR(50) NOT NULL,
	`type_of_project` VARCHAR(30) NOT NULL,
	`expected_duration` VARCHAR(20) NOT NULL,
	`date_start` DATETIME NOT NULL,
	`date_end` DATETIME,
	`status` VARCHAR(20) NOT NULL,
	`priority` VARCHAR(20) NOT NULL,
	`technology_stack` VARCHAR(50) NOT NULL,
	FOREIGN KEY(`team_hash`) REFERENCES cur_teams(`team_hash`)
);

CREATE TABLE attendence(
	`rail_id` VARCHAR(11) NOT NULL,
	`team_login` CHAR(8) NOT NULL ,
	`time_in` DATETIME NOT NULL DEFAULT NOW(),
	`time_out` DATETIME DEFAULT NULL,
	`time_spent` TIME DEFAULT NULL,
	`purpose` VARCHAR(50) NOT NULL,
	FOREIGN KEY(`rail_id`) REFERENCES cur_studs(`rail_id`),
	FOREIGN KEY(`team_login`) REFERENCES cur_teams(`team_hash`)
);

CREATE TABLE all_admin(
	-- `slno` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`admin_name` VARCHAR(50) NOT NULL,
	`admin_id` VARCHAR(10) PRIMARY KEY,
	`date_of_birth` DATETIME DEFAULT NULL,
	`date_of_account_creation` DATETIME NOT NULL,
	`phone_number` CHAR(10) NOT NULL,
	`email` VARCHAR(50) NOT NULL,
	`password` VARCHAR(20) NOT NULL
);

CREATE TABLE cur_admin(
	-- `slno` INT(3) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`admin_name` VARCHAR(50) NOT NULL,
	`admin_id` VARCHAR(10) PRIMARY KEY,
	`date_of_birth` DATETIME DEFAULT NULL,
	`date_of_account_creation` DATETIME NOT NULL,
	`phone_number` CHAR(10) NOT NULL,
	`email` VARCHAR(50) NOT NULL,
	`password` VARCHAR(20) NOT NULL
);

CREATE TABLE admin_attendence(
	`admin_id` VARCHAR(11) NOT NULL,
	`time_in` DATETIME NOT NULL DEFAULT NOW(),
	`time_out` DATETIME DEFAULT NULL,
	`time_spent` TIME DEFAULT NULL,
	FOREIGN KEY(`admin_id`) REFERENCES cur_admin(`admin_id`)
);

CREATE TABLE events(
	-- `slno` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`rail_id` CHAR(10) NOT NULL,
	`time_of_event` DATETIME PRIMARY KEY,
	`type` VARCHAR(30) NOT NULL,
	`topic` VARCHAR(70) NOT NULL,
	`description` VARCHAR(200) NOT NULL,
	`domain` VARCHAR(20) NOT NULL,
	`member_type` VARCHAR(30) NOT NULL,
	`duraiton` TIME NOT NULL,
	`by_who` VARCHAR(30) NOT NULL,
	`phone_number` CHAR(10),
	`email` VARCHAR(50),
	`number_of_attendes` INT(3) NOT NULL
	-- FOREIGN KEY
);

CREATE TABLE components(
	-- `slno` INT(3) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`component_id` CHAR(10) PRIMARY KEY,
	`component_name` VARCHAR(55) NOT NULL,
	`date_of_procurement` DATE,
	`if_kit` VARCHAR(3) DEFAULT 'NO',
	`associated_colour` VARCHAR(20) NOT NULL,
	`number_of_times_issued` INT UNSIGNED DEFAULT '0',
	`group` VARCHAR(15) NOT NULL,
	`component_status` VARCHAR(3) DEFAULT 'YES',
	`most_recent_issue` DATETIME,
	`total_time_of_use` VARCHAR(20)
	-- YOU NEED TO HAD THE HASH VALUE TO THIS
);

CREATE TABLE kits(
	-- `slno` INT(3) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`kit_id` CHAR(10) PRIMARY KEY,
	`component_id` CHAR(10),
	`number_of_sub_compoenents` INT(3) UNSIGNED NOT NULL,
	`sub_components` BLOB NOT NULL
);

CREATE TABLE iss_compnts(
	-- `slno` INT(3) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`component_id` CHAR(10) NOT NULL,
	`issued_to` VARCHAR(20) NOT NULL,
	`associated_team` VARCHAR(20) NOT NULL,
	`time_of_issue` DATETIME DEFAULT NOW(),
	`time_of_return` DATETIME,
	`time_of_use` VARCHAR(20), 						/* Why have I made this varchar */
	FOREIGN KEY(`component_id`) REFERENCES components(`component_id`)
);

CREATE TABLE rail_donors(
	-- `slno` INT(3) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`rail_id` CHAR(10) NOT NULL,
	`amount` INT NOT NULL,
	`time` DATETIME DEFAULT NOW(),
	`reason` VARCHAR(20) NOT NULL
);

CREATE TABLE rail_expenses(
	-- `slno` INT(3) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`item_purchased` VARCHAR(25) NOT NULL,
	`quantity` INT DEFAULT 1,
	`date_of_purchase` DATE NOT NULL,
	`component_id` CHAR(10) NOT NULL,
	`company` VARCHAR(20),
	`cost` INT NOT NULL,
	FOREIGN KEY(`component_id`) REFERENCES components(`component_id`)	/* Is this nencessary? */
);



