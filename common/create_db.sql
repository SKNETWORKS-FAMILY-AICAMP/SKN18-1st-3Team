# 사용자 조회 및 생성과 권한 설정
use mysql;
select * from user;

Create user 'chap1'@'%'
identified by '1234';

create database project_chap1;

grant all privileges
    on project_chap1.*
    to 'chap1'@'%';

use project_chap1;

-- # 테이블 생성
-- create table registered_car(
--     id int auto_increment primary key,
--     year int not null,
--     owner_name varchar(50) not null,
--     registration_date date not null
-- )

CREATE TABLE kia_faq (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(100),
    question TEXT,
    answer TEXT
);


create table registered_car(
    id INT AUTO_INCREMENT PRIMARY KEY,
    metrics VARCHAR(100),
    year INT,
    values TEXT
);

# 면적 당 등록 대수
create table register_electricity_car(
    id INT AUTO_INCREMENT PRIMARY KEY,
    region VARCHAR(100),
    register_by_region NUMERIC
);

# 면적 당 증가량
CREATE TABLE add_electricity_car (
    id INT AUTO_INCREMENT PRIMARY KEY,
    month DATE,  
    region VARCHAR(100) NOT NULL,
    add_by_region NUMERIC(6,2)  
);


create table fire_per(
    id INT AUTO_INCREMENT PRIMARY KEY,
    region VARCHAR(100) NOT NULL,
    cnt_fire NUMERIC(6,3) 
);


create table cal_by_region(
    id INT AUTO_INCREMENT PRIMARY KEY, 
    region VARCHAR(100) NOT NULL,
    cnt_building NUMERIC(6,2),
    cnt_popul NUMERIC(6,2)
)

create table charge_by_region(
    id INT AUTO_INCREMENT PRIMARY KEY, 
    region VARCHAR(100) NOT NULL,
    year INT,
    cnt_charge NUMERIC(6,2)
);


#############################################

create table income_tb(
    id INT AUTO_INCREMENT PRIMARY KEY, 
    region VARCHAR(100) NOT NULL,
    year INT,
    income INT
);


create table industry_tb(
    id INT AUTO_INCREMENT PRIMARY KEY, 
    region VARCHAR(100) NOT NULL,
    industry_category VARCHAR(50),
    industry_code VARCHAR(10),
    year INT,
    number_of_employees INT
);


create table population_tb(
    id INT AUTO_INCREMENT PRIMARY KEY, 
    region VARCHAR(100) NOT NULL,
    gender VARCHAR(50),
    age VARCHAR(10),
    year INT,
    value INT
);


create table total_tb(
    id INT AUTO_INCREMENT PRIMARY KEY, 
    region VARCHAR(100) NOT NULL,
    year INT,
    total INT
);


create table vehicle_tb(
    id INT AUTO_INCREMENT PRIMARY KEY, 
    region VARCHAR(100) NOT NULL,
    gender VARCHAR(50),
    age VARCHAR(10),
    year INT,
    value INT
);