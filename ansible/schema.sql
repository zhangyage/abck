drop table if exists `hosts`;
create table if not exists `hosts` (
	`id` int(11) not null auto_increment,
	`alias` varchar(100) unique not null,
	`ip` varchar(100) unique not null,
	`ip2` varchar(100) default null,
	`port` int not null default 22,
	`remote_user` varchar(100) not null default 'root',
	/*`last_update` int(11),
	`info` varchar(10000),*/
	primary key (`id`)
);


drop table if exists `host_info`;
create table if not exists `host_info` (
	`host_id` int(11) unique not null,
	`last_update` int(11),
	/*server*/
	`system_vendor` varchar(20),
	`product_name` varchar(50),
	`product_serial` varchar(100),
	/*system*/
	`distribution` varchar(20),
	`distribution_version` varchar(10),
	`architecture` varchar(20),
	`kernel` varchar(50),
	/*cpu*/
	`processor_count` int,
	`processor_cores` int,
	`processor_vcpus` int,
	`processor_threads_per_core` int,
	`processor` varchar(500),
	/*swap*/
	`swaptotal_mb` int,
	`swapfree_mb` int,
	/*mem*/
	`memtotal_mb` int,
	`memfree_mb` int,
	/*disk*/
	`devices` varchar(2000),
	/*mount*/
	`mounts` varchar(2000),
	/*ip*/
	`default_ipv4` varchar(2000),
	`all_ipv4_addresses` varchar(1000),
	/*software*/
	`selinux` varchar(1000),
	`python_version` varchar(100),
	/*other*/
	`failed` varchar(1000),
	`msg` varchar(1000),
	primary key (`host_id`)
);


drop table if exists `groups`;
create table if not exists `groups` (
	`id` int(11) not null auto_increment,
	`name` varchar(100) unique not null,
	`description` varchar(500) default null,
	primary key (`id`)
);


drop table if exists `host_group`;
create table if not exists `host_group` (
	`id` int(11) not null auto_increment,
	`host_id` int(11) not null,
	`group_id` int(11) not null,
	primary key (`id`)
	/*primary key (`id`),
	CONSTRAINT `host_group_ibfk_1` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT `host_group_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `groups` (`id`) ON DELETE CASCADE ON UPDATE CASCADE*/
);


drop table if exists `jobs`;
create table if not exists `jobs` (
	`id` int(11) not null auto_increment,
	`started` int(11),
	`finished` int(11),
	`template_name` varchar(100),
	`args` varchar(1000),
	`status` varchar(1000),
	primary key (`id`)
);

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `active`	boolean DEFAULT 1,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `roles`;
CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `descript` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `routes`;
CREATE TABLE `routes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `path` varchar(50) NOT NULL,
  `descript` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `path` (`path`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `user_role`;
CREATE TABLE `user_role` (
  `user_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `role_route`;
CREATE TABLE `role_route` (
  `role_id` int(11) NOT NULL,
  `route_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/* admin:admin */
insert into users(username, password) value('admin', '$2a$12$hs17WPbfSkSDYUD6byATf.yF71ug74tD2Oq06bJLlWHs7hm88IN.m');
insert into roles(name) value('administrators');
insert into roles(name) value('users');
insert into routes(path) value('/*');
insert into user_role(user_id, role_id) value(1,1);
insert into role_route(role_id, route_id) value(1,1);
