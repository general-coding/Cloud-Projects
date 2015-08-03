#appcfg.py -A sinuous-photon-93704 update appengine-try-php

create database cloud6;

use cloud6;

create table users(
username varchar(50),
password varchar(32),
fullname varchar(50),
email    varchar(50)
);

select * from users;

create table data1(
station   varchar(50),
elevation varchar(50),
latitude  varchar(50),
longitude varchar(50),
date      varchar(50),
hpcp      varchar(50)
);

select * from data1;

create table data2(
season varchar(20),
prec   varchar(20)
);

select * from data2;