-- Main Model schema defined for MySQL

CREATE TABLE `Models` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `date_create` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `date_create` (`date_create`),
) ENGINE=InnoDB DEFAULT CHARSET=latin1;