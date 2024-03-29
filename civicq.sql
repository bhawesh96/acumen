-- drop table if exists `kodamr13_inquizitive`.players;

CREATE TABLE `kodamr13_inquizitive`.players (
  `user_id` BIGINT AUTO_INCREMENT,
  `name` VARCHAR(45),
  `reg_no` VARCHAR(45),
  `email` VARCHAR(45),
  `mobile` VARCHAR(10),
  `password` VARCHAR(200),
  `curr_ques` VARCHAR(20),
  PRIMARY KEY (`user_id`)
  );

CREATE TABLE `kodamr13_inquizitive`.`scores` (
  `user_id` BIGINT REFERENCES `players` (`user_id`),
  `points` varchar(20)
  );

CREATE TABLE `kodamr13_inquizitive`.`winner_rapid` (
  `user_id` BIGINT REFERENCES `players` (`user_id`),
  `rapid` INT,
  `time` VARCHAR(100),
  PRIMARY KEY (`user_id`)
  );

-- drop table if exists `kodamr13_inquizitive`.questions;

CREATE TABLE `kodamr13_inquizitive`.`questions` (
  `question_id` VARCHAR(20),
  `question` VARCHAR(400),
  `option1` VARCHAR(100),
  `option2` VARCHAR(100),
  `option3` VARCHAR(100),
  `option4` VARCHAR(100),
  `question_image` varchar(200),
  `answer` INT,
  `difficulty` INT,
  PRIMARY KEY (`question_id`));

CREATE TABLE `kodamr13_inquizitive`.`rapid` (
  `question_id` VARCHAR(20),
  `question` VARCHAR(400),
  `option1` VARCHAR(100),
  `option2` VARCHAR(100),
  `option3` VARCHAR(100),
  `option4` VARCHAR(100),
  `answer` INT,
  PRIMARY KEY (`question_id`));


-- CREATE PLAYER PROCEDURE
-- SIGNS UP A USER IF NOT ALREADY EXISTS


drop procedure if exists `insert_player_inquizitive`;
delimiter $$
create procedure `insert_player_inquizitive`(  IN p_name VARCHAR(45), IN p_regno VARCHAR(45), IN p_email VARCHAR(45),IN p_mobile VARCHAR(10), IN p_password VARCHAR(200))
begin
	if exists( SELECT user_id FROM players WHERE  reg_no = p_regno) 
    then select 'Not unique';
  else
	insert into players(name,reg_no,email,mobile,password,curr_ques, curr_rapid) values (p_name,p_regno,p_email,p_mobile,p_password,'1_1', 0);
    end if;
end$$
delimiter ;

-- call insert_player_inquizitive('rahul','150911122','abc@gmail.com','9008318345','rahul');

-- select * from players;

-- VALIDATE LOGIN PROCEDURE
-- RETURNS 0 IN THE VARIABLE PASSED IF NOT FOUND AND THE ID OF THE PLAYER IF FOUND



drop procedure if exists `validate_login_inquizitive`;
delimiter $$
create procedure `validate_login_inquizitive`(in e varchar(45), in p varchar(20))
begin
select * from players where email = e and password=p;
end
$$
delimiter ;


-- call validate_login_inquizitive('abc@gmail.com','rahul123');

drop trigger if exists `init_score_inquizitive`;
delimiter $$
create trigger init_score_inquizitive after insert on players
for each row
insert into scores values (New.user_id,'0', 0, 0, 0, 0);
$$
delimiter ;

-- update players set curr_ques='1_20', curr_rapid=1 where name='Bhawesh';



update questions set question="Compared to mild steel, cast iron has: 1.High compressive strength 2.high tensile strength 3.low compressive strength 4.low tensile strength" where question_id="4_11";

update questions set option2="surface tension is expressed in N/m" where question_id="3_16";

update rapid set option2="Intranet" where question_id="3_6";

