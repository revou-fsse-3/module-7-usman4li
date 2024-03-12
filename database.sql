create database module7_assignment;
use module7_assignment;

create table users(
	id int primary key auto_increment,
    email varchar(191) not null,
    name varchar(191) not null,
    password varchar(191) not null,
    created_at timestamp default current_timestamp
);
drop table users;
create table product (
	id int auto_increment primary key,
    email varchar(100) not null,
    price int not null,
    description varchar(100) not null,
    created_at timestamp not null
);

drop table product;
create table product_review (
	id int auto_increment primary key,
    product_id int not null,
    email varchar(100) not null,
    rating int,
    review_content text,
    created_at timestamp
);
drop table product_review;

Select * from product;
Select * from users;
alter table product modify column created_at timestamp default current_timestamp;
alter table users add column role varchar(191) null default null