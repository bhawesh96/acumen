drop table `acumen`.players;

CREATE TABLE `acumen`.players (
  `user_id` BIGINT AUTO_INCREMENT,
  `name` VARCHAR(45),
  `reg_no` VARCHAR(45),
  `email` VARCHAR(45),
  `mobile` VARCHAR(10),
  `password` VARCHAR(200),
  `curr_ques` VARCHAR(20),
  PRIMARY KEY (`user_id`)
  );

CREATE TABLE `acumen`.`scores` (
  `user_id` BIGINT REFERENCES `players` (`user_id`),
  `points` varchar(20)
  );

CREATE TABLE `acumen`.`questions` (
  `ques_id` VARCHAR(20),
  `story` VARCHAR(400),
  `question` VARCHAR(400),
  `ques_image` varchar(200),
  `answer` VARCHAR(30),
  `hint` VARCHAR(500),
  PRIMARY KEY (`ques_id`));

---CREATE PLAYER PROCEDURE
---SIGNS UP A USER IF NOT ALREADY EXISTS


drop procedure if exists `insert_player_acumen`;
delimiter $$
create procedure `insert_player_acumen`(  IN p_name VARCHAR(45), IN p_regno VARCHAR(45), IN p_email VARCHAR(45),IN p_mobile VARCHAR(10), IN p_password VARCHAR(200))
begin
	if exists( SELECT user_id FROM players WHERE  reg_no = p_regno) 
    then select 'Not unique';
  else
	insert into players(name,reg_no,email,mobile,password,curr_ques) values (p_name,p_regno,p_email,p_mobile,p_password,'1');
    end if;
end$$
delimiter ;

call insert_player_acumen('rahul','150911122','abc@gmail.com','9008318345','rahul123');

select * from players;

---VALIDATE LOGIN PROCEDURE
---RETURNS 0 IN THE VARIABLE PASSED IF NOT FOUND AND THE ID OF THE PLAYER IF FOUND



drop procedure if exists `validate_login_acumen`;
delimiter $$
create procedure acumen.`validate_login_acumen`(in e varchar(45), in p varchar(20))
begin
select * from players where email = e and password=p;
end
$$
delimiter ;


call validate_login('abc@gmail.com','rahul123');

delimiter $$
create trigger init_score_acumen after insert on players
for each row
insert into scores values (New.user_id,'0');
$$
delimiter ;
