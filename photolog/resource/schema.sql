drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title string not null,
  text string not null
);

drop table if exists users;
create table users (
  id integer primary key autoincrement,
  username string not null,
  password string not null
);