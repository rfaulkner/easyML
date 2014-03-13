-- Main Model schema defined for MySQL

CREATE TABLE `Users` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `fullname` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `date_join` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `date_create` (`date_join`),
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Models` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `uid` bigint(20) unsigned NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `date_create` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `date_create` (`date_create`),
) ENGINE=InnoDB DEFAULT CHARSET=latin1;