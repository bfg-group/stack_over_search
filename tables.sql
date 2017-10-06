CREATE TABLE `requests` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`request` VARCHAR(100) NOT NULL COLLATE 'latin1_swedish_ci',
	`reqtime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`),
	UNIQUE INDEX `request` (`request`)
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=311
;


CREATE TABLE `requests_data` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`request` VARCHAR(50) NULL DEFAULT NULL,
	`title` VARCHAR(200) NULL DEFAULT NULL,
	`author` TEXT NULL,
	`link` TEXT NULL,
	`create_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`last_activity` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`),
	UNIQUE INDEX `title` (`title`)
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=13529
;
