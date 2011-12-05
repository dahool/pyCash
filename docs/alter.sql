ALTER TABLE `loan` ADD `remain` DECIMAL( 19, 2 ) NULL ;
ALTER TABLE `loan` ADD INDEX ( `remain` ) ;

