-- database create DDL
CREATE DATABASE final_project_db;
use final_project_db;

-- table create DDL
CREATE TABLE IF NOT EXISTS app_roles (
    `id` INT AUTO_INCREMENT,
    `code` VARCHAR(5) CHARACTER SET utf8,
    `description` VARCHAR(50) CHARACTER SET utf8,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS user_type (
    `id` INT AUTO_INCREMENT,
    `code` VARCHAR(5) CHARACTER SET utf8,
    `description` VARCHAR(50) CHARACTER SET utf8,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS user_status (
    `id` INT AUTO_INCREMENT,
    `code` VARCHAR(5) CHARACTER SET utf8,
    `description` VARCHAR(50) CHARACTER SET utf8,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS user_address (
    `id` INT AUTO_INCREMENT,
    `type` VARCHAR(10) CHARACTER SET utf8,
    `line_1` VARCHAR(50) CHARACTER SET utf8,
    `line_2` VARCHAR(50) CHARACTER SET utf8,
    `city` VARCHAR(25) CHARACTER SET utf8,
    `state` VARCHAR(25) CHARACTER SET utf8,
    `zip_code` VARCHAR(10) CHARACTER SET utf8,
    `email` VARCHAR(100) CHARACTER SET utf8,
    `phone` VARCHAR(10) CHARACTER SET utf8,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS app_users (
    `id` INT AUTO_INCREMENT,
    `login_name` VARCHAR(10) CHARACTER SET utf8,
    `password` VARCHAR(25) CHARACTER SET utf8,
    `first_name` VARCHAR(50) CHARACTER SET utf8,
    `last_name` VARCHAR(50) CHARACTER SET utf8,
    `role_id` INT not null references app_roles(id) ,
    `type_id` INT not null references user_type(id) ,
    `status_id` INT not null references user_status(id) ,
    `address_id` INT not null references user_address(id),
    PRIMARY KEY (`id`)
);

-- data population DML for 100 records
/*
INSERT INTO tblCities VALUES
    (1,41,5,59,'N',80,39,0,'W','Youngstown','OH'),
    (2,42,52,48,'N',97,23,23,'W','Yankton','SD'),
    (3,46,35,59,'N',120,30,36,'W','Yakima','WA'),
    (4,42,16,12,'N',71,48,0,'W','Worcester','MA'),
    (5,43,37,48,'N',89,46,11,'W','Wisconsin Dells','WI'),
    (6,36,5,59,'N',80,15,0,'W','Winston-Salem','NC'),
    (7,49,52,48,'N',97,9,0,'W','Winnipeg','MB'),
    (8,39,11,23,'N',78,9,36,'W','Winchester','VA'),
    (9,34,14,24,'N',77,55,11,'W','Wilmington','NC'),
    (10,39,45,0,'N',75,33,0,'W','Wilmington','DE'),
 ;*/
