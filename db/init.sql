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

INSERT INTO user_status VALUES
    (1,'A','Active'),
    (2,'I','Inactive')
 ;

INSERT INTO user_type VALUES
    (1,'U','Regular User'),
    (2,'A','Admin'),
    (3,'S','Support')
 ;

INSERT INTO app_roles VALUES
    (1,'U','Regular User'),
    (2,'A','Admin'),
    (3,'S','Support')
 ;