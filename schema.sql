drop table if exists user;
create table user (
  user_id integer primary key autoincrement,
  username text not null,
  email text not null,
  pw_hash text not null,
  is_admin integer not null default 0
);
drop table if exists blog_post;
create table blog_post (
  post_id integer primary key autoincrement,
  title text not null,
  content text not null,
  photos text,
  videos text,
  posted_at datetime not null default CURRENT_TIMESTAMP,
  edited_at datetime,
  poster_id integer not null,
  foreign key (poster_id) references user(user_id)
);
drop table if exists comment;
create table comment (
  comment_id integer primary key autoincrement,
  content text not null,
  posted_at datetime not null default CURRENT_TIMESTAMP,
  edited_at datetime,
  commenter_id integer,
  foreign key (commenter_id) references user(user_id)
);
drop table if exists private_message;
create table private_message (
  message_id integer primary key autoincrement,
  name text,
  message text not null,
  email text,
  sent_at datetime not null default CURRENT_TIMESTAMP,
  received_at datetime,
  user_id integer,
  foreign key (user_id) references user(user_id)
);
