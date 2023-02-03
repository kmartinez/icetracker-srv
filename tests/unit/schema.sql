-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: iceland
-- ------------------------------------------------------
-- Server version	8.0.31

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `iceland`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `iceland` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `iceland`;

--
-- Table structure for table `accelerometer_readings`
--

DROP TABLE IF EXISTS `accelerometer_readings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accelerometer_readings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `device_id` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL,
  `pitch` float NOT NULL,
  `roll` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_id` (`device_id`,`timestamp`),
  CONSTRAINT `accelerometer_readings_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=26751 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `api_keys`
--

DROP TABLE IF EXISTS `api_keys`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_keys` (
  `id` int NOT NULL AUTO_INCREMENT,
  `api_key` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `conductivity_readings`
--

DROP TABLE IF EXISTS `conductivity_readings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `conductivity_readings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `device_id` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL,
  `value` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_id` (`device_id`,`timestamp`),
  CONSTRAINT `conductivity_readings_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=26378 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `delay_data`
--

DROP TABLE IF EXISTS `delay_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `delay_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `device_id` varchar(255) NOT NULL,
  `reading_timestamp` datetime NOT NULL,
  `received_timestamp` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_id` (`device_id`,`reading_timestamp`)
) ENGINE=InnoDB AUTO_INCREMENT=21080 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `devices`
--

DROP TABLE IF EXISTS `devices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `devices` (
  `id` varchar(255) NOT NULL DEFAULT '',
  `location_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `location_id` (`location_id`),
  CONSTRAINT `devices_ibfk_1` FOREIGN KEY (`location_id`) REFERENCES `locations` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `file_revisions`
--

DROP TABLE IF EXISTS `file_revisions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `file_revisions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `device_id` varchar(255) NOT NULL,
  `name` text NOT NULL,
  `md5sum` varchar(32) NOT NULL,
  `computed` varchar(32) NOT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `device_id` (`device_id`),
  CONSTRAINT `file_revisions_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=148 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `geophone_data`
--

DROP TABLE IF EXISTS `geophone_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `geophone_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `event_id` int NOT NULL,
  `sample_number` int NOT NULL,
  `x` int NOT NULL,
  `y` int NOT NULL,
  `z` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `event_id` (`event_id`),
  CONSTRAINT `geophone_data_ibfk_1` FOREIGN KEY (`id`) REFERENCES `geophone_events` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `geophone_events`
--

DROP TABLE IF EXISTS `geophone_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `geophone_events` (
  `id` int NOT NULL AUTO_INCREMENT,
  `device_id` varchar(255) NOT NULL,
  `RTC_counter` float NOT NULL,
  `RTC_current` float NOT NULL,
  `RTC_reference` float NOT NULL,
  `missed_samples` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `device_id` (`device_id`,`RTC_counter`,`RTC_current`,`RTC_reference`),
  CONSTRAINT `geophone_events_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `gps_measurements_geod`
--

DROP TABLE IF EXISTS `gps_measurements_geod`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gps_measurements_geod` (
  `id` int NOT NULL AUTO_INCREMENT,
  `device_id` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL,
  `latitude` float(11,8) NOT NULL,
  `longitude` float(11,8) NOT NULL,
  `height` float(11,8) NOT NULL,
  `sigN` float(7,5) NOT NULL,
  `sigE` float(7,5) NOT NULL,
  `sigH` float(7,5) NOT NULL,
  `RMS` float(7,5) NOT NULL,
  `BF` int NOT NULL,
  `notFixed` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_id_2` (`device_id`,`timestamp`),
  KEY `device_id` (`device_id`),
  CONSTRAINT `gps_measurements_geod_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1237912 DEFAULT CHARSET=latin1 COMMENT='All units distances converted to m';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `gps_measurements_neu`
--

DROP TABLE IF EXISTS `gps_measurements_neu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gps_measurements_neu` (
  `id` int NOT NULL AUTO_INCREMENT,
  `device_id` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL,
  `dNorth` float(8,4) NOT NULL,
  `dNorth_err` float(6,5) NOT NULL,
  `dEast` float(8,4) NOT NULL,
  `dEast_err` float(6,5) NOT NULL,
  `dHeight` float(8,4) NOT NULL,
  `dHeight_err` float(6,5) NOT NULL,
  `RMS` float(7,6) NOT NULL,
  `BF` int NOT NULL,
  `notFixed` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_id_2` (`device_id`,`timestamp`),
  KEY `device_id` (`device_id`),
  KEY `timestamp` (`timestamp`),
  CONSTRAINT `gps_measurements_neu_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1272596 DEFAULT CHARSET=latin1 COMMENT='All units distances converted to m';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `gps_measurements_ppp`
--

DROP TABLE IF EXISTS `gps_measurements_ppp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gps_measurements_ppp` (
  `id` int NOT NULL AUTO_INCREMENT,
  `dir` varchar(3) NOT NULL,
  `device_id` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL,
  `NSV` int NOT NULL,
  `GDOP` float NOT NULL,
  `SDC` float NOT NULL,
  `SDP` float NOT NULL,
  `DLAT` float NOT NULL COMMENT 'm',
  `DLON` float NOT NULL COMMENT 'm',
  `DHGT` float NOT NULL COMMENT 'm',
  `CLK` float NOT NULL COMMENT 'ns',
  `TZD` float NOT NULL COMMENT 'm',
  `SLAT` float NOT NULL COMMENT 'm',
  `SLON` float NOT NULL COMMENT 'm',
  `SHGT` float NOT NULL COMMENT 'm',
  `SCLK` float NOT NULL COMMENT 'ns',
  `STZD` float NOT NULL COMMENT 'm',
  `longitude` float(11,4) NOT NULL,
  `latitude` float(11,4) NOT NULL,
  `HGT` float NOT NULL COMMENT 'm',
  `CGVD28` varchar(4) NOT NULL,
  `northing` float NOT NULL COMMENT 'm',
  `easting` float NOT NULL COMMENT 'm',
  `zone` int NOT NULL,
  `scale_factor` float NOT NULL,
  `hemi` varchar(1) NOT NULL,
  `AM` int NOT NULL,
  `combined_scale_factor` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_id` (`device_id`,`timestamp`),
  KEY `device_id_2` (`device_id`),
  CONSTRAINT `gps_measurements_ppp_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9652 DEFAULT CHARSET=latin1 COMMENT='Contains data from the .pos file returned from the canadian ';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `gps_readings`
--

DROP TABLE IF EXISTS `gps_readings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gps_readings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `location` varchar(11) NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime DEFAULT NULL,
  `no_sats` int DEFAULT NULL,
  `filename` varchar(50) NOT NULL,
  `processed` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_readings` (`location`,`start_time`),
  KEY `location` (`location`),
  KEY `start_time` (`start_time`),
  KEY `end_time` (`end_time`),
  KEY `no_sats` (`no_sats`),
  KEY `processed` (`processed`),
  CONSTRAINT `gps_readings_ibfk_1` FOREIGN KEY (`location`) REFERENCES `devices` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=19517 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `gw12_data_converted`
--

DROP TABLE IF EXISTS `gw12_data_converted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gw12_data_converted` (
  `device` int DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `temperature` decimal(16,4) DEFAULT NULL,
  `pressure_bar` decimal(16,4) DEFAULT NULL,
  `depth_metres` decimal(16,4) DEFAULT NULL,
  `heading` double DEFAULT NULL,
  `dip_x` double DEFAULT NULL,
  `dip_y` double DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `gw12_nodes`
--

DROP TABLE IF EXISTS `gw12_nodes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gw12_nodes` (
  `id` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `gw12_raw`
--

DROP TABLE IF EXISTS `gw12_raw`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gw12_raw` (
  `id` int NOT NULL AUTO_INCREMENT,
  `device` int NOT NULL,
  `timestamp` datetime NOT NULL,
  `rtc_value` int NOT NULL,
  `bat_volts` int NOT NULL,
  `vdd` float NOT NULL,
  `temp_plat` int NOT NULL,
  `temp_internal` int NOT NULL,
  `temp_internal_celcius` float NOT NULL,
  `pressure` int NOT NULL,
  `strain` int NOT NULL,
  `conductivity` int NOT NULL,
  `accel_x` int NOT NULL,
  `accel_y` int NOT NULL,
  `accel_z` int NOT NULL,
  `compass_x` int NOT NULL,
  `compass_y` int NOT NULL,
  `compass_z` int NOT NULL,
  `gyro_x` int NOT NULL,
  `gyro_y` int NOT NULL,
  `gyro_z` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `device` (`device`,`timestamp`),
  CONSTRAINT `gw12_raw_ibfk_1` FOREIGN KEY (`device`) REFERENCES `gw12_nodes` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13701 DEFAULT CHARSET=latin1 COMMENT='raw data from GW12 probes';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `humidity_readings`
--

DROP TABLE IF EXISTS `humidity_readings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `humidity_readings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `device_id` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL,
  `sensor_position_id` int NOT NULL,
  `value` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_id` (`device_id`,`timestamp`,`sensor_position_id`),
  KEY `sensor_position_id` (`sensor_position_id`),
  CONSTRAINT `humidity_readings_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `humidity_readings_ibfk_2` FOREIGN KEY (`sensor_position_id`) REFERENCES `sensor_positions` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=3617014 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `image_data`
--

DROP TABLE IF EXISTS `image_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `image_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `device_id` varchar(255) NOT NULL,
  `filename` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `timestamp_2` (`timestamp`,`device_id`),
  KEY `device_id` (`device_id`),
  CONSTRAINT `image_data_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10131 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `iridium_raw`
--

DROP TABLE IF EXISTS `iridium_raw`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `iridium_raw` (
  `id` int NOT NULL AUTO_INCREMENT,
  `imei` varchar(15) NOT NULL COMMENT 'device that sent the message',
  `momsn` smallint unsigned NOT NULL COMMENT 'sequence number - wraps around',
  `transmit_time` datetime NOT NULL,
  `recieve_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `cep` float NOT NULL COMMENT 'edtimation of accuracy of position fix (km)',
  `data` varchar(300) NOT NULL,
  `processed` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `imei` (`imei`)
) ENGINE=InnoDB AUTO_INCREMENT=3510 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `light_readings`
--

DROP TABLE IF EXISTS `light_readings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `light_readings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `device_id` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL,
  `value` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_id` (`device_id`,`timestamp`),
  CONSTRAINT `light_readings_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=26378 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `locations`
--

DROP TABLE IF EXISTS `locations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `locations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `location_name` varchar(40) NOT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `elevation` double DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `orbit_files`
--

DROP TABLE IF EXISTS `orbit_files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orbit_files` (
  `id` int NOT NULL AUTO_INCREMENT,
  `filename` varchar(40) NOT NULL,
  `type` varchar(10) NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `filename` (`filename`),
  UNIQUE KEY `one-type-per-day` (`type`,`date`),
  KEY `type` (`type`),
  KEY `date` (`date`)
) ENGINE=InnoDB AUTO_INCREMENT=11215 DEFAULT CHARSET=latin1 COMMENT='Details of combined orbit files available on this server';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `orbit_types`
--

DROP TABLE IF EXISTS `orbit_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orbit_types` (
  `name` varchar(10) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Definitions of different types of gps orbit file';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `power_inputs`
--

DROP TABLE IF EXISTS `power_inputs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `power_inputs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(40) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `power_readings`
--

DROP TABLE IF EXISTS `power_readings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `power_readings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `device_id` varchar(255) NOT NULL,
  `input_id` int NOT NULL,
  `timestamp` datetime NOT NULL,
  `current` float DEFAULT NULL,
  `voltage` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_id` (`device_id`,`input_id`,`timestamp`),
  KEY `device` (`device_id`,`input_id`),
  KEY `input_id` (`input_id`),
  CONSTRAINT `power_readings_ibfk_3` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `power_readings_ibfk_4` FOREIGN KEY (`input_id`) REFERENCES `power_inputs` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=27763 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `power_states`
--

DROP TABLE IF EXISTS `power_states`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `power_states` (
  `id` int NOT NULL AUTO_INCREMENT,
  `device_id` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL,
  `value` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_id` (`device_id`,`timestamp`),
  CONSTRAINT `power_states_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=4893 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pressure_readings`
--

DROP TABLE IF EXISTS `pressure_readings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pressure_readings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `device_id` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL,
  `value` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_id` (`device_id`,`timestamp`),
  CONSTRAINT `pressure_readings_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=1814524 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rain_readings`
--

DROP TABLE IF EXISTS `rain_readings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rain_readings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `device_id` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL,
  `value` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_id_2` (`device_id`,`timestamp`),
  KEY `device_id` (`device_id`),
  CONSTRAINT `rain_readings_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1151962 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `received_files`
--

DROP TABLE IF EXISTS `received_files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `received_files` (
  `id` int NOT NULL AUTO_INCREMENT,
  `filename` varchar(40) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `filename` (`filename`)
) ENGINE=InnoDB AUTO_INCREMENT=7556 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rssi_readings`
--

DROP TABLE IF EXISTS `rssi_readings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rssi_readings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `device_id` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL,
  `value` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_id` (`device_id`,`timestamp`),
  CONSTRAINT `rssi_readings_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=508 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sensor_positions`
--

DROP TABLE IF EXISTS `sensor_positions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sensor_positions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `description` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `snow_readings`
--

DROP TABLE IF EXISTS `snow_readings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `snow_readings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `device_id` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL,
  `value` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_id` (`device_id`,`timestamp`),
  CONSTRAINT `snow_readings_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=6627 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `strain_readings`
--

DROP TABLE IF EXISTS `strain_readings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `strain_readings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `device_id` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL,
  `value` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_id` (`device_id`,`timestamp`),
  CONSTRAINT `strain_readings_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=26378 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `temperature_readings`
--

DROP TABLE IF EXISTS `temperature_readings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `temperature_readings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `device_id` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL,
  `sensor_position_id` int NOT NULL,
  `value` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_id` (`device_id`,`timestamp`,`sensor_position_id`),
  KEY `sensor_position_id` (`sensor_position_id`),
  CONSTRAINT `temperature_readings_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `temperature_readings_ibfk_2` FOREIGN KEY (`sensor_position_id`) REFERENCES `sensor_positions` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=4012932 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tracker_data`
--

DROP TABLE IF EXISTS `tracker_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tracker_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `rover_id` int NOT NULL,
  `timestamp` datetime NOT NULL,
  `longitude` double NOT NULL COMMENT 'decimal',
  `latitude` double NOT NULL COMMENT 'decimal',
  `altitude` double NOT NULL COMMENT 'meters',
  `quality` int DEFAULT NULL,
  `hdop` float DEFAULT NULL,
  `sats` int NOT NULL,
  `temperature` float DEFAULT NULL COMMENT 'Temperature in degress Celcius only available after 2018',
  PRIMARY KEY (`id`),
  UNIQUE KEY `rover_id_timestamp` (`rover_id`,`timestamp`),
  KEY `sats` (`sats`),
  KEY `timestamp` (`timestamp`),
  KEY `rover_id` (`rover_id`),
  CONSTRAINT `tracker_data_ibfk_1` FOREIGN KEY (`rover_id`) REFERENCES `tracker_devices` (`rover_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13533 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tracker_devices`
--

DROP TABLE IF EXISTS `tracker_devices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tracker_devices` (
  `rover_id` int NOT NULL AUTO_INCREMENT,
  `imei` varchar(15) DEFAULT NULL,
  `Notes` varchar(250) NOT NULL,
  `Glacier` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`rover_id`),
  KEY `Glacier` (`Glacier`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `voltage_readings`
--

DROP TABLE IF EXISTS `voltage_readings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `voltage_readings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `device_id` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL,
  `value` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_id` (`device_id`,`timestamp`),
  CONSTRAINT `voltage_readings_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=89530 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `weather`
--

DROP TABLE IF EXISTS `weather`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `weather` (
  `id` int NOT NULL AUTO_INCREMENT,
  `location_id` int NOT NULL,
  `timestamp` datetime NOT NULL,
  `temperature` float NOT NULL,
  `humidity` float NOT NULL,
  `wind_direction` float NOT NULL,
  `wind_speed` float NOT NULL,
  `pressure` float NOT NULL,
  `dewpoint` float NOT NULL,
  `visibility` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `location_id_2` (`location_id`,`timestamp`),
  CONSTRAINT `weather_ibfk_1` FOREIGN KEY (`location_id`) REFERENCES `weather_locations` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=33126 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `weather_locations`
--

DROP TABLE IF EXISTS `weather_locations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `weather_locations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type_id` int NOT NULL,
  `station_id` varchar(15) DEFAULT NULL,
  `name` varchar(40) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `latitude` (`latitude`,`longitude`,`elevation`),
  KEY `type_id` (`type_id`),
  CONSTRAINT `weather_locations_ibfk_1` FOREIGN KEY (`type_id`) REFERENCES `weather_type` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `weather_type`
--

DROP TABLE IF EXISTS `weather_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `weather_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Description` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `wind_readings`
--

DROP TABLE IF EXISTS `wind_readings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wind_readings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `device_id` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL,
  `speed` float NOT NULL,
  `direction` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_id_2` (`device_id`,`timestamp`),
  KEY `device_id` (`device_id`),
  CONSTRAINT `wind_readings_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1173344 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Current Database: `norway`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `norway` /*!40100 DEFAULT CHARACTER SET latin1 */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `norway`;

--
-- Table structure for table `basedata`
--

DROP TABLE IF EXISTS `basedata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `basedata` (
  `readdate` date DEFAULT NULL,
  `readtime` time DEFAULT NULL,
  `temp` float DEFAULT NULL,
  `xtilt` float DEFAULT NULL,
  `ytilt` float DEFAULT NULL,
  `ploughch1` float DEFAULT NULL,
  `ploughch2` float DEFAULT NULL,
  `tilt1x` float DEFAULT NULL,
  `tilt1y` float DEFAULT NULL,
  `tilt2x` float DEFAULT NULL,
  `tilt2y` float DEFAULT NULL,
  `battvolts` double DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dat71`
--

DROP TABLE IF EXISTS `dat71`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dat71` (
  `cmd` text
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `delaydata`
--

DROP TABLE IF EXISTS `delaydata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `delaydata` (
  `probe_id` tinyint NOT NULL,
  `date_measured` date NOT NULL,
  `date_received` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fm`
--

DROP TABLE IF EXISTS `fm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fm` (
  `fm` longblob
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `probedata`
--

DROP TABLE IF EXISTS `probedata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `probedata` (
  `probeid` int DEFAULT NULL,
  `readdate` date DEFAULT NULL,
  `readtime` time DEFAULT NULL,
  `temperature` float DEFAULT NULL,
  `pressure` float DEFAULT NULL,
  `strain` float DEFAULT NULL,
  `resistivity` float DEFAULT NULL,
  `xtilt` float DEFAULT NULL,
  `ytilt` float DEFAULT NULL,
  `ztilt` float DEFAULT NULL,
  `battvolts` float DEFAULT NULL,
  `light` float DEFAULT NULL,
  KEY `probeid` (`probeid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `wthrdata`
--

DROP TABLE IF EXISTS `wthrdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wthrdata` (
  `readdate` date DEFAULT NULL,
  `readtime` time DEFAULT NULL,
  `extemp` int DEFAULT NULL,
  `intemp` int DEFAULT NULL,
  `maxtemp` int DEFAULT NULL,
  `mintemp` int DEFAULT NULL,
  `rain` int DEFAULT NULL,
  `maxrain` int DEFAULT NULL,
  `pressure` float DEFAULT NULL,
  `sun` int DEFAULT NULL,
  `maxsun` int DEFAULT NULL,
  `uv` int DEFAULT NULL,
  `maxuv` int DEFAULT NULL,
  `wind` int DEFAULT NULL,
  `maxwind` int DEFAULT NULL,
  `winddir` int DEFAULT NULL,
  `maxwinddir` int DEFAULT NULL,
  `inhumidity` int DEFAULT NULL,
  `exhumidity` int DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `xadxx`
--

DROP TABLE IF EXISTS `xadxx`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `xadxx` (
  `codetab` text
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-01-05 20:25:47
