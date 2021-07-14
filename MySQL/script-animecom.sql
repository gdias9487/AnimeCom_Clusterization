-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema animecom
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema animecom
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `animecom` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `animecom` ;

-- -----------------------------------------------------
-- Table `animecom`.`Animes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `animecom`.`Animes` (
  `uid` INT NOT NULL AUTO_INCREMENT,
  `title` MEDIUMTEXT NOT NULL,
  `synopsis` LONGTEXT NULL,
  `genre` MEDIUMTEXT NOT NULL,
  `aired_start` VARCHAR(45) NULL,
  `aired_finish` VARCHAR(45) NULL,
  `episodes` INT NULL,
  `img_url` MEDIUMTEXT NULL,
  `link` MEDIUMTEXT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE INDEX `uid_UNIQUE` (`uid` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `animecom`.`Evaluation`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `animecom`.`Evaluation` (
  `anime_uid` INT NOT NULL,
  `members` INT NULL,
  `popularity` INT NULL,
  `ranked` INT NULL,
  `score` INT NULL,
  PRIMARY KEY (`anime_uid`),
  UNIQUE INDEX `anime_uid_UNIQUE` (`anime_uid` ASC) VISIBLE,
  CONSTRAINT `fk_Evalution_Animes`
    FOREIGN KEY (`anime_uid`)
    REFERENCES `animecom`.`Animes` (`uid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `animecom`.`Profiles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `animecom`.`Profiles` (
  `uid` INT NOT NULL AUTO_INCREMENT,
  `user_name` VARCHAR(45) NULL,
  `email` VARCHAR(45) NOT NULL,
  `pass` VARCHAR(45) NOT NULL,
  `gender` VARCHAR(10) NULL,
  `birthday` VARCHAR(45) NULL,
  `phone` VARCHAR(45) NULL,
  UNIQUE INDEX `profile_UNIQUE` (`uid` ASC) VISIBLE,
  PRIMARY KEY (`uid`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `animecom`.`Favorites`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `animecom`.`Favorites` (
  `user_uid` INT NOT NULL,
  `anime_uid` INT NOT NULL,
  PRIMARY KEY (`user_uid`, `anime_uid`),
  INDEX `fk_Favorites_Animes1_idx` (`anime_uid` ASC) VISIBLE,
  CONSTRAINT `fk_Favorites_Profiles1`
    FOREIGN KEY (`user_uid`)
    REFERENCES `animecom`.`Profiles` (`uid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Favorites_Animes1`
    FOREIGN KEY (`anime_uid`)
    REFERENCES `animecom`.`Animes` (`uid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;


-- Criando usuário que está default na aplicação
Use mysql;
DROP USER IF EXISTS `animecom`@`localhost`;
CREATE USER `animecom`@`localhost` IDENTIFIED BY '12345678';
GRANT ALL ON animecom.* TO `animecom`@`localhost`;
FLUSH PRIVILEGES;


Use animecom;
-- Criando procedures
DELIMITER $$
CREATE PROCEDURE animecom.stp_profiles_incluir(
IN user_name MEDIUMTEXT,
IN email LONGTEXT,
IN pass MEDIUMTEXT,
IN gender VARCHAR(45) ,
IN birthday VARCHAR(45),
IN phone INT)

BEGIN
	CALL animecom.stp_profiles_validar(email,pass);
  
	INSERT INTO animecom.profiles 
  VALUES (null,user_name,email,pass,gender,birthday,phone);
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE animecom.stp_profiles_validar(
IN email VARCHAR(45),
IN pass VARCHAR(45))
BEGIN
	-- validação--
	IF email IS NULL THEN
		SIGNAL SQLSTATE '45001' SET MESSAGE_TEXT = 'Email is mandatory!';
	END IF;
	IF pass IS NULL THEN
		SIGNAL SQLSTATE '45001' SET MESSAGE_TEXT = 'Password is mandatory!' ;
	END IF;
END $$
DELIMITER ;


-- Criando trigger
DELIMITER $$    
CREATE TRIGGER trg_profiles_deletar BEFORE DELETE ON animecom.profiles FOR EACH ROW
	BEGIN
		DELETE FROM animecom.favorites WHERE user_uid = OLD.uid;
	END$$

DELIMITER ;