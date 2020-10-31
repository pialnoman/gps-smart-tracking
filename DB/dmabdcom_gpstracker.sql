-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Nov 08, 2019 at 06:55 AM
-- Server version: 5.6.41-84.1
-- PHP Version: 7.2.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dmabdcom_gpstracker`
--

-- --------------------------------------------------------

--
-- Table structure for table `agent_account`
--

CREATE TABLE `agent_account` (
  `acc_id` int(11) NOT NULL,
  `acc_admin_id` int(11) NOT NULL,
  `acc_agent_id` int(11) NOT NULL,
  `acc_farmer_id` int(11) NOT NULL,
  `acc_due` decimal(10,2) NOT NULL,
  `acc_due_date` datetime DEFAULT NULL,
  `acc_rcv` decimal(10,2) NOT NULL,
  `acc_rcv_date` datetime DEFAULT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0 = due and 1 = '
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `agent_account`
--

INSERT INTO `agent_account` (`acc_id`, `acc_admin_id`, `acc_agent_id`, `acc_farmer_id`, `acc_due`, `acc_due_date`, `acc_rcv`, `acc_rcv_date`, `status`) VALUES
(1, 1, 2, 3, '1000.00', '2019-10-10 00:00:00', '0.00', NULL, 0),
(2, 1, 2, 3, '1000.00', '2019-10-10 00:00:00', '0.00', NULL, 0),
(3, 1, 2, 3, '1000.00', '2019-10-10 00:00:00', '0.00', NULL, 0);

-- --------------------------------------------------------

--
-- Table structure for table `agent_target`
--

CREATE TABLE `agent_target` (
  `ata_id` int(11) NOT NULL,
  `ata_agent_id` int(11) NOT NULL,
  `ata_amount` decimal(10,2) NOT NULL,
  `ata_from_date` datetime NOT NULL,
  `ata_to_date` datetime NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `agent_target`
--

INSERT INTO `agent_target` (`ata_id`, `ata_agent_id`, `ata_amount`, `ata_from_date`, `ata_to_date`, `created_by`, `created_at`) VALUES
(1, 1, '1000.00', '2019-01-10 00:00:00', '2019-01-30 00:00:00', 1, '2019-01-10 17:31:00'),
(2, 2, '2000.00', '2019-01-10 00:00:00', '2019-01-30 00:00:00', 1, '2019-01-10 17:31:00');

-- --------------------------------------------------------

--
-- Table structure for table `application`
--

CREATE TABLE `application` (
  `app_id` int(11) NOT NULL,
  `app_name` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `app_type` varchar(60) CHARACTER SET utf8 DEFAULT NULL,
  `app_host` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `application`
--

INSERT INTO `application` (`app_id`, `app_name`, `app_type`, `app_host`, `created_by`, `created_at`) VALUES
(1, 'metal_gpstracker', 'android', 'wasa_server', 6, '2019-07-25 08:06:32');

-- --------------------------------------------------------

--
-- Table structure for table `assign_info`
--

CREATE TABLE `assign_info` (
  `ass_id` int(11) NOT NULL,
  `usr_id` int(11) NOT NULL,
  `pro_id` int(11) NOT NULL,
  `ass_type` tinyint(1) NOT NULL COMMENT '1-to product user, 2-to engineer',
  `created_by` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `assign_info`
--

INSERT INTO `assign_info` (`ass_id`, `usr_id`, `pro_id`, `ass_type`, `created_by`, `created_at`) VALUES
(1, 2, 1, 1, 1, '2019-07-25 09:59:25'),
(2, 3, 2, 1, 1, '2019-07-25 09:59:25'),
(3, 4, 3, 1, 1, '2019-07-25 09:59:25'),
(4, 5, 4, 1, 1, '2019-07-25 09:59:25'),
(5, 6, 5, 1, 1, '2019-07-25 09:59:25'),
(6, 7, 6, 1, 1, '2019-07-25 09:59:25'),
(18, 9, 18, 1, 9, '2019-09-08 22:38:14'),
(19, 18, 19, 1, 9, '2019-09-26 22:38:14'),
(20, 19, 20, 1, 9, '2019-09-26 22:38:14'),
(21, 20, 21, 1, 9, '2019-09-26 22:38:14');

-- --------------------------------------------------------

--
-- Table structure for table `devices_gateway`
--

CREATE TABLE `devices_gateway` (
  `dev_id` int(11) NOT NULL,
  `dev_name` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `dev_type` int(3) DEFAULT NULL COMMENT 'from dev_type table',
  `dev_protocol` varchar(10) CHARACTER SET utf8 DEFAULT NULL COMMENT 'device communication protocol',
  `dev_location` tinyint(1) NOT NULL DEFAULT '0',
  `dev_model` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `dev_s_n` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
  `dev_mob_num` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `dev_ip` varchar(32) CHARACTER SET utf8 DEFAULT NULL,
  `dev_mac` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `dev_image` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `dev_app_id` int(3) DEFAULT NULL,
  `dev_created_by` int(11) NOT NULL,
  `dev_created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `devices_gateway`
--

INSERT INTO `devices_gateway` (`dev_id`, `dev_name`, `dev_type`, `dev_protocol`, `dev_location`, `dev_model`, `dev_s_n`, `dev_mob_num`, `dev_ip`, `dev_mac`, `dev_image`, `dev_app_id`, `dev_created_by`, `dev_created_at`) VALUES
(1, 'gps tracker 1', 1, 'tcp/ip', 1, 'ET 300', '1703070823', NULL, NULL, NULL, NULL, 1, 1, '2019-07-25 08:10:30'),
(3, 'gps tracker 2', 1, 'tcp/ip', 1, 'ET 300', '1703071400', NULL, NULL, NULL, NULL, 1, 1, '2019-07-25 08:12:35'),
(4, 'gps tracker 3', 1, 'tcp/ip', 1, 'BW 202', '0868003032433430', NULL, NULL, NULL, NULL, 1, 1, '2019-07-25 08:12:35'),
(5, 'gps tracker 4', 1, 'tcp/ip', 1, 'ET 300', '1703070707', NULL, NULL, NULL, NULL, 1, 1, '2019-07-25 08:12:35'),
(6, 'gps tracker 5', 1, 'tcp/ip', 1, 'BW 202', '1703154938', NULL, NULL, NULL, NULL, 1, 1, '2019-07-25 08:12:35'),
(7, 'gps tracker 6', 1, 'tcp/ip', 1, 'BW 202', '1703154710', NULL, NULL, NULL, NULL, 1, 1, '2019-07-25 08:12:35'),
(10, 'gps tracker 6', 1, 'tcp/ip', 1, 'BW 202', '1703154915', NULL, NULL, NULL, NULL, 1, 1, '2019-07-25 08:12:35'),
(11, 'gps tracker 7', 1, 'tcp/ip', 1, 'BW 202', '1703155762', NULL, NULL, NULL, NULL, 1, 1, '2019-09-25 05:00:00'),
(12, 'gps tracker 8', 1, 'tcp/ip', 1, 'BW 202', '868003032159290', NULL, NULL, NULL, NULL, 1, 1, '2019-10-10 18:00:00'),
(13, 'gps tracker 9', 1, 'tcp/ip', 1, 'BW 906', '868003032159303', NULL, NULL, NULL, NULL, 1, 1, '2019-10-10 21:00:00'),
(14, 'gps tracker 10', 1, 'tcp/ip', 1, 'BW 906', '868003032159423', NULL, NULL, NULL, NULL, 1, 1, '2019-10-10 21:12:00'),
(15, 'gps tracker 11', 1, 'tcp/ip', 1, 'BW 906', '868003032159357', '01313790967', NULL, NULL, NULL, 1, 1, '2019-10-10 05:00:00'),
(16, 'gps tracker 12', 1, 'tcp/ip', 1, 'BW 906', '868003032159266', '01313790961', NULL, NULL, NULL, 1, 1, '2019-10-10 10:53:16'),
(17, 'gps tracker 13', 1, 'tcp/ip', 1, 'BW 906', '868003032159233', '01313790968', NULL, NULL, NULL, 1, 1, '2019-10-10 10:55:42'),
(18, 'gps tracker 14', 1, 'tcp/ip', 1, 'BW 906', '868003032159324', '01313790969', NULL, NULL, NULL, 1, 1, '2019-10-10 11:00:48'),
(19, 'gps tracker 15', 1, 'tcp/ip', 1, 'BW 09', '0868003032433430000', '01313790972', NULL, NULL, NULL, 1, 1, '2019-10-10 11:00:48'),
(20, 'gps tracker 16', 1, 'tcp/ip', 1, 'BW 09', '0868003032433422', '01313790971', NULL, NULL, NULL, 1, 1, '2019-10-10 11:00:48');

-- --------------------------------------------------------

--
-- Table structure for table `device_data`
--

CREATE TABLE `device_data` (
  `dvd_id` int(11) NOT NULL,
  `dev_id` int(11) NOT NULL,
  `dvd_status` tinyint(1) DEFAULT NULL COMMENT '0 and 1 = cultivation status, 2 and 3 = operational status, 4 and 5 = engine status (first one for inactivation and last one for activation status)',
  `dvd_haulage` varchar(255) NOT NULL COMMENT 'transport',
  `dvd_fuel_consumption` varchar(255) NOT NULL COMMENT 'Give fuel percentage',
  `dvd_mileages` decimal(10,2) NOT NULL,
  `dvd_running_hour` time NOT NULL,
  `dvd_start_hour` time NOT NULL,
  `dvd_end_hour` time NOT NULL,
  `dvd_latitude` varchar(255) NOT NULL,
  `dvd_longitude` varchar(255) NOT NULL,
  `dvd_speed` int(11) NOT NULL,
  `dvd_odometer_reading` int(11) NOT NULL,
  `dvd_bearing` varchar(20) NOT NULL,
  `dvd_battery` int(3) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `device_data`
--

INSERT INTO `device_data` (`dvd_id`, `dev_id`, `dvd_status`, `dvd_haulage`, `dvd_fuel_consumption`, `dvd_mileages`, `dvd_running_hour`, `dvd_start_hour`, `dvd_end_hour`, `dvd_latitude`, `dvd_longitude`, `dvd_speed`, `dvd_odometer_reading`, `dvd_bearing`, `dvd_battery`, `created_at`, `updated_at`) VALUES
(1, 1, 1, '1', '50 L', '10.00', '82:00:00', '13:00:00', '18:00:00', '25.66369', '88.93093', 10, 1000, '', 0, '2019-07-31 20:27:29', '2019-09-01 14:50:28'),
(2, 3, 1, '0', '62 L', '10.00', '92:00:00', '12:00:00', '17:00:00', '23.773525', '90.3660117', 4, 1200, '231.1', 95, '2019-07-31 20:27:29', '2019-09-26 17:21:08'),
(3, 4, 1, '1', '65 L', '11.00', '23:00:00', '12:00:00', '17:00:00', '23.79206', '90.420255', 0, 1300, '73', 0, '2019-07-31 20:27:29', '2019-10-26 17:26:51'),
(4, 5, 1, '1', '65 L', '11.00', '92:00:00', '12:00:00', '17:00:00', '24.007285', '90.3835733', 54, 1400, '186.4', 74, '2019-07-31 20:27:29', '2019-09-09 16:23:19'),
(5, 6, 1, '1', '65 L', '11.00', '92:00:00', '12:00:00', '17:00:00', '23.774133', '90.3658183', 0, 1500, '61.8', 48, '2019-07-27 20:27:29', '2019-09-23 16:06:38'),
(6, 7, 1, '0', '70 L', '15.00', '102:00:00', '13:15:00', '15:20:00', '24.886436', '91.880722', 16, 1600, '', 0, '2019-07-27 20:27:29', '2019-09-01 08:35:28'),
(6018, 11, 1, '0', '0 L', '0.00', '00:00:00', '00:00:00', '00:00:00', '23.774157', '90.3657233', 0, 0, '0.0', 90, '2019-09-26 17:20:24', '2019-09-26 17:21:08'),
(6019, 12, 1, '0', '0 L', '0.00', '00:00:00', '00:00:00', '00:00:00', '23.774157', '90.3657233', 0, 0, '0.0', 90, '2019-10-10 17:20:24', '2019-10-10 17:21:08'),
(6020, 20, 1, '0', '24 L', '0.00', '00:00:00', '00:00:00', '00:00:00', '23.111755', '114.40923', 0, 0, '2', 0, '2019-10-10 17:20:24', '2019-11-08 18:30:06');

-- --------------------------------------------------------

--
-- Table structure for table `dev_location`
--

CREATE TABLE `dev_location` (
  `loc_id` int(11) NOT NULL,
  `dev_id` int(11) NOT NULL,
  `loc_name` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `loc_country` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `loc_address` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `loc_lat` varchar(10) NOT NULL,
  `loc_long` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dev_location`
--

INSERT INTO `dev_location` (`loc_id`, `dev_id`, `loc_name`, `loc_country`, `loc_address`, `loc_lat`, `loc_long`) VALUES
(1, 1, 'Dinajpur', 'Bangladesh', 'Dinajpur', '25.636574 ', '88.636322'),
(2, 3, 'Cox\'s Bazar', 'Bangladesh', 'Cox\'s Bazar', '21.453881', '91.967651'),
(3, 4, 'Gazipur', 'Bangladesh', 'Gazipur', '22.8033', '89.5324'),
(4, 5, 'Jessore', 'Bangladesh', 'Jessore', '23.1778', '89.1801'),
(5, 6, 'Mymensingh', 'Bangladesh', 'Mymensingh', '24.7471', '90.4203'),
(6, 7, 'Savar', 'Bangladesh', 'Savar', '23.8479', '90.2576'),
(14, 10, 'Chittagong', 'Bangladesh', 'Rangamati', '22.123456', '90.123456'),
(15, 11, 'Tetulia', 'Bangladesh', 'Rangamati', '26.335377', '88.551697'),
(16, 12, 'Sundorban', 'Bangladesh', 'Rangamati', '21.9502', '89.1706'),
(17, 20, 'Rangamati', 'Bangladesh', 'Rangamati', '22.6573', '92.1733');

-- --------------------------------------------------------

--
-- Table structure for table `dev_type`
--

CREATE TABLE `dev_type` (
  `dty_id` int(11) NOT NULL,
  `dty_title` varchar(20) NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `dev_type`
--

INSERT INTO `dev_type` (`dty_id`, `dty_title`, `created_by`, `created_at`) VALUES
(1, 'gpstracker', 6, '2019-07-25 07:58:07'),
(2, 'android app', 6, '2019-07-26 07:58:07');

-- --------------------------------------------------------

--
-- Table structure for table `product_model`
--

CREATE TABLE `product_model` (
  `pmo_id` int(11) NOT NULL,
  `pmo_title` varchar(50) NOT NULL,
  `pmo_engine` varchar(10) DEFAULT NULL,
  `pmo_cylinder` varchar(5) DEFAULT NULL,
  `pmo_cubic_capacity` varchar(10) DEFAULT NULL,
  `pmo_transmission` varchar(50) DEFAULT NULL,
  `pmo_tyres` varchar(50) DEFAULT NULL,
  `pmo_rated_power` varchar(5) DEFAULT NULL,
  `pmo_rated_current` varchar(5) DEFAULT NULL,
  `pmo_engine_speed` varchar(5) DEFAULT NULL,
  `pmo_fuel_capacity` varchar(5) DEFAULT NULL,
  `pmo_warranty` varchar(5) DEFAULT NULL,
  `pmo_lwh` varchar(20) DEFAULT NULL COMMENT 'length with height',
  `pmo_dry_weight` varchar(20) DEFAULT NULL,
  `pmo_displacement` varchar(50) DEFAULT NULL,
  `pmo_dc_output` varchar(50) DEFAULT NULL,
  `contentious_op` varchar(50) DEFAULT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `product_model`
--

INSERT INTO `product_model` (`pmo_id`, `pmo_title`, `pmo_engine`, `pmo_cylinder`, `pmo_cubic_capacity`, `pmo_transmission`, `pmo_tyres`, `pmo_rated_power`, `pmo_rated_current`, `pmo_engine_speed`, `pmo_fuel_capacity`, `pmo_warranty`, `pmo_lwh`, `pmo_dry_weight`, `pmo_displacement`, `pmo_dc_output`, `contentious_op`, `created_by`, `created_at`) VALUES
(1, 'Tractor TAFE 35 DI', '35 HP', '3 nos', '2365 cc', '8 Forward 2 Reverse', '6.00×16, Rear: 13.6×28', NULL, NULL, NULL, NULL, '24 m', NULL, NULL, NULL, NULL, NULL, 1, '2019-07-25 09:23:21'),
(2, 'Tractor TAFE 241 DI', '41 HP', '3 nos', '2500 cc', '8 Forward 2 Reverse', 'Front: 6.00×16, Rear: 13.6×28', NULL, NULL, NULL, NULL, '24 m', NULL, NULL, NULL, NULL, NULL, 1, '2019-07-25 09:23:21'),
(3, 'Tractor TAFE 45 DI', '47 HP', '3 nos', '2500 cc', '8 Forward 2 Reverse', 'Front: 6.00×16, Rear: 13.6×28', NULL, NULL, NULL, NULL, '24 m', NULL, NULL, NULL, NULL, NULL, 1, '2019-07-25 09:23:21'),
(4, 'Tractor TAFE 7250 DI', '50 HP', '3 nos', '2500 cc', '8 Forward 2 Reverse', 'Front: 6.00×16, Rear: 13.6×28', NULL, NULL, NULL, NULL, '24 m', NULL, NULL, NULL, NULL, NULL, 1, '2019-07-25 09:23:21'),
(5, 'Diesel Gen Kummins KH-16GF', NULL, NULL, NULL, NULL, NULL, '18', '20', '1500R', NULL, '24 m', NULL, NULL, NULL, NULL, NULL, 1, '2019-07-25 09:23:21'),
(6, 'Portable Gen Marine Gen-set 001', NULL, NULL, NULL, NULL, NULL, '18', '20', '1500R', NULL, '24 m', NULL, NULL, NULL, NULL, NULL, 1, '2019-07-25 09:23:21');

-- --------------------------------------------------------

--
-- Table structure for table `product_profile`
--

CREATE TABLE `product_profile` (
  `pro_id` int(11) NOT NULL,
  `pro_name` varchar(50) NOT NULL,
  `dev_id` int(11) NOT NULL,
  `pmo_id` int(11) NOT NULL,
  `ven_id` int(11) NOT NULL,
  `type_id` int(11) NOT NULL,
  `pro_purchase_date` date DEFAULT NULL,
  `pro_ft_vol` float DEFAULT NULL COMMENT 'Product Fuel Volume',
  `pro_specifications` varchar(255) DEFAULT NULL,
  `pro_others` varchar(255) DEFAULT NULL,
  `pro_mfg_date` date DEFAULT NULL,
  `pro_exp_date` date DEFAULT NULL,
  `pro_status` tinyint(1) NOT NULL COMMENT '0 = inactive and 1 = active',
  `pro_image` varchar(255) DEFAULT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `product_profile`
--

INSERT INTO `product_profile` (`pro_id`, `pro_name`, `dev_id`, `pmo_id`, `ven_id`, `type_id`, `pro_purchase_date`, `pro_ft_vol`, `pro_specifications`, `pro_others`, `pro_mfg_date`, `pro_exp_date`, `pro_status`, `pro_image`, `created_by`, `created_at`) VALUES
(1, 'Tractor 1', 1, 1, 1, 1, '2019-07-17', NULL, '', '', '2019-07-03', '2021-03-31', 1, NULL, 1, '2019-07-25 09:36:36'),
(2, 'Tractor 2', 3, 2, 1, 1, '2019-07-17', NULL, '', '', '2019-07-03', '2021-03-31', 1, NULL, 1, '2019-07-25 09:36:36'),
(3, 'Tractor 3', 4, 3, 1, 1, '2019-07-17', NULL, '', '', '2019-07-03', '2021-03-31', 1, NULL, 1, '2019-07-25 09:36:36'),
(4, 'Tractor 4', 5, 4, 1, 1, '2019-07-17', NULL, '', '', '2019-07-03', '2021-03-31', 1, NULL, 1, '2019-07-25 09:36:36'),
(5, 'Diesel Gen 1', 6, 5, 2, 2, '2019-07-17', NULL, '', '', '2019-07-03', '2021-03-31', 1, NULL, 1, '2019-07-25 09:36:36'),
(6, 'Portable Gen 1', 7, 6, 2, 3, '2019-07-17', NULL, '', '', '2019-07-03', '2021-03-31', 1, NULL, 1, '2019-07-25 09:36:36'),
(18, 'TEST 535', 10, 1, 1, 1, NULL, NULL, NULL, NULL, NULL, NULL, 1, NULL, 9, '2019-09-08 22:38:14'),
(19, 'TEST 124', 11, 2, 1, 1, '2019-07-17', NULL, NULL, NULL, NULL, NULL, 1, NULL, 9, '2019-09-08 22:38:14'),
(20, 'TEST 124', 12, 5, 1, 2, '2019-10-10', NULL, NULL, NULL, NULL, NULL, 1, NULL, 9, '2019-09-08 22:38:14'),
(21, 'TEST 20', 20, 1, 1, 1, '2019-10-10', 40.25, NULL, NULL, NULL, NULL, 1, NULL, 9, '2019-09-08 22:38:14');

-- --------------------------------------------------------

--
-- Table structure for table `product_type`
--

CREATE TABLE `product_type` (
  `type_id` int(11) NOT NULL,
  `type_name` varchar(50) NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `product_type`
--

INSERT INTO `product_type` (`type_id`, `type_name`, `created_by`, `created_at`) VALUES
(1, 'Tractor', 6, '2019-07-25 19:59:45'),
(2, 'Diesel Generator', 6, '2019-07-25 20:01:02'),
(3, 'Portable Generator', 6, '2019-07-25 20:01:02');

-- --------------------------------------------------------

--
-- Table structure for table `servicing_schedule`
--

CREATE TABLE `servicing_schedule` (
  `ser_id` int(11) NOT NULL,
  `pro_id` int(11) NOT NULL,
  `schedule_time` varchar(255) NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `user_log`
--

CREATE TABLE `user_log` (
  `log_id` int(11) NOT NULL,
  `usr_id` int(11) NOT NULL,
  `log_login` datetime NOT NULL,
  `log_logout` datetime NOT NULL,
  `log_ip` varchar(30) NOT NULL,
  `log_location` varchar(100) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `user_profile`
--

CREATE TABLE `user_profile` (
  `usr_id` int(11) NOT NULL,
  `usr_fname` varchar(30) CHARACTER SET utf8 DEFAULT NULL,
  `usr_lname` varchar(30) CHARACTER SET utf8 DEFAULT NULL,
  `usr_name` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `usr_email` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `usr_password` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `usr_fcmtoken` text NOT NULL,
  `usr_address` tinyint(1) DEFAULT '0' COMMENT '0 = no and 1 = yes, from usr_address table',
  `usr_phone` tinyint(1) DEFAULT '0' COMMENT '0 = no and 1 = yes, from usr_phone table',
  `usr_occupation` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0 = no and 1 = yes',
  `usr_account_status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0 = no and 1 = yes',
  `usr_behavior` tinyint(1) DEFAULT '0' COMMENT '1 = yes payment and 0 = no payment',
  `usr_location` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0=no location and 1 = location',
  `usr_create_time` time DEFAULT NULL,
  `usr_create_date` date DEFAULT NULL,
  `usr_account_type` tinyint(2) DEFAULT NULL COMMENT '0 = super user , 1 = normal user, 2 = admin , 3 = customer, 4=agent',
  `usr_modified_time` time DEFAULT NULL,
  `usr_modified_date` date DEFAULT NULL,
  `app_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user_profile`
--

INSERT INTO `user_profile` (`usr_id`, `usr_fname`, `usr_lname`, `usr_name`, `usr_email`, `usr_password`, `usr_fcmtoken`, `usr_address`, `usr_phone`, `usr_occupation`, `usr_account_status`, `usr_behavior`, `usr_location`, `usr_create_time`, `usr_create_date`, `usr_account_type`, `usr_modified_time`, `usr_modified_date`, `app_id`) VALUES
(1, 'Real', 'Haque', 'Real', 'real_ariful@hotmail.com', 'e10adc3949ba59abbe56e057f20f883e', '', 1, 1, 0, 0, NULL, 1, '11:00:00', '2019-07-25', 4, NULL, NULL, 1),
(2, 'Nizam', 'Ahmed', 'Nizam', 'real_ariful@hotmail.com', 'e10adc3949ba59abbe56e057f20f883e', '', 1, 1, 0, 0, NULL, 1, '11:00:00', '2019-07-25', 4, NULL, NULL, 1),
(3, 'Sinthia', 'Sultana', 'Sinthia', 'sinthia.sultana@gmail.com', '123456', '', 1, 1, 0, 0, NULL, 0, '11:00:00', '2019-07-25', 3, NULL, NULL, 1),
(4, 'Shiblu', 'Alam', 'Shiblu', 'shiblu.alam@gmail.com', '123456', '', 1, 1, 0, 0, NULL, 0, '11:00:00', '2019-07-25', 3, NULL, NULL, 1),
(5, 'Pubesh', 'Khan', 'Pubesh', 'pubesh.khan@gmail.com', '123456', '', 1, 1, 0, 0, NULL, 0, '11:00:00', '2019-07-25', 3, NULL, NULL, 1),
(6, 'Misla', 'Titu', 'Misla', 'misla.titu@gmail.com', '123456', '', 1, 1, 0, 0, NULL, 0, '11:00:00', '2019-07-25', 3, NULL, NULL, 1),
(7, 'Nahid', 'Rahman', 'Nahid', 'nahid.rahman@gmail.com', '123456', '', 1, 1, 0, 0, NULL, 0, '11:00:00', '2019-07-25', 3, NULL, NULL, 1),
(8, 'Hasan', 'Mahmood', 'Hasan', 'hasan@gmail.com', '827ccb0eea8a706c4c34a16891f84e7b', '123sada', 1, 1, 0, 0, NULL, 0, '11:38:44', '2019-07-29', 2, NULL, NULL, 1),
(9, 'Admin', 'admin', 'admin', 'admin@gmail.com', '21232f297a57a5a743894a0e4a801fc3', 'eIuNj0assEc:APA91bGug-HJ1IAZIAuKCCa36QGjDa7mU_al19dHjuYddTEx88SJmDmFQtOwuEEL8_P7IUHmEzooO6z207DkRKfjrx-7YZXGcbfW6n46IAkIkI2fOZK3cJWqj1FU3Qx6Ni17JGIpsQJ4', 1, 1, 0, 0, NULL, 0, '11:38:44', '2019-07-29', 0, NULL, NULL, 1),
(18, 'Elias', 'Hossain', 'elias', 'elias@gmail.com', '21232f297a57a5a743894a0e4a801fc3', '123sada', 1, 1, 0, 0, NULL, 0, '11:38:44', '2019-09-26', 3, NULL, NULL, 1),
(19, 'Nasirul', 'Haque', 'nasirul', 'nasirul@gmail.com', '21232f297a57a5a743894a0e4a801fc3', '123sada', 1, 1, 0, 0, NULL, 0, '11:38:44', '2019-09-26', 3, NULL, NULL, 1),
(20, 'Hasibul', 'Mahmood', 'hasibul', 'hasibul@gmail.com', '21232f297a57a5a743894a0e4a801fc3', '123sada', 1, 1, 0, 0, NULL, 0, '11:38:44', '2019-09-26', 3, NULL, NULL, 1);

-- --------------------------------------------------------

--
-- Table structure for table `usr_address`
--

CREATE TABLE `usr_address` (
  `add_id` int(11) NOT NULL,
  `usr_id` int(4) NOT NULL,
  `add_village` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `add_police_station` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
  `add_zip` varchar(10) CHARACTER SET utf8 DEFAULT NULL,
  `add_road` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
  `add_house` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `add_union` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
  `add_state` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
  `add_country` varchar(20) CHARACTER SET utf8 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `usr_address`
--

INSERT INTO `usr_address` (`add_id`, `usr_id`, `add_village`, `add_police_station`, `add_zip`, `add_road`, `add_house`, `add_union`, `add_state`, `add_country`) VALUES
(1, 1, 'Shyamoli', 'Parbatipur', '5250', 'Amirganj', '53', 'Amirganj', 'Rangpur', 'Bangladesh'),
(2, 2, 'Parbatipur', 'Gazipur', '5120', 'Gazipur', '25', 'Gazipur', 'Gazipur', 'Bangladesh'),
(3, 3, 'Cox\'s Bazar', 'Barishal', '5120', 'Barishal', '25', 'Barishal', 'Barishal', 'Bangladesh'),
(4, 4, '4', 'Gaibandha', '5120', 'Gaibandha', '25', 'Gaibandha', 'Gaibandha', 'Bangladesh'),
(5, 5, 'Khulna', 'Shylhet', '6150', 'Shylhet', '25', 'Shylhet', 'Shylhet', 'Bangladesh'),
(6, 6, 'Bajitpur', 'Bajitpur', '5105', 'Bajitpur', '25', 'Bajitpur', 'Bajitpur', 'Bangladesh'),
(7, 7, 'Shylhet', 'Cox\'s Bazar', '5105', 'Cox\'s Bazar', '25', 'Cox\'s Bazar', 'Cox\'s Bazar', 'Bangladesh'),
(8, 8, 'Chittagong', 'Chittagong', '5105', 'Chittagong', '52', 'Chittagong', 'Chittagong', 'Bangladesh'),
(13, 18, 'Tetulia', 'Tetulia', '5105', 'Tetulia', '52', 'Tetulia', 'Tetulia', 'Bangladesh'),
(14, 19, 'Sundorban', 'Sundorban', '5105', 'Sundorban', '52', 'Sundorban', 'Sundorban', 'Bangladesh'),
(15, 20, 'Rangamati', 'Rangamati', '5105', 'Rangamati', '52', 'Rangamati', 'Rangamati', 'Bangladesh');

-- --------------------------------------------------------

--
-- Table structure for table `usr_citizenship`
--

CREATE TABLE `usr_citizenship` (
  `cit_id` int(11) NOT NULL,
  `usr_id` int(4) NOT NULL,
  `cit_dob` date DEFAULT NULL,
  `cit_nid` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `cit_passport` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
  `cit_gender` tinyint(1) DEFAULT NULL,
  `cit_citizenship` varchar(50) CHARACTER SET utf8 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `usr_location`
--

CREATE TABLE `usr_location` (
  `id` int(11) NOT NULL,
  `usr_id` int(11) NOT NULL,
  `loc_long` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `loc_lati` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `loc_imei` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `loc_date_time` datetime DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `usr_location`
--

INSERT INTO `usr_location` (`id`, `usr_id`, `loc_long`, `loc_lati`, `loc_imei`, `loc_date_time`) VALUES
(1, 1, '12.123456', '80.123456', '12345', '2019-10-06 10:52:06'),
(2, 2, '12.57676', '80.43546', '1234', '2019-10-07 16:43:10'),
(3, 1, '12.123456', '80.123456', '12345', '2019-10-07 17:30:30'),
(4, 1, '12.57676', '80.43546', '1234', '2019-10-07 17:31:58'),
(5, 1, '90.3660558', '23.7744464', '65765', '2019-10-07 17:37:10'),
(6, 1, '90.366057', '23.7744484', '65765', '2019-10-07 17:37:30'),
(7, 1, '90.3660616', '23.7744455', '65765', '2019-10-07 17:38:10'),
(8, 1, '90.36607', '23.7743796', '65765', '2019-10-07 17:39:11'),
(9, 1, '90.3660445', '23.774511', '65765', '2019-10-09 10:55:41'),
(10, 1, '90.3660445', '23.774511', '65765', '2019-10-09 10:55:52'),
(11, 1, '90.3660398', '23.7744958', '65765', '2019-10-09 10:56:53'),
(12, 1, '90.3660709', '23.7743708', '65765', '2019-10-09 10:58:13'),
(13, 1, '90.3660531', '23.7744397', '65765', '2019-10-09 10:59:13'),
(14, 1, '90.3660524', '23.7744371', '65765', '2019-10-09 10:59:53'),
(15, 1, '90.3660546', '23.7745426', '65765', '2019-10-09 11:00:53'),
(16, 1, '90.3660746', '23.7743736', '65765', '2019-10-09 11:01:53'),
(17, 1, '90.3660434', '23.7744934', '65765', '2019-10-09 11:02:53'),
(18, 1, '90.3661108', '23.7742385', '65765', '2019-10-09 11:03:53'),
(19, 1, '90.3660968', '23.7742513', '65765', '2019-10-09 11:04:48'),
(20, 1, '90.3660746', '23.7743736', '65765', '2019-10-09 11:06:48'),
(21, 1, '90.3660547', '23.7744381', '65765', '2019-10-09 11:07:48'),
(22, 1, '90.3660209', '23.7744751', '65765', '2019-10-09 11:08:51'),
(23, 1, '90.3660521', '23.7744517', '65765', '2019-10-09 11:09:48'),
(24, 1, '90.3660512', '23.7744557', '65765', '2019-10-09 11:10:51'),
(25, 1, '90.366055', '23.7745423', '65765', '2019-10-09 11:11:41'),
(26, 1, '90.3660108', '23.7743685', '65765', '2019-10-09 11:12:18'),
(27, 1, '90.3660108', '23.7743685', '65765', '2019-10-09 11:12:27'),
(28, 1, '90.3660108', '23.7743685', '65765', '2019-10-09 11:13:32'),
(29, 1, '90.3660108', '23.7743685', '65765', '2019-10-09 11:14:32'),
(30, 1, '90.3660108', '23.7743685', '65765', '2019-10-09 11:15:21'),
(31, 1, '90.3660108', '23.7743685', '65765', '2019-10-09 11:16:32'),
(32, 1, '90.3660504', '23.7744478', '65765', '2019-10-09 11:17:49'),
(33, 1, '90.3660504', '23.7744478', '65765', '2019-10-09 11:19:02'),
(34, 1, '90.3660809', '23.7744661', '65765', '2019-10-09 11:19:32'),
(35, 1, '90.3660809', '23.7744661', '65765', '2019-10-09 11:19:44'),
(36, 1, '90.3660809', '23.7744661', '65765', '2019-10-09 11:20:01'),
(37, 1, '90.3660742', '23.7743514', '65765', '2019-10-09 11:20:41'),
(38, 1, '90.3660561', '23.7745675', '65765', '2019-10-09 11:22:42'),
(39, 1, '90.36615', '23.7740688', '65765', '2019-10-09 11:23:42'),
(40, 1, '90.366055', '23.7744261', '65765', '2019-10-09 11:24:45'),
(41, 1, '90.3660401', '23.7745262', '65765', '2019-10-09 11:25:45'),
(42, 1, '90.366012', '23.7744422', '65765', '2019-10-09 11:26:42'),
(43, 1, '90.3660264', '23.7745139', '65765', '2019-10-09 11:28:25'),
(44, 1, '90.3660264', '23.7745139', '65765', '2019-10-09 11:28:42'),
(45, 1, '90.3660329', '23.7744326', '65765', '2019-10-09 11:29:42'),
(46, 1, '90.3660503', '23.7744477', '65765', '2019-10-09 11:30:42'),
(47, 1, '90.3660501', '23.7744495', '65765', '2019-10-09 11:32:25'),
(48, 1, '90.3660501', '23.7744495', '65765', '2019-10-09 11:32:42'),
(49, 1, '90.36605', '23.7744494', '65765', '2019-10-09 11:33:42'),
(50, 1, '90.3660448', '23.7745663', '65765', '2019-10-09 11:34:42'),
(51, 1, '90.3660578', '23.7744557', '65765', '2019-10-09 11:35:43'),
(52, 1, '90.3660523', '23.7744727', '65765', '2019-10-09 11:36:43'),
(53, 1, '90.3660653', '23.7744086', '65765', '2019-10-09 11:37:43'),
(54, 1, '90.3660827', '23.7743671', '65765', '2019-10-09 11:38:43'),
(55, 1, '90.3660547', '23.7745425', '65765', '2019-10-09 11:39:43'),
(56, 1, '90.3660747', '23.7743746', '65765', '2019-10-09 11:40:43'),
(57, 1, '90.3660747', '23.7743757', '65765', '2019-10-09 11:41:43'),
(58, 1, '90.3660508', '23.774457', '65765', '2019-10-09 11:43:23'),
(59, 1, '90.3660499', '23.7744493', '65765', '2019-10-09 11:43:43'),
(60, 1, '90.36605', '23.7744494', '65765', '2019-10-09 11:44:43'),
(61, 1, '90.3660259', '23.7744257', '65765', '2019-10-09 11:45:43'),
(62, 1, '90.3661229', '23.7742165', '65765', '2019-10-09 11:47:24'),
(63, 1, '90.3660446', '23.7745665', '65765', '2019-10-09 11:47:44'),
(64, 1, '90.366095', '23.7744666', '65765', '2019-10-09 11:49:24'),
(65, 1, '90.3661031', '23.774257', '65765', '2019-10-09 11:49:44'),
(66, 1, '90.3660614', '23.7744518', '65765', '2019-10-09 11:50:44'),
(67, 1, '90.3661198', '23.7741297', '65765', '2019-10-09 11:51:44'),
(68, 1, '90.3660885', '23.7743437', '65765', '2019-10-09 11:52:45'),
(69, 1, '90.3660797', '23.7744471', '65765', '2019-10-09 11:53:45'),
(70, 1, '90.3660797', '23.7744471', 'f645a8cb39d5fb59', '2019-10-09 11:54:28'),
(71, 1, '90.3660691', '23.7743981', 'f645a8cb39d5fb59', '2019-10-09 11:54:37'),
(72, 1, '90.3660503', '23.7743599', 'f645a8cb39d5fb59', '2019-10-09 11:55:28'),
(73, 1, '90.3660704', '23.7743794', 'f645a8cb39d5fb59', '2019-10-09 11:56:32'),
(74, 1, '90.3660879', '23.7743455', 'f645a8cb39d5fb59', '2019-10-09 11:57:32'),
(75, 1, '90.3660536', '23.7743561', 'f645a8cb39d5fb59', '2019-10-09 11:58:32'),
(76, 1, '90.36609', '23.7743997', 'f645a8cb39d5fb59', '2019-10-09 11:59:32'),
(77, 1, '90.3660824', '23.7743677', 'f645a8cb39d5fb59', '2019-10-09 12:00:32'),
(78, 1, '90.3660505', '23.7744384', 'f645a8cb39d5fb59', '2019-10-09 12:01:32'),
(79, 1, '90.3660525', '23.7744361', 'f645a8cb39d5fb59', '2019-10-09 12:02:48'),
(80, 1, '90.3660825', '23.7743674', 'f645a8cb39d5fb59', '2019-10-09 12:03:35'),
(81, 1, '90.3660825', '23.7743674', 'f645a8cb39d5fb59', '2019-10-09 12:04:35'),
(82, 1, '90.3660705', '23.7744031', 'f645a8cb39d5fb59', '2019-10-09 12:05:35'),
(83, 1, '90.3660883', '23.774344', 'f645a8cb39d5fb59', '2019-10-09 12:06:32'),
(84, 1, '90.3660974', '23.774301', 'f645a8cb39d5fb59', '2019-10-09 12:07:35'),
(85, 1, '90.3661148', '23.7742176', 'f645a8cb39d5fb59', '2019-10-09 12:08:32'),
(86, 1, '90.3661087', '23.7742569', 'f645a8cb39d5fb59', '2019-10-09 12:09:32'),
(87, 1, '90.3661104', '23.774257', 'f645a8cb39d5fb59', '2019-10-09 12:10:32'),
(88, 1, '90.3660836', '23.7743087', 'f645a8cb39d5fb59', '2019-10-09 12:11:35'),
(89, 1, '90.3661231', '23.7741208', 'f645a8cb39d5fb59', '2019-10-09 12:12:32'),
(90, 1, '90.3661188', '23.7741674', 'f645a8cb39d5fb59', '2019-10-09 12:13:32'),
(91, 1, '90.3661152', '23.7742177', 'f645a8cb39d5fb59', '2019-10-09 12:14:32'),
(92, 1, '90.366099', '23.7743037', 'f645a8cb39d5fb59', '2019-10-09 12:15:32'),
(93, 1, '90.3660436', '23.7742832', 'f645a8cb39d5fb59', '2019-10-09 12:16:32'),
(94, 1, '90.3661094', '23.7742541', 'f645a8cb39d5fb59', '2019-10-09 12:17:32'),
(95, 1, '90.3661094', '23.7742541', 'f645a8cb39d5fb59', '2019-10-09 12:18:32'),
(96, 1, '90.3661094', '23.7742541', 'f645a8cb39d5fb59', '2019-10-09 12:19:33'),
(97, 1, '90.3660975', '23.7743005', 'f645a8cb39d5fb59', '2019-10-09 12:20:32'),
(98, 1, '90.3661096', '23.7742513', 'f645a8cb39d5fb59', '2019-10-09 12:21:44'),
(99, 1, '90.366097', '23.774302', 'f645a8cb39d5fb59', '2019-10-09 12:22:32'),
(100, 1, '90.366111', '23.7742378', 'f645a8cb39d5fb59', '2019-10-09 12:23:32'),
(101, 1, '90.3660897', '23.7743402', 'f645a8cb39d5fb59', '2019-10-09 12:24:32'),
(102, 1, '90.3661172', '23.774264', 'f645a8cb39d5fb59', '2019-10-09 12:25:45'),
(103, 1, '90.3660876', '23.7743441', 'f645a8cb39d5fb59', '2019-10-09 12:26:32'),
(104, 1, '90.3661113', '23.7742363', 'f645a8cb39d5fb59', '2019-10-09 12:28:11'),
(105, 1, '90.3661113', '23.7742363', 'f645a8cb39d5fb59', '2019-10-09 12:28:32'),
(106, 1, '90.366109', '23.7742464', 'f645a8cb39d5fb59', '2019-10-09 12:29:45'),
(107, 1, '90.3660768', '23.7741669', 'f645a8cb39d5fb59', '2019-10-09 12:30:45'),
(108, 1, '90.3661147', '23.7743013', 'f645a8cb39d5fb59', '2019-10-09 12:31:45'),
(109, 1, '90.3660901', '23.7743559', 'f645a8cb39d5fb59', '2019-10-09 12:32:32'),
(110, 1, '90.3660973', '23.774308', 'f645a8cb39d5fb59', '2019-10-09 12:33:33'),
(111, 1, '90.3660699', '23.7742437', 'f645a8cb39d5fb59', '2019-10-09 12:34:32'),
(112, 1, '90.366111', '23.774253', 'f645a8cb39d5fb59', '2019-10-09 12:35:32'),
(113, 1, '90.3661122', '23.7742018', 'f645a8cb39d5fb59', '2019-10-09 12:36:32'),
(114, 1, '90.366101', '23.7741603', 'f645a8cb39d5fb59', '2019-10-09 12:37:35'),
(115, 1, '90.3661121', '23.774249', 'f645a8cb39d5fb59', '2019-10-09 12:38:32'),
(116, 1, '90.3661117', '23.7742348', 'f645a8cb39d5fb59', '2019-10-09 12:39:32'),
(117, 1, '90.3661113', '23.7742364', 'f645a8cb39d5fb59', '2019-10-09 12:40:32'),
(118, 1, '90.3660835', '23.7742789', 'f645a8cb39d5fb59', '2019-10-09 12:41:32'),
(119, 1, '90.3661048', '23.7742762', 'f645a8cb39d5fb59', '2019-10-09 12:42:32'),
(120, 1, '90.3661048', '23.7742762', 'f645a8cb39d5fb59', '2019-10-09 12:43:32'),
(121, 1, '90.3661271', '23.7741149', 'f645a8cb39d5fb59', '2019-10-09 12:44:32'),
(122, 1, '90.3661271', '23.7741149', 'f645a8cb39d5fb59', '2019-10-09 12:45:32'),
(123, 1, '90.3661271', '23.7741149', 'f645a8cb39d5fb59', '2019-10-09 12:46:32'),
(124, 1, '90.3661271', '23.7741149', 'f645a8cb39d5fb59', '2019-10-09 12:47:12'),
(125, 1, '90.3661271', '23.7741149', 'f645a8cb39d5fb59', '2019-10-09 12:47:24'),
(126, 1, '90.3661271', '23.7741149', 'f645a8cb39d5fb59', '2019-10-09 12:48:12'),
(127, 1, '90.366088', '23.7744054', 'f645a8cb39d5fb59', '2019-10-09 12:49:12'),
(128, 1, '90.366088', '23.7744054', 'f645a8cb39d5fb59', '2019-10-09 12:50:32'),
(129, 1, '90.366095', '23.7743613', 'f645a8cb39d5fb59', '2019-10-09 12:53:48'),
(130, 1, '90.3660974', '23.7743001', 'f645a8cb39d5fb59', '2019-10-09 12:54:08'),
(131, 1, '90.3661032', '23.7742569', 'f645a8cb39d5fb59', '2019-10-09 12:54:48'),
(132, 1, '90.3660917', '23.7743597', 'f645a8cb39d5fb59', '2019-10-09 12:55:48'),
(133, 1, '90.3660976', '23.7742965', 'f645a8cb39d5fb59', '2019-10-09 12:56:35'),
(134, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 13:02:05'),
(135, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 13:03:30'),
(136, 1, '90.3661693', '23.7744669', 'f645a8cb39d5fb59', '2019-10-09 13:03:31'),
(137, 1, '90.3660889', '23.774221', 'f645a8cb39d5fb59', '2019-10-09 13:05:10'),
(138, 1, '90.3661023', '23.7742819', 'f645a8cb39d5fb59', '2019-10-09 13:07:07'),
(139, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 13:07:27'),
(140, 1, '90.3660901', '23.7742604', 'f645a8cb39d5fb59', '2019-10-09 13:08:07'),
(141, 1, '90.3660886', '23.774341', 'f645a8cb39d5fb59', '2019-10-09 13:09:07'),
(142, 1, '90.3660986', '23.7743038', 'f645a8cb39d5fb59', '2019-10-09 13:10:32'),
(143, 1, '90.3661693', '23.7744669', 'f645a8cb39d5fb59', '2019-10-09 13:11:32'),
(144, 1, '90.3660774', '23.7744446', 'f645a8cb39d5fb59', '2019-10-09 13:12:47'),
(145, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 13:13:32'),
(146, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 13:14:32'),
(147, 1, '90.3661017', '23.7743102', 'f645a8cb39d5fb59', '2019-10-09 13:15:48'),
(148, 1, '90.3661017', '23.7743102', 'f645a8cb39d5fb59', '2019-10-09 13:16:28'),
(149, 1, '90.3660736', '23.7744508', 'f645a8cb39d5fb59', '2019-10-09 13:16:48'),
(150, 1, '90.3660804', '23.774258', 'f645a8cb39d5fb59', '2019-10-09 13:17:32'),
(151, 1, '90.3660923', '23.7742239', 'f645a8cb39d5fb59', '2019-10-09 13:18:32'),
(152, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 13:19:48'),
(153, 1, '90.3661011', '23.7743', 'f645a8cb39d5fb59', '2019-10-09 13:20:51'),
(154, 1, '90.3660939', '23.7743638', 'f645a8cb39d5fb59', '2019-10-09 13:21:35'),
(155, 1, '90.3660884', '23.7743416', 'f645a8cb39d5fb59', '2019-10-09 13:22:32'),
(156, 1, '90.3661164', '23.7742163', 'f645a8cb39d5fb59', '2019-10-09 13:23:32'),
(157, 1, '90.3661201', '23.7741369', 'f645a8cb39d5fb59', '2019-10-09 13:24:49'),
(158, 1, '90.3660884', '23.774341', 'f645a8cb39d5fb59', '2019-10-09 13:25:32'),
(159, 1, '90.3660884', '23.774341', 'f645a8cb39d5fb59', '2019-10-09 13:26:32'),
(160, 1, '90.3660892', '23.7743385', 'f645a8cb39d5fb59', '2019-10-09 13:28:07'),
(161, 1, '90.3660892', '23.7743385', 'f645a8cb39d5fb59', '2019-10-09 13:28:34'),
(162, 1, '90.3660892', '23.7743385', 'f645a8cb39d5fb59', '2019-10-09 13:29:32'),
(163, 1, '90.3660892', '23.7743385', 'f645a8cb39d5fb59', '2019-10-09 13:30:32'),
(164, 1, '90.3660892', '23.7743385', 'f645a8cb39d5fb59', '2019-10-09 13:31:32'),
(165, 1, '90.3660984', '23.7743553', 'f645a8cb39d5fb59', '2019-10-09 13:32:32'),
(166, 1, '90.3660984', '23.7743553', 'f645a8cb39d5fb59', '2019-10-09 13:33:32'),
(167, 1, '90.3660984', '23.7743553', 'f645a8cb39d5fb59', '2019-10-09 13:34:32'),
(168, 1, '90.3660984', '23.7743553', 'f645a8cb39d5fb59', '2019-10-09 13:35:32'),
(169, 1, '90.3660984', '23.7743553', 'f645a8cb39d5fb59', '2019-10-09 13:36:32'),
(170, 1, '90.3660995', '23.7742967', 'f645a8cb39d5fb59', '2019-10-09 13:37:32'),
(171, 1, '90.3660995', '23.7742967', 'f645a8cb39d5fb59', '2019-10-09 13:38:32'),
(172, 1, '90.3660995', '23.7742967', 'f645a8cb39d5fb59', '2019-10-09 13:39:32'),
(173, 1, '90.3660995', '23.7742967', 'f645a8cb39d5fb59', '2019-10-09 13:40:32'),
(174, 1, '90.3660995', '23.7742967', 'f645a8cb39d5fb59', '2019-10-09 13:41:32'),
(175, 1, '90.3660895', '23.7743651', 'f645a8cb39d5fb59', '2019-10-09 13:42:32'),
(176, 1, '90.3660895', '23.7743651', 'f645a8cb39d5fb59', '2019-10-09 13:43:32'),
(177, 1, '90.3660895', '23.7743651', 'f645a8cb39d5fb59', '2019-10-09 13:44:32'),
(178, 1, '90.3660895', '23.7743651', 'f645a8cb39d5fb59', '2019-10-09 13:45:32'),
(179, 1, '90.3660895', '23.7743651', 'f645a8cb39d5fb59', '2019-10-09 13:46:32'),
(180, 1, '90.3660855', '23.7743091', 'f645a8cb39d5fb59', '2019-10-09 13:47:33'),
(181, 1, '90.3660855', '23.7743091', 'f645a8cb39d5fb59', '2019-10-09 13:48:32'),
(182, 1, '90.3660855', '23.7743091', 'f645a8cb39d5fb59', '2019-10-09 13:49:32'),
(183, 1, '90.3660855', '23.7743091', 'f645a8cb39d5fb59', '2019-10-09 13:50:32'),
(184, 1, '90.3660855', '23.7743091', 'f645a8cb39d5fb59', '2019-10-09 13:51:32'),
(185, 1, '90.3661047', '23.7743009', 'f645a8cb39d5fb59', '2019-10-09 13:52:32'),
(186, 1, '90.3661047', '23.7743009', 'f645a8cb39d5fb59', '2019-10-09 13:53:32'),
(187, 1, '90.3661047', '23.7743009', 'f645a8cb39d5fb59', '2019-10-09 13:54:32'),
(188, 1, '90.3661047', '23.7743009', 'f645a8cb39d5fb59', '2019-10-09 13:55:32'),
(189, 1, '90.3661047', '23.7743009', 'f645a8cb39d5fb59', '2019-10-09 13:56:32'),
(190, 1, '90.3660814', '23.7742944', 'f645a8cb39d5fb59', '2019-10-09 13:58:08'),
(191, 1, '90.3660814', '23.7742944', 'f645a8cb39d5fb59', '2019-10-09 13:58:32'),
(192, 1, '90.3660814', '23.7742944', 'f645a8cb39d5fb59', '2019-10-09 13:59:32'),
(193, 1, '90.3660814', '23.7742944', 'f645a8cb39d5fb59', '2019-10-09 14:00:32'),
(194, 1, '90.3660814', '23.7742944', 'f645a8cb39d5fb59', '2019-10-09 14:01:32'),
(195, 1, '90.366088', '23.7743449', 'f645a8cb39d5fb59', '2019-10-09 14:02:32'),
(196, 1, '90.366088', '23.7743449', 'f645a8cb39d5fb59', '2019-10-09 14:03:32'),
(197, 1, '90.366088', '23.7743449', 'f645a8cb39d5fb59', '2019-10-09 14:04:32'),
(198, 1, '90.366088', '23.7743449', 'f645a8cb39d5fb59', '2019-10-09 14:05:32'),
(199, 1, '90.366088', '23.7743449', 'f645a8cb39d5fb59', '2019-10-09 14:06:32'),
(200, 1, '90.3661182', '23.774216', 'f645a8cb39d5fb59', '2019-10-09 14:07:32'),
(201, 1, '90.3661182', '23.774216', 'f645a8cb39d5fb59', '2019-10-09 14:08:32'),
(202, 1, '90.3661182', '23.774216', 'f645a8cb39d5fb59', '2019-10-09 14:09:32'),
(203, 1, '90.3661182', '23.774216', 'f645a8cb39d5fb59', '2019-10-09 14:10:32'),
(204, 1, '90.3661182', '23.774216', 'f645a8cb39d5fb59', '2019-10-09 14:11:32'),
(205, 1, '90.3661091', '23.7742558', 'f645a8cb39d5fb59', '2019-10-09 14:12:32'),
(206, 1, '90.3661091', '23.7742558', 'f645a8cb39d5fb59', '2019-10-09 14:13:32'),
(207, 1, '90.3661091', '23.7742558', 'f645a8cb39d5fb59', '2019-10-09 14:14:32'),
(208, 1, '90.3661091', '23.7742558', 'f645a8cb39d5fb59', '2019-10-09 14:15:32'),
(209, 1, '90.3661091', '23.7742558', 'f645a8cb39d5fb59', '2019-10-09 14:16:32'),
(210, 1, '90.3660889', '23.7743378', 'f645a8cb39d5fb59', '2019-10-09 14:17:32'),
(211, 1, '90.3660889', '23.7743378', 'f645a8cb39d5fb59', '2019-10-09 14:18:32'),
(212, 1, '90.3660889', '23.7743378', 'f645a8cb39d5fb59', '2019-10-09 14:19:32'),
(213, 1, '90.3660889', '23.7743378', 'f645a8cb39d5fb59', '2019-10-09 14:20:32'),
(214, 1, '90.3660889', '23.7743378', 'f645a8cb39d5fb59', '2019-10-09 14:21:32'),
(215, 1, '90.3660873', '23.7743675', 'f645a8cb39d5fb59', '2019-10-09 14:22:32'),
(216, 1, '90.3660873', '23.7743675', 'f645a8cb39d5fb59', '2019-10-09 14:23:32'),
(217, 1, '90.3660873', '23.7743675', 'f645a8cb39d5fb59', '2019-10-09 14:24:32'),
(218, 1, '90.3660873', '23.7743675', 'f645a8cb39d5fb59', '2019-10-09 14:25:32'),
(219, 1, '90.3660873', '23.7743675', 'f645a8cb39d5fb59', '2019-10-09 14:26:32'),
(220, 1, '90.3660938', '23.7742525', 'f645a8cb39d5fb59', '2019-10-09 14:28:07'),
(221, 1, '90.3660938', '23.7742525', 'f645a8cb39d5fb59', '2019-10-09 14:28:32'),
(222, 1, '90.3660938', '23.7742525', 'f645a8cb39d5fb59', '2019-10-09 14:29:33'),
(223, 1, '90.3660938', '23.7742525', 'f645a8cb39d5fb59', '2019-10-09 14:30:32'),
(224, 1, '90.3660938', '23.7742525', 'f645a8cb39d5fb59', '2019-10-09 14:31:32'),
(225, 1, '90.3661026', '23.7742584', 'f645a8cb39d5fb59', '2019-10-09 14:32:32'),
(226, 1, '90.3661026', '23.7742584', 'f645a8cb39d5fb59', '2019-10-09 14:33:32'),
(227, 1, '90.3661026', '23.7742584', 'f645a8cb39d5fb59', '2019-10-09 14:34:35'),
(228, 1, '90.3661026', '23.7742584', 'f645a8cb39d5fb59', '2019-10-09 14:35:32'),
(229, 1, '90.3661026', '23.7742584', 'f645a8cb39d5fb59', '2019-10-09 14:36:32'),
(230, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 14:37:32'),
(231, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 14:38:35'),
(232, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 14:39:32'),
(233, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 14:40:32'),
(234, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 14:41:32'),
(235, 1, '90.3661443', '23.7740792', 'f645a8cb39d5fb59', '2019-10-09 14:42:35'),
(236, 1, '90.3661443', '23.7740792', 'f645a8cb39d5fb59', '2019-10-09 14:43:32'),
(237, 1, '90.3661443', '23.7740792', 'f645a8cb39d5fb59', '2019-10-09 14:44:32'),
(238, 1, '90.3661443', '23.7740792', 'f645a8cb39d5fb59', '2019-10-09 14:45:32'),
(239, 1, '90.3661443', '23.7740792', 'f645a8cb39d5fb59', '2019-10-09 14:46:32'),
(240, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 14:47:33'),
(241, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 14:48:32'),
(242, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 14:49:32'),
(243, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 14:50:32'),
(244, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 14:51:32'),
(245, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 14:52:32'),
(246, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 14:53:32'),
(247, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 14:54:32'),
(248, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 14:55:32'),
(249, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 14:56:32'),
(250, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 14:57:32'),
(251, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 14:58:32'),
(252, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 14:59:32'),
(253, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 15:00:32'),
(254, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 15:01:32'),
(255, 1, '90.3661413', '23.774082', 'f645a8cb39d5fb59', '2019-10-09 15:02:32'),
(256, 1, '90.3661413', '23.774082', 'f645a8cb39d5fb59', '2019-10-09 15:03:32'),
(257, 1, '90.3661413', '23.774082', 'f645a8cb39d5fb59', '2019-10-09 15:04:32'),
(258, 1, '90.3661413', '23.774082', 'f645a8cb39d5fb59', '2019-10-09 15:05:32'),
(259, 1, '90.3661413', '23.774082', 'f645a8cb39d5fb59', '2019-10-09 15:06:32'),
(260, 1, '90.3661413', '23.774082', 'f645a8cb39d5fb59', '2019-10-09 15:07:32'),
(261, 1, '90.3661413', '23.774082', 'f645a8cb39d5fb59', '2019-10-09 15:08:32'),
(262, 1, '90.3661413', '23.774082', 'f645a8cb39d5fb59', '2019-10-09 15:09:32'),
(263, 1, '90.3661413', '23.774082', 'f645a8cb39d5fb59', '2019-10-09 15:10:32'),
(264, 1, '90.3661413', '23.774082', 'f645a8cb39d5fb59', '2019-10-09 15:11:32'),
(265, 1, '90.3661114', '23.7742358', 'f645a8cb39d5fb59', '2019-10-09 15:13:07'),
(266, 1, '90.3661114', '23.7742358', 'f645a8cb39d5fb59', '2019-10-09 15:13:32'),
(267, 1, '90.3661114', '23.7742358', 'f645a8cb39d5fb59', '2019-10-09 15:14:32'),
(268, 1, '90.3661114', '23.7742358', 'f645a8cb39d5fb59', '2019-10-09 15:15:32'),
(269, 1, '90.3661114', '23.7742358', 'f645a8cb39d5fb59', '2019-10-09 15:16:32'),
(270, 1, '90.3661114', '23.7742358', 'f645a8cb39d5fb59', '2019-10-09 15:17:32'),
(271, 1, '90.3661114', '23.7742358', 'f645a8cb39d5fb59', '2019-10-09 15:18:32'),
(272, 1, '90.3661114', '23.7742358', 'f645a8cb39d5fb59', '2019-10-09 15:19:32'),
(273, 1, '90.3661114', '23.7742358', 'f645a8cb39d5fb59', '2019-10-09 15:20:32'),
(274, 1, '90.3661114', '23.7742358', 'f645a8cb39d5fb59', '2019-10-09 15:21:32'),
(275, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 15:22:32'),
(276, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 15:23:33'),
(277, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 15:24:32'),
(278, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 15:25:32'),
(279, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 15:26:32'),
(280, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 15:27:32'),
(281, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 15:28:32'),
(282, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 15:29:32'),
(283, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 15:30:32'),
(284, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 15:31:32'),
(285, 1, '90.3660979', '23.7742942', 'f645a8cb39d5fb59', '2019-10-09 15:32:32'),
(286, 1, '90.3660979', '23.7742942', 'f645a8cb39d5fb59', '2019-10-09 15:33:32'),
(287, 1, '90.3660979', '23.7742942', 'f645a8cb39d5fb59', '2019-10-09 15:34:09'),
(288, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 15:34:18'),
(289, 1, '90.3661024', '23.7742756', 'f645a8cb39d5fb59', '2019-10-09 15:35:10'),
(290, 1, '90.3661108', '23.7742385', 'f645a8cb39d5fb59', '2019-10-09 15:36:10'),
(291, 1, '90.3661037', '23.7742344', 'f645a8cb39d5fb59', '2019-10-09 15:37:11'),
(292, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 15:38:10'),
(293, 1, '90.3661112', '23.7742368', 'f645a8cb39d5fb59', '2019-10-09 15:39:10'),
(294, 1, '90.3660286', '23.77431', 'f645a8cb39d5fb59', '2019-10-09 15:40:11'),
(295, 1, '90.3661025', '23.7743032', 'f645a8cb39d5fb59', '2019-10-09 15:41:11'),
(296, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 15:42:11'),
(297, 1, '90.3660976', '23.7742956', 'f645a8cb39d5fb59', '2019-10-09 15:43:11'),
(298, 1, '90.366074', '23.774331', 'f645a8cb39d5fb59', '2019-10-09 15:44:31'),
(299, 1, '90.3661031', '23.774261', 'f645a8cb39d5fb59', '2019-10-09 15:44:38'),
(300, 1, '90.3660769', '23.774286', 'f645a8cb39d5fb59', '2019-10-09 15:45:32'),
(301, 1, '90.3661114', '23.7742361', 'f645a8cb39d5fb59', '2019-10-09 15:46:32'),
(302, 1, '90.3660729', '23.7742883', 'f645a8cb39d5fb59', '2019-10-09 15:47:33'),
(303, 1, '90.3660876', '23.7742844', 'f645a8cb39d5fb59', '2019-10-09 15:48:32'),
(304, 1, '90.3660982', '23.7742905', 'f645a8cb39d5fb59', '2019-10-09 15:49:32'),
(305, 1, '90.366111', '23.7742377', 'f645a8cb39d5fb59', '2019-10-09 15:50:32'),
(306, 1, '90.3661087', '23.7742578', 'f645a8cb39d5fb59', '2019-10-09 15:51:32'),
(307, 1, '90.3660934', '23.7743402', 'f645a8cb39d5fb59', '2019-10-09 15:52:32'),
(308, 1, '90.3661009', '23.7743071', 'f645a8cb39d5fb59', '2019-10-09 15:53:32'),
(309, 1, '90.3660913', '23.7743072', 'f645a8cb39d5fb59', '2019-10-09 15:54:32'),
(310, 1, '90.3660913', '23.7743072', 'f645a8cb39d5fb59', '2019-10-09 15:55:32'),
(311, 1, '90.3660894', '23.774343', 'f645a8cb39d5fb59', '2019-10-09 15:56:32'),
(312, 1, '90.3660894', '23.774343', 'f645a8cb39d5fb59', '2019-10-09 15:57:32'),
(313, 1, '90.3660894', '23.774343', 'f645a8cb39d5fb59', '2019-10-09 15:58:32'),
(314, 1, '90.3660894', '23.774343', 'f645a8cb39d5fb59', '2019-10-09 15:59:32'),
(315, 1, '90.3660894', '23.774343', 'f645a8cb39d5fb59', '2019-10-09 16:00:32'),
(316, 1, '90.3660887', '23.7743387', 'f645a8cb39d5fb59', '2019-10-09 16:01:32'),
(317, 1, '90.3660887', '23.7743387', 'f645a8cb39d5fb59', '2019-10-09 16:02:32'),
(318, 1, '90.3660887', '23.7743387', 'f645a8cb39d5fb59', '2019-10-09 16:03:32'),
(319, 1, '90.3660887', '23.7743387', 'f645a8cb39d5fb59', '2019-10-09 16:04:35'),
(320, 1, '90.3660887', '23.7743387', 'f645a8cb39d5fb59', '2019-10-09 16:05:32'),
(321, 1, '90.3660881', '23.7743447', 'f645a8cb39d5fb59', '2019-10-09 16:06:32'),
(322, 1, '90.3660881', '23.7743447', 'f645a8cb39d5fb59', '2019-10-09 16:07:33'),
(323, 1, '90.3660881', '23.7743447', 'f645a8cb39d5fb59', '2019-10-09 16:08:32'),
(324, 1, '90.366084', '23.7741681', 'f645a8cb39d5fb59', '2019-10-09 16:09:32'),
(325, 1, '90.3661116', '23.7742354', 'f645a8cb39d5fb59', '2019-10-09 16:10:32'),
(326, 1, '90.3660937', '23.7743602', 'f645a8cb39d5fb59', '2019-10-09 16:11:32'),
(327, 1, '90.3660917', '23.7743614', 'f645a8cb39d5fb59', '2019-10-09 16:12:35'),
(328, 1, '90.3661159', '23.7742178', 'f645a8cb39d5fb59', '2019-10-09 16:13:33'),
(329, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 16:14:33'),
(330, 1, '90.3660621', '23.7745589', 'f645a8cb39d5fb59', '2019-10-09 16:15:42'),
(331, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 16:16:02'),
(332, 1, '90.3661351', '23.7741675', 'f645a8cb39d5fb59', '2019-10-09 16:16:42'),
(333, 1, '90.3661097', '23.774258', 'f645a8cb39d5fb59', '2019-10-09 16:17:42'),
(334, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 16:18:42'),
(335, 1, '90.3661352', '23.7741668', 'f645a8cb39d5fb59', '2019-10-09 16:19:42'),
(336, 1, '90.3661352', '23.7741668', 'f645a8cb39d5fb59', '2019-10-09 16:20:42'),
(337, 1, '90.3661352', '23.7741668', 'f645a8cb39d5fb59', '2019-10-09 16:21:18'),
(338, 1, '90.366097', '23.7743021', 'f645a8cb39d5fb59', '2019-10-09 16:21:32'),
(339, 1, '90.366097', '23.7743014', 'f645a8cb39d5fb59', '2019-10-09 16:22:00'),
(340, 1, '90.3661089', '23.7742567', 'f645a8cb39d5fb59', '2019-10-09 16:24:21'),
(341, 1, '90.366108', '23.7742142', 'f645a8cb39d5fb59', '2019-10-09 16:24:23'),
(342, 1, '90.366108', '23.7742142', 'f645a8cb39d5fb59', '2019-10-09 16:24:29'),
(343, 1, '90.3660737', '23.7745426', 'f645a8cb39d5fb59', '2019-10-09 16:25:21'),
(344, 1, '90.3661105', '23.7742562', 'f645a8cb39d5fb59', '2019-10-09 16:26:21'),
(345, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 16:26:41'),
(346, 1, '90.3661166', '23.774242', 'f645a8cb39d5fb59', '2019-10-09 16:27:02'),
(347, 1, '90.3661166', '23.774242', 'f645a8cb39d5fb59', '2019-10-09 16:27:22'),
(348, 1, '90.3660888', '23.7743541', 'f645a8cb39d5fb59', '2019-10-09 16:28:36'),
(349, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 16:28:47'),
(350, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 16:28:49'),
(351, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 16:29:34'),
(352, 1, '90.366103', '23.7742575', 'f645a8cb39d5fb59', '2019-10-09 16:29:51'),
(353, 1, '90.3660818', '23.7742425', 'f645a8cb39d5fb59', '2019-10-09 16:30:11'),
(354, 1, '90.3660818', '23.7742425', 'f645a8cb39d5fb59', '2019-10-09 16:30:46'),
(355, 1, '90.3661029', '23.7742575', 'f645a8cb39d5fb59', '2019-10-09 16:30:59'),
(356, 1, '90.3660973', '23.774298', 'f645a8cb39d5fb59', '2019-10-09 16:31:19'),
(357, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 16:31:59'),
(358, 1, '90.366111', '23.7742375', 'f645a8cb39d5fb59', '2019-10-09 16:32:59'),
(359, 1, '90.3660859', '23.7742454', 'f645a8cb39d5fb59', '2019-10-09 16:33:56'),
(360, 1, '90.366089', '23.7743535', 'f645a8cb39d5fb59', '2019-10-09 16:34:16'),
(361, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 16:34:57'),
(362, 1, '90.366103', '23.7742574', 'f645a8cb39d5fb59', '2019-10-09 16:34:58'),
(363, 1, '90.3661108', '23.7742408', 'f645a8cb39d5fb59', '2019-10-09 16:36:32'),
(364, 1, '90.3660901', '23.7743651', 'f645a8cb39d5fb59', '2019-10-09 16:37:32'),
(365, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 16:38:32'),
(366, 1, '90.3661114', '23.7742361', 'f645a8cb39d5fb59', '2019-10-09 16:39:32'),
(367, 1, '90.3661154', '23.7742297', 'f645a8cb39d5fb59', '2019-10-09 16:40:32'),
(368, 1, '90.3660912', '23.7743627', 'f645a8cb39d5fb59', '2019-10-09 16:41:32'),
(369, 1, '90.3660962', '23.7742428', 'f645a8cb39d5fb59', '2019-10-09 16:42:32'),
(370, 1, '90.3660787', '23.7742497', 'f645a8cb39d5fb59', '2019-10-09 16:43:32'),
(371, 1, '90.366103', '23.7742574', 'f645a8cb39d5fb59', '2019-10-09 16:44:32'),
(372, 1, '90.3661088', '23.7742576', 'f645a8cb39d5fb59', '2019-10-09 16:45:32'),
(373, 1, '90.3661113', '23.7742362', 'f645a8cb39d5fb59', '2019-10-09 16:46:32'),
(374, 1, '90.3661113', '23.7742362', 'f645a8cb39d5fb59', '2019-10-09 16:47:34'),
(375, 1, '90.3660887', '23.7743337', 'f645a8cb39d5fb59', '2019-10-09 16:47:56'),
(376, 1, '90.3660887', '23.7743337', 'f645a8cb39d5fb59', '2019-10-09 16:49:31'),
(377, 1, '90.3660887', '23.7743337', 'f645a8cb39d5fb59', '2019-10-09 16:49:33'),
(378, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 16:50:11'),
(379, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 16:50:32'),
(380, 1, '90.3660149', '23.7743781', 'f645a8cb39d5fb59', '2019-10-09 16:51:17'),
(381, 1, '90.3660783', '23.7742388', 'f645a8cb39d5fb59', '2019-10-09 16:51:27'),
(382, 1, '90.3660783', '23.7742388', 'f645a8cb39d5fb59', '2019-10-09 16:51:29'),
(383, 1, '90.3660863', '23.7744443', 'f645a8cb39d5fb59', '2019-10-09 16:52:17'),
(384, 1, '90.3660677', '23.7743256', 'f645a8cb39d5fb59', '2019-10-09 16:53:09'),
(385, 1, '90.3661031', '23.7742571', 'f645a8cb39d5fb59', '2019-10-09 16:53:19'),
(386, 1, '90.3661031', '23.7742571', 'f645a8cb39d5fb59', '2019-10-09 16:53:29'),
(387, 1, '90.3661031', '23.7742571', 'f645a8cb39d5fb59', '2019-10-09 16:54:01'),
(388, 1, '90.3660965', '23.7742662', 'f645a8cb39d5fb59', '2019-10-09 16:54:08'),
(389, 1, '90.3660965', '23.7742662', 'f645a8cb39d5fb59', '2019-10-09 16:54:21'),
(390, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 16:54:58'),
(391, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 16:55:18'),
(392, 1, '90.3661006', '23.7743118', 'f645a8cb39d5fb59', '2019-10-09 16:55:58'),
(393, 1, '90.3660901', '23.7743284', 'f645a8cb39d5fb59', '2019-10-09 16:57:32'),
(394, 1, '90.3661111', '23.7742374', 'f645a8cb39d5fb59', '2019-10-09 16:58:32'),
(395, 1, '90.3661114', '23.7742362', 'f645a8cb39d5fb59', '2019-10-09 16:59:32'),
(396, 1, '90.3660984', '23.774288', 'f645a8cb39d5fb59', '2019-10-09 17:00:32'),
(397, 1, '90.3660621', '23.7745589', 'f645a8cb39d5fb59', '2019-10-09 17:01:32'),
(398, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 17:02:32'),
(399, 1, '90.3661028', '23.7742619', 'f645a8cb39d5fb59', '2019-10-09 17:03:50'),
(400, 1, '90.3661115', '23.7742386', 'f645a8cb39d5fb59', '2019-10-09 17:03:55'),
(401, 1, '90.3661115', '23.7742386', 'f645a8cb39d5fb59', '2019-10-09 17:03:57'),
(402, 1, '90.366094', '23.7743304', 'f645a8cb39d5fb59', '2019-10-09 17:04:50'),
(403, 1, '90.3660939', '23.7742212', 'f645a8cb39d5fb59', '2019-10-09 17:05:34'),
(404, 1, '90.3660939', '23.7742212', 'f645a8cb39d5fb59', '2019-10-09 17:05:50'),
(405, 1, '90.3660893', '23.7743323', 'f645a8cb39d5fb59', '2019-10-09 17:06:50'),
(406, 1, '90.3660959', '23.7743618', 'f645a8cb39d5fb59', '2019-10-09 17:07:50'),
(407, 1, '90.3660766', '23.7743072', 'f645a8cb39d5fb59', '2019-10-09 17:08:50'),
(408, 1, '90.366099', '23.7743403', 'f645a8cb39d5fb59', '2019-10-09 17:09:50'),
(409, 1, '90.3661148', '23.7742321', 'f645a8cb39d5fb59', '2019-10-09 17:10:50'),
(410, 1, '90.3660819', '23.7742921', 'f645a8cb39d5fb59', '2019-10-09 17:11:50'),
(411, 1, '90.3660819', '23.7742921', 'f645a8cb39d5fb59', '2019-10-09 17:12:20'),
(412, 1, '90.366103', '23.7742574', 'f645a8cb39d5fb59', '2019-10-09 17:12:26'),
(413, 1, '90.366103', '23.7742574', 'f645a8cb39d5fb59', '2019-10-09 17:12:40'),
(414, 1, '90.3660989', '23.7742434', 'f645a8cb39d5fb59', '2019-10-09 17:13:20'),
(415, 1, '90.366098', '23.7743043', 'f645a8cb39d5fb59', '2019-10-09 17:14:32'),
(416, 1, '90.3661278', '23.7741625', 'f645a8cb39d5fb59', '2019-10-09 17:15:32'),
(417, 1, '90.3661118', '23.7742562', 'f645a8cb39d5fb59', '2019-10-09 17:16:32'),
(418, 1, '90.3661113', '23.7742365', 'f645a8cb39d5fb59', '2019-10-09 17:17:52'),
(419, 1, '90.3660928', '23.7743609', 'f645a8cb39d5fb59', '2019-10-09 17:18:32'),
(420, 1, '90.3661393', '23.774116', 'f645a8cb39d5fb59', '2019-10-09 17:19:32'),
(421, 1, '90.3660972', '23.7741266', 'f645a8cb39d5fb59', '2019-10-09 17:20:32'),
(422, 1, '90.366112', '23.7742335', 'f645a8cb39d5fb59', '2019-10-09 17:21:32'),
(423, 1, '90.36615', '23.7740688', 'f645a8cb39d5fb59', '2019-10-09 17:22:33'),
(424, 1, '90.3661112', '23.7742366', 'f645a8cb39d5fb59', '2019-10-09 17:22:42'),
(425, 1, '90.3661112', '23.7742366', 'f645a8cb39d5fb59', '2019-10-09 17:23:57'),
(426, 1, '90.3661029', '23.7742576', 'f645a8cb39d5fb59', '2019-10-09 17:24:06'),
(427, 1, '90.3661029', '23.7742576', 'f645a8cb39d5fb59', '2019-10-09 17:24:20'),
(428, 1, '90.3661029', '23.7742576', 'f645a8cb39d5fb59', '2019-10-09 17:25:06'),
(429, 1, '90.3660621', '23.7745589', 'f645a8cb39d5fb59', '2019-10-09 17:25:12'),
(430, 1, '90.3660621', '23.7745589', 'f645a8cb39d5fb59', '2019-10-09 17:25:26'),
(431, 1, '90.3661221', '23.7742912', 'f645a8cb39d5fb59', '2019-10-10 10:34:28'),
(432, 1, '90.3663131', '23.7739891', 'f645a8cb39d5fb59', '2019-10-10 10:34:41'),
(433, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 10:35:37'),
(434, 1, '90.3662322', '23.774123', 'f645a8cb39d5fb59', '2019-10-10 10:36:35'),
(435, 1, '90.3661344', '23.7742538', 'f645a8cb39d5fb59', '2019-10-10 10:37:29'),
(436, 1, '90.3661299', '23.7741655', 'f645a8cb39d5fb59', '2019-10-10 10:38:34'),
(437, 1, '90.366197', '23.7741411', 'f645a8cb39d5fb59', '2019-10-10 10:39:34'),
(438, 1, '90.3662099', '23.774122', 'f645a8cb39d5fb59', '2019-10-10 10:40:29'),
(439, 1, '90.3662314', '23.774091', 'f645a8cb39d5fb59', '2019-10-10 10:41:29'),
(440, 1, '90.3663131', '23.7739891', 'f645a8cb39d5fb59', '2019-10-10 10:43:16'),
(441, 1, '90.3663131', '23.7739891', 'f645a8cb39d5fb59', '2019-10-10 10:43:20'),
(442, 1, '90.3661812', '23.7742963', 'f645a8cb39d5fb59', '2019-10-10 10:44:16'),
(443, 1, '90.3662314', '23.774091', 'f645a8cb39d5fb59', '2019-10-10 10:45:16'),
(444, 1, '90.366224', '23.7741015', 'f645a8cb39d5fb59', '2019-10-10 10:46:34'),
(445, 1, '90.3661243', '23.7742287', 'f645a8cb39d5fb59', '2019-10-10 10:47:34'),
(446, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 10:48:34'),
(447, 1, '90.3663131', '23.7739891', 'f645a8cb39d5fb59', '2019-10-10 10:49:16'),
(448, 1, '90.3662099', '23.774122', 'f645a8cb39d5fb59', '2019-10-10 10:50:12'),
(449, 1, '90.3661471', '23.7741128', 'f645a8cb39d5fb59', '2019-10-10 10:50:16'),
(450, 1, '90.3663131', '23.7739891', 'f645a8cb39d5fb59', '2019-10-10 10:51:14'),
(451, 1, '90.3661835', '23.774084', 'f645a8cb39d5fb59', '2019-10-10 10:52:14'),
(452, 1, '90.3662168', '23.7741119', 'f645a8cb39d5fb59', '2019-10-10 10:53:58'),
(453, 1, '90.3663131', '23.7739891', 'f645a8cb39d5fb59', '2019-10-10 10:54:18'),
(454, 1, '90.3661458', '23.7741439', 'f645a8cb39d5fb59', '2019-10-10 10:54:58'),
(455, 1, '90.3661921', '23.7740983', 'f645a8cb39d5fb59', '2019-10-10 10:56:34'),
(456, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 10:57:34'),
(457, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 10:58:34'),
(458, 1, '90.3661921', '23.7740983', 'f645a8cb39d5fb59', '2019-10-10 10:59:15'),
(459, 1, '90.3660926', '23.7742973', 'f645a8cb39d5fb59', '2019-10-10 10:59:58'),
(460, 1, '90.3662453', '23.7743933', 'f645a8cb39d5fb59', '2019-10-10 11:01:38'),
(461, 1, '90.3661297', '23.7743399', 'f645a8cb39d5fb59', '2019-10-10 11:02:18'),
(462, 1, '90.3661561', '23.7742435', 'f645a8cb39d5fb59', '2019-10-10 11:03:38'),
(463, 1, '90.3661896', '23.7743383', 'f645a8cb39d5fb59', '2019-10-10 11:04:34'),
(464, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-10 11:04:58'),
(465, 1, '90.3662181', '23.7741437', 'f645a8cb39d5fb59', '2019-10-10 11:06:14'),
(466, 1, '90.3662119', '23.7742992', 'f645a8cb39d5fb59', '2019-10-10 11:07:34'),
(467, 1, '90.3661282', '23.7743728', 'f645a8cb39d5fb59', '2019-10-10 11:08:34'),
(468, 1, '90.3661536', '23.7744095', 'f645a8cb39d5fb59', '2019-10-10 11:09:34'),
(469, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 11:10:34'),
(470, 1, '90.3661183', '23.7744256', 'f645a8cb39d5fb59', '2019-10-10 11:11:34'),
(471, 1, '90.3661324', '23.7743424', 'f645a8cb39d5fb59', '2019-10-10 11:12:34'),
(472, 1, '90.3660921', '23.7742916', 'f645a8cb39d5fb59', '2019-10-10 11:13:34'),
(473, 1, '90.3661271', '23.77441', 'f645a8cb39d5fb59', '2019-10-10 11:14:34'),
(474, 1, '90.3661159', '23.77441', 'f645a8cb39d5fb59', '2019-10-10 11:15:34'),
(475, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 11:16:34'),
(476, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 11:17:36'),
(477, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 11:18:34'),
(478, 1, '90.3661333', '23.7743903', 'f645a8cb39d5fb59', '2019-10-10 11:18:58'),
(479, 1, '90.3661333', '23.7743903', 'f645a8cb39d5fb59', '2019-10-10 11:20:34'),
(480, 1, '90.3661333', '23.7743903', 'f645a8cb39d5fb59', '2019-10-10 11:21:34'),
(481, 1, '90.3661333', '23.7743903', 'f645a8cb39d5fb59', '2019-10-10 11:22:34'),
(482, 1, '90.3661333', '23.7743903', 'f645a8cb39d5fb59', '2019-10-10 11:23:37'),
(483, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 11:24:38'),
(484, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 11:25:34'),
(485, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 11:26:34'),
(486, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 11:27:34'),
(487, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 11:28:09'),
(488, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 11:29:34'),
(489, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 11:30:23'),
(490, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 11:30:34'),
(491, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 11:31:23'),
(492, 1, '90.3661127', '23.7744212', 'f645a8cb39d5fb59', '2019-10-10 11:32:42'),
(493, 1, '90.3661344', '23.7742538', 'f645a8cb39d5fb59', '2019-10-10 11:33:02'),
(494, 1, '90.3661159', '23.7744052', 'f645a8cb39d5fb59', '2019-10-10 11:33:40'),
(495, 1, '90.3661138', '23.7744309', 'f645a8cb39d5fb59', '2019-10-10 11:33:50'),
(496, 1, '90.366309', '23.7740058', 'f645a8cb39d5fb59', '2019-10-10 11:34:40'),
(497, 1, '90.3661161', '23.7744143', 'f645a8cb39d5fb59', '2019-10-10 11:36:00'),
(498, 1, '90.3660792', '23.7744322', 'f645a8cb39d5fb59', '2019-10-10 11:36:41'),
(499, 1, '90.3661', '23.774406', 'f645a8cb39d5fb59', '2019-10-10 11:37:41'),
(500, 1, '90.3660986', '23.7744039', 'f645a8cb39d5fb59', '2019-10-10 11:38:41'),
(501, 1, '90.3660979', '23.7744057', 'f645a8cb39d5fb59', '2019-10-10 11:39:41'),
(502, 1, '90.3661232', '23.7742877', 'f645a8cb39d5fb59', '2019-10-10 11:41:04'),
(503, 1, '90.3660668', '23.7744887', 'f645a8cb39d5fb59', '2019-10-10 11:42:01'),
(504, 1, '90.3661008', '23.7744106', 'f645a8cb39d5fb59', '2019-10-10 11:42:41'),
(505, 1, '90.3661009', '23.7744105', 'f645a8cb39d5fb59', '2019-10-10 11:43:41'),
(506, 1, '90.3661007', '23.7743979', 'f645a8cb39d5fb59', '2019-10-10 11:44:41'),
(507, 1, '90.3660945', '23.7744358', 'f645a8cb39d5fb59', '2019-10-10 11:45:41'),
(508, 1, '90.3661105', '23.7743321', 'f645a8cb39d5fb59', '2019-10-10 11:46:40'),
(509, 1, '90.3661105', '23.7743321', 'f645a8cb39d5fb59', '2019-10-10 11:48:04'),
(510, 1, '90.3661105', '23.7743321', 'f645a8cb39d5fb59', '2019-10-10 11:48:40'),
(511, 1, '90.3661105', '23.7743321', 'f645a8cb39d5fb59', '2019-10-10 11:49:40'),
(512, 1, '90.3661105', '23.7743321', 'f645a8cb39d5fb59', '2019-10-10 11:50:40'),
(513, 1, '90.366108', '23.7743771', 'f645a8cb39d5fb59', '2019-10-10 11:51:45'),
(514, 1, '90.366108', '23.7743771', 'f645a8cb39d5fb59', '2019-10-10 11:52:40'),
(515, 1, '90.366108', '23.7743771', 'f645a8cb39d5fb59', '2019-10-10 11:54:11'),
(516, 1, '90.366108', '23.7743771', 'f645a8cb39d5fb59', '2019-10-10 11:55:04'),
(517, 1, '90.3661159', '23.77441', 'f645a8cb39d5fb59', '2019-10-10 11:55:40'),
(518, 1, '90.3661159', '23.77441', 'f645a8cb39d5fb59', '2019-10-10 11:56:40'),
(519, 1, '90.3661159', '23.77441', 'f645a8cb39d5fb59', '2019-10-10 11:57:40'),
(520, 1, '90.3661159', '23.77441', 'f645a8cb39d5fb59', '2019-10-10 11:58:40'),
(521, 1, '90.3661159', '23.77441', 'f645a8cb39d5fb59', '2019-10-10 11:59:40'),
(522, 1, '90.3661172', '23.7744007', 'f645a8cb39d5fb59', '2019-10-10 12:00:40'),
(523, 1, '90.3661172', '23.7744007', 'f645a8cb39d5fb59', '2019-10-10 12:01:57'),
(524, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-10 12:02:16'),
(525, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-10 12:03:06'),
(526, 1, '90.3663108', '23.7739987', 'f645a8cb39d5fb59', '2019-10-10 12:03:26'),
(527, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 12:04:06'),
(528, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-10 12:05:34'),
(529, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 12:06:47'),
(530, 1, '90.3661342', '23.7743277', 'f645a8cb39d5fb59', '2019-10-10 12:07:47'),
(531, 1, '90.3661342', '23.7743277', 'f645a8cb39d5fb59', '2019-10-10 12:08:07'),
(532, 1, '90.3661442', '23.7743722', 'f645a8cb39d5fb59', '2019-10-10 12:09:34'),
(533, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 12:10:34'),
(534, 1, '90.3661023', '23.7744801', 'f645a8cb39d5fb59', '2019-10-10 12:11:30'),
(535, 1, '90.3661403', '23.7743837', 'f645a8cb39d5fb59', '2019-10-10 12:11:34'),
(536, 1, '90.366171', '23.7743367', 'f645a8cb39d5fb59', '2019-10-10 12:12:34'),
(537, 1, '90.36621', '23.7741706', 'f645a8cb39d5fb59', '2019-10-10 12:14:10'),
(538, 1, '90.3661186', '23.7743958', 'f645a8cb39d5fb59', '2019-10-10 12:14:34'),
(539, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 12:15:30'),
(540, 1, '90.3661143', '23.7744526', 'f645a8cb39d5fb59', '2019-10-10 12:16:34'),
(541, 1, '90.3661186', '23.7743127', 'f645a8cb39d5fb59', '2019-10-10 12:17:23'),
(542, 1, '90.3662387', '23.7740005', 'f645a8cb39d5fb59', '2019-10-10 12:17:57'),
(543, 1, '90.3661176', '23.774401', 'f645a8cb39d5fb59', '2019-10-10 12:18:17'),
(544, 1, '90.3661176', '23.774401', 'f645a8cb39d5fb59', '2019-10-10 12:18:47'),
(545, 1, '90.3661204', '23.7743903', 'f645a8cb39d5fb59', '2019-10-10 12:19:07'),
(546, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 12:20:12'),
(547, 1, '90.3661434', '23.7744132', 'f645a8cb39d5fb59', '2019-10-10 12:20:32'),
(548, 1, '90.3661115', '23.774469', 'f645a8cb39d5fb59', '2019-10-10 12:21:12'),
(549, 1, '90.3661358', '23.7743135', 'f645a8cb39d5fb59', '2019-10-10 12:22:34'),
(550, 1, '90.3661896', '23.7743383', 'f645a8cb39d5fb59', '2019-10-10 12:23:34'),
(551, 1, '90.3660869', '23.7745107', 'f645a8cb39d5fb59', '2019-10-10 12:24:30'),
(552, 1, '90.3661144', '23.7743861', 'f645a8cb39d5fb59', '2019-10-10 12:25:35'),
(553, 1, '90.3661144', '23.7743861', 'f645a8cb39d5fb59', '2019-10-10 12:26:34'),
(554, 1, '90.3661144', '23.7743861', 'f645a8cb39d5fb59', '2019-10-10 12:27:34'),
(555, 1, '90.3661144', '23.7743861', 'f645a8cb39d5fb59', '2019-10-10 12:28:12'),
(556, 1, '90.3661144', '23.7743861', 'f645a8cb39d5fb59', '2019-10-10 12:29:12'),
(557, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 12:30:34'),
(558, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 12:31:34'),
(559, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 12:32:34'),
(560, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 12:33:34'),
(561, 1, '90.3661671', '23.7743629', 'f645a8cb39d5fb59', '2019-10-10 12:34:34'),
(562, 1, '90.3661671', '23.7743629', 'f645a8cb39d5fb59', '2019-10-10 12:35:34'),
(563, 1, '90.3661671', '23.7743629', 'f645a8cb39d5fb59', '2019-10-10 12:36:34'),
(564, 1, '90.3661671', '23.7743629', 'f645a8cb39d5fb59', '2019-10-10 12:37:34'),
(565, 1, '90.3661671', '23.7743629', 'f645a8cb39d5fb59', '2019-10-10 12:38:34'),
(566, 1, '90.3661719', '23.7742178', 'f645a8cb39d5fb59', '2019-10-10 12:39:34'),
(567, 1, '90.3661719', '23.7742178', 'f645a8cb39d5fb59', '2019-10-10 13:16:15'),
(568, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 13:16:18'),
(569, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 13:17:15'),
(570, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-10 13:18:15'),
(571, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-10 13:19:34'),
(572, 1, '90.3660858', '23.7744094', 'f645a8cb39d5fb59', '2019-10-10 13:20:34'),
(573, 1, '90.366099', '23.7744907', 'f645a8cb39d5fb59', '2019-10-10 13:21:34'),
(574, 1, '90.3661356', '23.7743339', 'f645a8cb39d5fb59', '2019-10-10 13:22:34'),
(575, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 13:23:34'),
(576, 1, '90.3661118', '23.7744775', 'f645a8cb39d5fb59', '2019-10-10 13:24:36'),
(577, 1, '90.3661342', '23.7743277', 'f645a8cb39d5fb59', '2019-10-10 13:25:34'),
(578, 1, '90.3661342', '23.7743277', 'f645a8cb39d5fb59', '2019-10-10 13:26:34'),
(579, 1, '90.3660927', '23.7742833', 'f645a8cb39d5fb59', '2019-10-10 13:27:34'),
(580, 1, '90.3660927', '23.7742833', 'f645a8cb39d5fb59', '2019-10-10 13:28:34'),
(581, 1, '90.3660927', '23.7742833', 'f645a8cb39d5fb59', '2019-10-10 13:29:34'),
(582, 1, '90.3660927', '23.7742833', 'f645a8cb39d5fb59', '2019-10-10 13:30:37'),
(583, 1, '90.3660898', '23.774524', 'f645a8cb39d5fb59', '2019-10-10 13:31:15'),
(584, 1, '90.3660898', '23.774524', 'f645a8cb39d5fb59', '2019-10-10 13:32:15'),
(585, 1, '90.3660898', '23.774524', 'f645a8cb39d5fb59', '2019-10-10 13:33:34'),
(586, 1, '90.3660898', '23.774524', 'f645a8cb39d5fb59', '2019-10-10 13:34:15'),
(587, 1, '90.3660898', '23.774524', 'f645a8cb39d5fb59', '2019-10-10 13:35:15'),
(588, 1, '90.3661342', '23.7743277', 'f645a8cb39d5fb59', '2019-10-10 13:36:34'),
(589, 1, '90.3661342', '23.7743277', 'f645a8cb39d5fb59', '2019-10-10 13:37:34'),
(590, 1, '90.3661342', '23.7743277', 'f645a8cb39d5fb59', '2019-10-10 13:38:37'),
(591, 1, '90.3661342', '23.7743277', 'f645a8cb39d5fb59', '2019-10-10 13:39:34'),
(592, 1, '90.3660825', '23.774528', 'f645a8cb39d5fb59', '2019-10-10 13:40:35'),
(593, 1, '90.3660825', '23.774528', 'f645a8cb39d5fb59', '2019-10-10 13:41:34'),
(594, 1, '90.3660825', '23.774528', 'f645a8cb39d5fb59', '2019-10-10 13:42:34'),
(595, 1, '90.3660825', '23.774528', 'f645a8cb39d5fb59', '2019-10-10 13:43:34'),
(596, 1, '90.3660825', '23.774528', 'f645a8cb39d5fb59', '2019-10-10 13:44:34'),
(597, 1, '90.3661527', '23.7742529', 'f645a8cb39d5fb59', '2019-10-10 13:45:34'),
(598, 1, '90.3661527', '23.7742529', 'f645a8cb39d5fb59', '2019-10-10 13:46:34'),
(599, 1, '90.3661527', '23.7742529', 'f645a8cb39d5fb59', '2019-10-10 13:47:34'),
(600, 1, '90.3661527', '23.7742529', 'f645a8cb39d5fb59', '2019-10-10 13:48:34'),
(601, 1, '90.3661527', '23.7742529', 'f645a8cb39d5fb59', '2019-10-10 13:49:34'),
(602, 1, '90.3660959', '23.7742849', 'f645a8cb39d5fb59', '2019-10-10 13:50:35'),
(603, 1, '90.3660959', '23.7742849', 'f645a8cb39d5fb59', '2019-10-10 13:51:34'),
(604, 1, '90.3660959', '23.7742849', 'f645a8cb39d5fb59', '2019-10-10 13:52:34'),
(605, 1, '90.3661634', '23.7743433', 'f645a8cb39d5fb59', '2019-10-10 13:53:38'),
(606, 1, '90.3660754', '23.7745201', 'f645a8cb39d5fb59', '2019-10-10 13:54:38'),
(607, 1, '90.3660702', '23.7744507', 'f645a8cb39d5fb59', '2019-10-10 13:55:38'),
(608, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 13:56:34'),
(609, 1, '90.3660858', '23.7744094', 'f645a8cb39d5fb59', '2019-10-10 13:57:34'),
(610, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 13:58:34'),
(611, 1, '90.3660858', '23.7744094', 'f645a8cb39d5fb59', '2019-10-10 13:59:34'),
(612, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-10 14:00:34'),
(613, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 14:01:34'),
(614, 1, '90.3661192', '23.7742972', 'f645a8cb39d5fb59', '2019-10-10 14:02:34'),
(615, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 14:03:34'),
(616, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 14:04:34'),
(617, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 14:05:34'),
(618, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 14:06:34'),
(619, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 14:07:34'),
(620, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 14:08:34'),
(621, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 14:09:34'),
(622, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 14:10:34'),
(623, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 14:11:34'),
(624, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 14:12:34'),
(625, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 14:13:34'),
(626, 1, '90.3662925', '23.7741646', 'f645a8cb39d5fb59', '2019-10-10 14:14:37'),
(627, 1, '90.3662925', '23.7741646', 'f645a8cb39d5fb59', '2019-10-10 14:15:34'),
(628, 1, '90.3662925', '23.7741646', 'f645a8cb39d5fb59', '2019-10-10 14:16:34'),
(629, 1, '90.3662925', '23.7741646', 'f645a8cb39d5fb59', '2019-10-10 14:17:34'),
(630, 1, '90.3662925', '23.7741646', 'f645a8cb39d5fb59', '2019-10-10 14:18:34'),
(631, 1, '90.3662127', '23.7741584', 'f645a8cb39d5fb59', '2019-10-10 14:19:34'),
(632, 1, '90.3662127', '23.7741584', 'f645a8cb39d5fb59', '2019-10-10 14:20:37'),
(633, 1, '90.3662127', '23.7741584', 'f645a8cb39d5fb59', '2019-10-10 14:21:34'),
(634, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 14:22:10'),
(635, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 14:22:18'),
(636, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 14:23:10'),
(637, 1, '90.366111', '23.7744696', 'f645a8cb39d5fb59', '2019-10-10 14:24:38'),
(638, 1, '90.3661108', '23.7744699', 'f645a8cb39d5fb59', '2019-10-10 14:25:50'),
(639, 1, '90.3661393', '23.7743804', 'f645a8cb39d5fb59', '2019-10-10 14:26:50'),
(640, 1, '90.3661032', '23.7742891', 'f645a8cb39d5fb59', '2019-10-10 14:27:34'),
(641, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 14:28:10'),
(642, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 14:29:10'),
(643, 1, '90.3662073', '23.7741836', 'f645a8cb39d5fb59', '2019-10-10 14:30:34'),
(644, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-10 14:31:50'),
(645, 1, '90.3661709', '23.7743473', 'f645a8cb39d5fb59', '2019-10-10 14:32:50'),
(646, 1, '90.3661709', '23.7743473', 'f645a8cb39d5fb59', '2019-10-10 14:33:10');
INSERT INTO `usr_location` (`id`, `usr_id`, `loc_long`, `loc_lati`, `loc_imei`, `loc_date_time`) VALUES
(647, 1, '90.3661515', '23.7741477', 'f645a8cb39d5fb59', '2019-10-10 14:34:34'),
(648, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-10 14:35:30'),
(649, 1, '90.366178', '23.7743827', 'f645a8cb39d5fb59', '2019-10-10 14:36:10'),
(650, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-10 14:37:39'),
(651, 1, '90.3661752', '23.7745033', 'f645a8cb39d5fb59', '2019-10-10 14:38:34'),
(652, 1, '90.3660799', '23.7745269', 'f645a8cb39d5fb59', '2019-10-10 14:39:34'),
(653, 1, '90.3660799', '23.7745269', 'f645a8cb39d5fb59', '2019-10-10 14:40:35'),
(654, 1, '90.3660799', '23.7745269', 'f645a8cb39d5fb59', '2019-10-10 14:41:34'),
(655, 1, '90.3660799', '23.7745269', 'f645a8cb39d5fb59', '2019-10-10 14:42:34'),
(656, 1, '90.3660799', '23.7745269', 'f645a8cb39d5fb59', '2019-10-10 14:43:24'),
(657, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-10 14:44:37'),
(658, 1, '90.3661855', '23.7747067', 'f645a8cb39d5fb59', '2019-10-10 14:45:37'),
(659, 1, '90.3661015', '23.7743117', 'f645a8cb39d5fb59', '2019-10-10 14:46:34'),
(660, 1, '90.366124', '23.7744609', 'f645a8cb39d5fb59', '2019-10-10 14:47:34'),
(661, 1, '90.3660799', '23.7745269', 'f645a8cb39d5fb59', '2019-10-10 14:48:34'),
(662, 1, '90.3662365', '23.7746184', 'f645a8cb39d5fb59', '2019-10-10 14:49:34'),
(663, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 14:49:53'),
(664, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 14:50:34'),
(665, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 14:51:35'),
(666, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 14:52:34'),
(667, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 14:53:34'),
(668, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 14:54:34'),
(669, 1, '90.3660974', '23.7742946', 'f645a8cb39d5fb59', '2019-10-10 14:55:34'),
(670, 1, '90.3660974', '23.7742946', 'f645a8cb39d5fb59', '2019-10-10 14:56:34'),
(671, 1, '90.3660974', '23.7742946', 'f645a8cb39d5fb59', '2019-10-10 14:57:34'),
(672, 1, '90.3660974', '23.7742946', 'f645a8cb39d5fb59', '2019-10-10 14:58:34'),
(673, 1, '90.3660974', '23.7742946', 'f645a8cb39d5fb59', '2019-10-10 15:00:04'),
(674, 1, '90.3662127', '23.7741584', 'f645a8cb39d5fb59', '2019-10-10 15:00:23'),
(675, 1, '90.3662127', '23.7741584', 'f645a8cb39d5fb59', '2019-10-10 15:00:54'),
(676, 1, '90.3660974', '23.7742946', 'f645a8cb39d5fb59', '2019-10-10 15:01:14'),
(677, 1, '90.3662127', '23.7741584', 'f645a8cb39d5fb59', '2019-10-10 15:01:57'),
(678, 1, '90.3662047', '23.7741973', 'f645a8cb39d5fb59', '2019-10-10 15:03:17'),
(679, 1, '90.3661324', '23.7743424', 'f645a8cb39d5fb59', '2019-10-10 15:04:34'),
(680, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-10 15:04:55'),
(681, 1, '90.3661515', '23.7741477', 'f645a8cb39d5fb59', '2019-10-10 15:06:34'),
(682, 1, '90.3661515', '23.7741477', 'f645a8cb39d5fb59', '2019-10-10 15:06:55'),
(683, 1, '90.3660793', '23.7741306', 'f645a8cb39d5fb59', '2019-10-10 15:08:37'),
(684, 1, '90.36621', '23.7741706', 'f645a8cb39d5fb59', '2019-10-10 15:09:34'),
(685, 1, '90.3662073', '23.7741836', 'f645a8cb39d5fb59', '2019-10-10 15:10:44'),
(686, 1, '90.3662073', '23.7741836', 'f645a8cb39d5fb59', '2019-10-10 15:10:54'),
(687, 1, '90.3662073', '23.7741836', 'f645a8cb39d5fb59', '2019-10-10 15:11:24'),
(688, 1, '90.3662073', '23.7741836', 'f645a8cb39d5fb59', '2019-10-10 15:11:26'),
(689, 1, '90.3662073', '23.7741836', 'f645a8cb39d5fb59', '2019-10-10 15:12:24'),
(690, 1, '90.3662073', '23.7741836', 'f645a8cb39d5fb59', '2019-10-10 15:13:46'),
(691, 1, '90.3662073', '23.7741836', 'f645a8cb39d5fb59', '2019-10-10 15:14:34'),
(692, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 15:15:34'),
(693, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 15:16:34'),
(694, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 15:17:51'),
(695, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 15:18:34'),
(696, 1, '90.36621', '23.7741706', 'f645a8cb39d5fb59', '2019-10-10 15:18:59'),
(697, 1, '90.36621', '23.7741706', 'f645a8cb39d5fb59', '2019-10-10 15:19:34'),
(698, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-10 15:20:34'),
(699, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-10 15:21:34'),
(700, 1, '90.3661219', '23.7744911', 'f645a8cb39d5fb59', '2019-10-10 15:22:34'),
(701, 1, '90.3661202', '23.7744187', 'f645a8cb39d5fb59', '2019-10-10 15:23:35'),
(702, 1, '90.3661342', '23.7743277', 'f645a8cb39d5fb59', '2019-10-10 15:24:36'),
(703, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-10 15:25:34'),
(704, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-10 15:26:34'),
(705, 1, '90.3661747', '23.7741488', 'f645a8cb39d5fb59', '2019-10-10 15:27:29'),
(706, 1, '90.36621', '23.7741706', 'f645a8cb39d5fb59', '2019-10-10 15:27:49'),
(707, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-10 15:28:34'),
(708, 1, '90.3662073', '23.7741836', 'f645a8cb39d5fb59', '2019-10-10 15:29:49'),
(709, 1, '90.3662127', '23.7741584', 'f645a8cb39d5fb59', '2019-10-10 15:30:06'),
(710, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-10 15:30:46'),
(711, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-10 15:31:46'),
(712, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 15:32:47'),
(713, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-10 15:33:47'),
(714, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-10 15:34:12'),
(715, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 15:34:22'),
(716, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 15:34:23'),
(717, 1, '90.3661896', '23.7743383', 'f645a8cb39d5fb59', '2019-10-10 15:35:12'),
(718, 1, '90.3661747', '23.77433', 'f645a8cb39d5fb59', '2019-10-10 15:36:11'),
(719, 1, '90.3661324', '23.7743424', 'f645a8cb39d5fb59', '2019-10-10 15:36:34'),
(720, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 15:37:34'),
(721, 1, '90.3661023', '23.7744801', 'f645a8cb39d5fb59', '2019-10-10 15:38:12'),
(722, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-10 15:39:34'),
(723, 1, '90.3661218', '23.7744211', 'f645a8cb39d5fb59', '2019-10-10 15:40:35'),
(724, 1, '90.3661358', '23.7743135', 'f645a8cb39d5fb59', '2019-10-10 15:41:34'),
(725, 1, '90.3661747', '23.7741488', 'f645a8cb39d5fb59', '2019-10-10 15:42:34'),
(726, 1, '90.3661896', '23.7743383', 'f645a8cb39d5fb59', '2019-10-10 15:43:34'),
(727, 1, '90.3661988', '23.7742693', 'f645a8cb39d5fb59', '2019-10-10 15:44:34'),
(728, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 15:45:34'),
(729, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-10 15:46:34'),
(730, 1, '90.3661324', '23.7743424', 'f645a8cb39d5fb59', '2019-10-10 15:47:34'),
(731, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-10 15:48:36'),
(732, 1, '90.3661078', '23.7743004', 'f645a8cb39d5fb59', '2019-10-10 15:49:34'),
(733, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 15:50:34'),
(734, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 15:51:34'),
(735, 1, '90.3660903', '23.7743199', 'f645a8cb39d5fb59', '2019-10-10 15:52:34'),
(736, 1, '90.3661283', '23.7744396', 'f645a8cb39d5fb59', '2019-10-10 15:53:34'),
(737, 1, '90.3661393', '23.7744101', 'f645a8cb39d5fb59', '2019-10-10 15:54:34'),
(738, 1, '90.3661393', '23.7744101', 'f645a8cb39d5fb59', '2019-10-10 15:55:34'),
(739, 1, '90.3661393', '23.7744101', 'f645a8cb39d5fb59', '2019-10-10 15:56:34'),
(740, 1, '90.3661393', '23.7744101', 'f645a8cb39d5fb59', '2019-10-10 15:57:34'),
(741, 1, '90.3661393', '23.7744101', 'f645a8cb39d5fb59', '2019-10-10 15:58:34'),
(742, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 15:59:34'),
(743, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 16:00:34'),
(744, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 16:01:12'),
(745, 1, '90.3661342', '23.7743277', 'f645a8cb39d5fb59', '2019-10-10 16:02:48'),
(746, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 16:03:34'),
(747, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 16:04:48'),
(748, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 16:05:34'),
(749, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 16:06:34'),
(750, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 16:07:34'),
(751, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 16:08:49'),
(752, 1, '90.3661527', '23.7743045', 'f645a8cb39d5fb59', '2019-10-10 16:09:34'),
(753, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 16:10:14'),
(754, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 16:10:49'),
(755, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-10 16:11:37'),
(756, 1, '90.3661513', '23.7743985', 'f645a8cb39d5fb59', '2019-10-10 16:12:34'),
(757, 1, '90.3660576', '23.7745543', 'f645a8cb39d5fb59', '2019-10-10 16:13:49'),
(758, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 16:14:58'),
(759, 1, '90.366098', '23.7742862', 'f645a8cb39d5fb59', '2019-10-10 16:15:07'),
(760, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 16:15:58'),
(761, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 16:16:22'),
(762, 1, '90.3661413', '23.774346', 'f645a8cb39d5fb59', '2019-10-10 16:16:58'),
(763, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-10 16:17:58'),
(764, 1, '90.3661844', '23.774309', 'f645a8cb39d5fb59', '2019-10-10 16:18:58'),
(765, 1, '90.3661433', '23.7743584', 'f645a8cb39d5fb59', '2019-10-10 16:20:34'),
(766, 1, '90.3660542', '23.7744112', 'f645a8cb39d5fb59', '2019-10-10 16:21:34'),
(767, 1, '90.3661848', '23.7741076', 'f645a8cb39d5fb59', '2019-10-10 16:22:34'),
(768, 1, '90.3661237', '23.7742588', 'f645a8cb39d5fb59', '2019-10-10 16:23:34'),
(769, 1, '90.3661462', '23.7743369', 'f645a8cb39d5fb59', '2019-10-10 16:24:34'),
(770, 1, '90.3662624', '23.7741383', 'f645a8cb39d5fb59', '2019-10-10 16:24:58'),
(771, 1, '90.3661371', '23.7742978', 'f645a8cb39d5fb59', '2019-10-10 16:25:58'),
(772, 1, '90.3661396', '23.7744098', 'f645a8cb39d5fb59', '2019-10-10 16:27:34'),
(773, 1, '90.3660927', '23.7742833', 'f645a8cb39d5fb59', '2019-10-10 16:28:34'),
(774, 1, '90.3660927', '23.7742833', 'f645a8cb39d5fb59', '2019-10-10 16:29:34'),
(775, 1, '90.3660927', '23.7742833', 'f645a8cb39d5fb59', '2019-10-10 16:30:34'),
(776, 1, '90.3660927', '23.7742833', 'f645a8cb39d5fb59', '2019-10-10 16:31:34'),
(777, 1, '90.3660927', '23.7742833', 'f645a8cb39d5fb59', '2019-10-10 16:32:34'),
(778, 1, '90.3660601', '23.7743058', 'f645a8cb39d5fb59', '2019-10-10 16:33:34'),
(779, 1, '90.3660601', '23.7743058', 'f645a8cb39d5fb59', '2019-10-10 16:34:34'),
(780, 1, '90.3660601', '23.7743058', 'f645a8cb39d5fb59', '2019-10-10 16:35:34'),
(781, 1, '90.3660601', '23.7743058', 'f645a8cb39d5fb59', '2019-10-10 16:36:34'),
(782, 1, '90.3660601', '23.7743058', 'f645a8cb39d5fb59', '2019-10-10 16:37:34'),
(783, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 16:38:14'),
(784, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-10 16:39:34'),
(785, 1, '90.3661896', '23.7743383', 'f645a8cb39d5fb59', '2019-10-10 16:40:34'),
(786, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-10 16:41:34'),
(787, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-10 16:42:34'),
(788, 1, '90.3662509', '23.7741854', 'f645a8cb39d5fb59', '2019-10-10 16:43:34'),
(789, 1, '90.3663131', '23.7739891', 'f645a8cb39d5fb59', '2019-10-10 16:44:34'),
(790, 1, '90.3660959', '23.7742849', 'f645a8cb39d5fb59', '2019-10-10 16:45:34'),
(791, 1, '90.3662592', '23.774157', 'f645a8cb39d5fb59', '2019-10-10 16:46:34'),
(792, 1, '90.3661361', '23.7741468', 'f645a8cb39d5fb59', '2019-10-10 16:47:37'),
(793, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 16:48:35'),
(794, 1, '90.3659245', '23.774471', 'f645a8cb39d5fb59', '2019-10-10 16:49:34'),
(795, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 16:50:34'),
(796, 1, '90.3661085', '23.7742919', 'f645a8cb39d5fb59', '2019-10-10 16:51:34'),
(797, 1, '90.366098', '23.7742862', 'f645a8cb39d5fb59', '2019-10-10 16:52:34'),
(798, 1, '90.3660916', '23.7744466', 'f645a8cb39d5fb59', '2019-10-10 16:53:34'),
(799, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 16:54:34'),
(800, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 16:55:34'),
(801, 1, '90.3661479', '23.7743426', 'f645a8cb39d5fb59', '2019-10-10 16:56:34'),
(802, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-10 16:57:34'),
(803, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-10 16:58:34'),
(804, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 16:58:58'),
(805, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 16:59:58'),
(806, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 17:00:58'),
(807, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 17:01:58'),
(808, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 17:02:58'),
(809, 1, '90.366157', '23.7743264', 'f645a8cb39d5fb59', '2019-10-10 17:03:52'),
(810, 1, '90.3662127', '23.7741584', 'f645a8cb39d5fb59', '2019-10-10 17:04:01'),
(811, 1, '90.3661896', '23.7743383', 'f645a8cb39d5fb59', '2019-10-10 17:04:53'),
(812, 1, '90.3660536', '23.7745035', 'f645a8cb39d5fb59', '2019-10-10 17:06:34'),
(813, 1, '90.3660536', '23.7745035', 'f645a8cb39d5fb59', '2019-10-10 17:06:54'),
(814, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 17:08:34'),
(815, 1, '90.3660862', '23.7744662', 'f645a8cb39d5fb59', '2019-10-10 17:09:34'),
(816, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 17:10:34'),
(817, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 17:10:54'),
(818, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 17:11:54'),
(819, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 17:12:55'),
(820, 1, '90.3660815', '23.7744527', 'f645a8cb39d5fb59', '2019-10-10 17:14:05'),
(821, 1, '90.3660664', '23.7744679', 'f645a8cb39d5fb59', '2019-10-10 17:14:11'),
(822, 1, '90.3660664', '23.7744679', 'f645a8cb39d5fb59', '2019-10-10 17:14:24'),
(823, 1, '90.3661358', '23.7743135', 'f645a8cb39d5fb59', '2019-10-10 17:15:28'),
(824, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-10 17:15:34'),
(825, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-10 17:15:39'),
(826, 1, '90.3660953', '23.7743232', 'f645a8cb39d5fb59', '2019-10-10 17:17:11'),
(827, 1, '90.3661186', '23.7743127', 'f645a8cb39d5fb59', '2019-10-10 17:17:27'),
(828, 1, '90.3661186', '23.7743127', 'f645a8cb39d5fb59', '2019-10-10 17:17:34'),
(829, 1, '90.3662047', '23.7741973', 'f645a8cb39d5fb59', '2019-10-10 17:18:31'),
(830, 1, '90.3660823', '23.7743001', 'f645a8cb39d5fb59', '2019-10-10 17:18:34'),
(831, 1, '90.3660823', '23.7743001', 'f645a8cb39d5fb59', '2019-10-10 17:19:08'),
(832, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-10 17:19:48'),
(833, 1, '90.3661593', '23.774148', 'f645a8cb39d5fb59', '2019-10-10 17:20:34'),
(834, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-10 17:21:34'),
(835, 1, '90.366183', '23.774523', 'f645a8cb39d5fb59', '2019-10-10 17:22:34'),
(836, 1, '90.3661438', '23.7741473', 'f645a8cb39d5fb59', '2019-10-10 17:23:36'),
(837, 1, '90.3662127', '23.7741584', 'f645a8cb39d5fb59', '2019-10-10 17:24:36'),
(838, 1, '90.3660964', '23.7745194', 'f645a8cb39d5fb59', '2019-10-10 17:25:36'),
(839, 1, '90.3662127', '23.7741584', 'f645a8cb39d5fb59', '2019-10-10 17:26:36'),
(840, 1, '90.3661956', '23.7742313', 'f645a8cb39d5fb59', '2019-10-10 17:27:34'),
(841, 1, '90.3661282', '23.774316', 'f645a8cb39d5fb59', '2019-10-10 17:28:34'),
(842, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-10 17:30:09'),
(843, 1, '90.3661896', '23.7743383', 'f645a8cb39d5fb59', '2019-10-10 17:30:46'),
(844, 1, '90.3662098', '23.7743052', 'f645a8cb39d5fb59', '2019-10-10 17:31:46'),
(845, 1, '90.3662127', '23.7741584', 'f645a8cb39d5fb59', '2019-10-10 17:32:34'),
(846, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-10 17:33:34'),
(847, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 17:34:34'),
(848, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 17:35:34'),
(849, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-10 17:36:34'),
(850, 1, '90.3661896', '23.7743383', 'f645a8cb39d5fb59', '2019-10-10 17:37:34'),
(851, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-10 17:38:34'),
(852, 1, '90.3661896', '23.7743383', 'f645a8cb39d5fb59', '2019-10-10 17:39:34'),
(853, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 17:40:34'),
(854, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-10 17:41:11'),
(855, 1, '90.3662127', '23.7741584', 'f645a8cb39d5fb59', '2019-10-10 17:41:51'),
(856, 1, '90.3661173', '23.7744797', 'f645a8cb39d5fb59', '2019-10-10 17:42:51'),
(857, 1, '90.3661527', '23.7742529', 'f645a8cb39d5fb59', '2019-10-10 17:43:52'),
(858, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-10 17:44:34'),
(859, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-13 10:40:44'),
(860, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 10:41:28'),
(861, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 10:42:25'),
(862, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 10:47:25'),
(863, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-13 10:52:28'),
(864, 1, '90.3662082', '23.7741898', '88c9ebcc1cbdf2bd', '2019-10-13 10:57:50'),
(865, 1, '90.366107', '23.7744758', '88c9ebcc1cbdf2bd', '2019-10-13 10:58:03'),
(866, 1, '90.366107', '23.7744758', '88c9ebcc1cbdf2bd', '2019-10-13 10:58:26'),
(867, 1, '90.3661066', '23.7744765', '88c9ebcc1cbdf2bd', '2019-10-13 10:59:06'),
(868, 1, '90.3661896', '23.7743383', '88c9ebcc1cbdf2bd', '2019-10-13 11:00:07'),
(869, 1, '90.3661066', '23.7744765', '88c9ebcc1cbdf2bd', '2019-10-13 11:01:25'),
(870, 1, '90.3663988', '23.7739194', '88c9ebcc1cbdf2bd', '2019-10-13 11:02:05'),
(871, 1, '90.3662144', '23.7741511', '88c9ebcc1cbdf2bd', '2019-10-13 11:03:05'),
(872, 1, '90.3662144', '23.7741511', '88c9ebcc1cbdf2bd', '2019-10-13 11:04:05'),
(873, 1, '90.3662144', '23.7741511', '88c9ebcc1cbdf2bd', '2019-10-13 11:05:05'),
(874, 1, '90.3661412', '23.7743081', '88c9ebcc1cbdf2bd', '2019-10-13 11:06:06'),
(875, 1, '90.3661371', '23.7742978', '88c9ebcc1cbdf2bd', '2019-10-13 11:07:09'),
(876, 1, '90.3662127', '23.7741584', '88c9ebcc1cbdf2bd', '2019-10-13 11:08:06'),
(877, 1, '90.3662144', '23.7741511', '88c9ebcc1cbdf2bd', '2019-10-13 11:09:06'),
(878, 1, '90.3662073', '23.7741836', '88c9ebcc1cbdf2bd', '2019-10-13 11:10:06'),
(879, 1, '90.3661328', '23.7743919', '88c9ebcc1cbdf2bd', '2019-10-13 11:11:06'),
(880, 1, '90.3662073', '23.7741836', '88c9ebcc1cbdf2bd', '2019-10-13 11:11:57'),
(881, 1, '90.3662073', '23.7741836', '88c9ebcc1cbdf2bd', '2019-10-13 11:11:58'),
(882, 1, '90.3662073', '23.7741836', '88c9ebcc1cbdf2bd', '2019-10-13 11:12:11'),
(883, 1, '90.3662073', '23.7741836', '88c9ebcc1cbdf2bd', '2019-10-13 11:12:31'),
(884, 1, '90.36621', '23.7741706', '88c9ebcc1cbdf2bd', '2019-10-13 11:13:00'),
(885, 1, '90.36621', '23.7741706', '88c9ebcc1cbdf2bd', '2019-10-13 11:13:21'),
(886, 1, '90.3661567', '23.7742906', '88c9ebcc1cbdf2bd', '2019-10-13 11:14:05'),
(887, 1, '90.3661367', '23.7743048', '88c9ebcc1cbdf2bd', '2019-10-13 11:15:02'),
(888, 1, '90.3661382', '23.7743328', '88c9ebcc1cbdf2bd', '2019-10-13 11:16:02'),
(889, 1, '90.3662431', '23.7741656', '88c9ebcc1cbdf2bd', '2019-10-13 11:17:23'),
(890, 1, '90.3662502', '23.7741725', '88c9ebcc1cbdf2bd', '2019-10-13 11:18:03'),
(891, 1, '90.36621', '23.7741706', '88c9ebcc1cbdf2bd', '2019-10-13 11:19:03'),
(892, 1, '90.3661367', '23.7743048', '88c9ebcc1cbdf2bd', '2019-10-13 11:20:04'),
(893, 1, '90.3661367', '23.7743048', '88c9ebcc1cbdf2bd', '2019-10-13 11:21:01'),
(894, 1, '90.3662073', '23.7741836', '88c9ebcc1cbdf2bd', '2019-10-13 11:22:22'),
(895, 1, '90.3662144', '23.7741511', '88c9ebcc1cbdf2bd', '2019-10-13 11:23:02'),
(896, 1, '90.3662073', '23.7741836', '88c9ebcc1cbdf2bd', '2019-10-13 11:24:05'),
(897, 1, '90.3661937', '23.7742767', '88c9ebcc1cbdf2bd', '2019-10-13 11:25:05'),
(898, 1, '90.3662073', '23.7741836', '88c9ebcc1cbdf2bd', '2019-10-13 11:26:26'),
(899, 1, '90.3661367', '23.7743048', '88c9ebcc1cbdf2bd', '2019-10-13 11:27:06'),
(900, 1, '90.3661105', '23.774485', 'f645a8cb39d5fb59', '2019-10-13 11:29:05'),
(901, 1, '90.3661362', '23.7743065', 'f645a8cb39d5fb59', '2019-10-13 11:29:08'),
(902, 1, '90.3661362', '23.7743065', 'f645a8cb39d5fb59', '2019-10-13 11:29:17'),
(903, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 11:30:31'),
(904, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 11:31:11'),
(905, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 11:32:11'),
(906, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 11:33:32'),
(907, 1, '90.3663131', '23.7739891', 'f645a8cb39d5fb59', '2019-10-13 11:34:06'),
(908, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-13 11:35:31'),
(909, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 11:36:31'),
(910, 1, '90.3659996', '23.7746195', 'f645a8cb39d5fb59', '2019-10-13 11:37:45'),
(911, 1, '90.3659996', '23.7746195', 'f645a8cb39d5fb59', '2019-10-13 11:38:05'),
(912, 1, '90.3661342', '23.7743277', 'f645a8cb39d5fb59', '2019-10-13 11:39:06'),
(913, 1, '90.3660552', '23.7745136', 'f645a8cb39d5fb59', '2019-10-13 11:40:31'),
(914, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 11:41:26'),
(915, 1, '90.3660799', '23.7745269', 'f645a8cb39d5fb59', '2019-10-13 11:42:31'),
(916, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 11:43:06'),
(917, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 11:44:31'),
(918, 1, '90.3660799', '23.7745269', 'f645a8cb39d5fb59', '2019-10-13 11:45:31'),
(919, 1, '90.3660796', '23.7744248', 'f645a8cb39d5fb59', '2019-10-13 11:46:35'),
(920, 1, '90.3660796', '23.7744248', 'f645a8cb39d5fb59', '2019-10-13 11:47:31'),
(921, 1, '90.3660796', '23.7744248', 'f645a8cb39d5fb59', '2019-10-13 11:48:05'),
(922, 1, '90.3660796', '23.7744248', 'f645a8cb39d5fb59', '2019-10-13 11:49:05'),
(923, 1, '90.3660775', '23.7744413', 'f645a8cb39d5fb59', '2019-10-13 11:51:07'),
(924, 1, '90.3660555', '23.7745309', 'f645a8cb39d5fb59', '2019-10-13 11:51:14'),
(925, 1, '90.3660555', '23.7745309', 'f645a8cb39d5fb59', '2019-10-13 11:51:26'),
(926, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-13 11:52:06'),
(927, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 11:52:41'),
(928, 1, '90.3660555', '23.7745278', 'f645a8cb39d5fb59', '2019-10-13 11:53:01'),
(929, 1, '90.3660713', '23.7745271', 'f645a8cb39d5fb59', '2019-10-13 11:53:36'),
(930, 1, '90.3660713', '23.7745271', 'f645a8cb39d5fb59', '2019-10-13 11:53:57'),
(931, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 11:54:07'),
(932, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 11:54:14'),
(933, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 11:54:28'),
(934, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 11:55:22'),
(935, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 11:55:34'),
(936, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 11:56:06'),
(937, 1, '90.3660667', '23.7744613', 'f645a8cb39d5fb59', '2019-10-13 11:56:31'),
(938, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 11:57:31'),
(939, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 11:58:29'),
(940, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 11:58:38'),
(941, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 11:58:40'),
(942, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:00:01'),
(943, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 12:00:07'),
(944, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 12:01:28'),
(945, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:01:35'),
(946, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:01:48'),
(947, 1, '90.3660927', '23.7742833', 'f645a8cb39d5fb59', '2019-10-13 12:02:31'),
(948, 1, '90.3660927', '23.7742833', 'f645a8cb39d5fb59', '2019-10-13 12:03:00'),
(949, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 12:03:06'),
(950, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 12:04:03'),
(951, 1, '90.3661046', '23.7744775', 'f645a8cb39d5fb59', '2019-10-13 12:05:02'),
(952, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 12:05:54'),
(953, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-13 12:06:14'),
(954, 1, '90.3661921', '23.7740983', 'f645a8cb39d5fb59', '2019-10-13 12:07:16'),
(955, 1, '90.3661236', '23.7744484', 'f645a8cb39d5fb59', '2019-10-13 12:07:34'),
(956, 1, '90.3661483', '23.7744685', 'f645a8cb39d5fb59', '2019-10-13 12:08:13'),
(957, 1, '90.3661257', '23.7744365', 'f645a8cb39d5fb59', '2019-10-13 12:09:13'),
(958, 1, '90.3661764', '23.7743124', 'f645a8cb39d5fb59', '2019-10-13 12:10:02'),
(959, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:10:31'),
(960, 1, '90.3660595', '23.7744852', 'f645a8cb39d5fb59', '2019-10-13 12:11:31'),
(961, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:12:18'),
(962, 1, '90.3661242', '23.7743308', 'f645a8cb39d5fb59', '2019-10-13 12:13:31'),
(963, 1, '90.3660831', '23.7744636', 'f645a8cb39d5fb59', '2019-10-13 12:14:13'),
(964, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-13 12:15:31'),
(965, 1, '90.3661896', '23.7743383', 'f645a8cb39d5fb59', '2019-10-13 12:15:51'),
(966, 1, '90.3660228', '23.774402', 'f645a8cb39d5fb59', '2019-10-13 12:16:31'),
(967, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 12:17:31'),
(968, 1, '90.3662127', '23.7741584', 'f645a8cb39d5fb59', '2019-10-13 12:18:54'),
(969, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:19:51'),
(970, 1, '90.3660707', '23.7742944', 'f645a8cb39d5fb59', '2019-10-13 12:20:32'),
(971, 1, '90.3660516', '23.7741556', 'f645a8cb39d5fb59', '2019-10-13 12:21:31'),
(972, 1, '90.3660516', '23.7741556', 'f645a8cb39d5fb59', '2019-10-13 12:23:04'),
(973, 1, '90.3660516', '23.7741556', 'f645a8cb39d5fb59', '2019-10-13 12:23:31'),
(974, 1, '90.3660516', '23.7741556', 'f645a8cb39d5fb59', '2019-10-13 12:24:31'),
(975, 1, '90.3660516', '23.7741556', 'f645a8cb39d5fb59', '2019-10-13 12:25:31'),
(976, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:27:26'),
(977, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 12:27:30'),
(978, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 12:27:59'),
(979, 1, '90.3660699', '23.7744741', 'f645a8cb39d5fb59', '2019-10-13 12:28:08'),
(980, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:28:31'),
(981, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:29:50'),
(982, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:30:09'),
(983, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:30:54'),
(984, 1, '90.3660701', '23.7745281', 'f645a8cb39d5fb59', '2019-10-13 12:31:03'),
(985, 1, '90.3660701', '23.7745281', 'f645a8cb39d5fb59', '2019-10-13 12:31:13'),
(986, 1, '90.3660701', '23.7745281', 'f645a8cb39d5fb59', '2019-10-13 12:31:26'),
(987, 1, '90.3660799', '23.7745269', 'f645a8cb39d5fb59', '2019-10-13 12:33:20'),
(988, 1, '90.36621', '23.7741706', 'f645a8cb39d5fb59', '2019-10-13 12:33:22'),
(989, 1, '90.36621', '23.7741706', 'f645a8cb39d5fb59', '2019-10-13 12:34:07'),
(990, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:34:27'),
(991, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:34:49'),
(992, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:35:13'),
(993, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:36:50'),
(994, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:37:58'),
(995, 1, '90.3661864', '23.7741863', 'f645a8cb39d5fb59', '2019-10-13 12:38:15'),
(996, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:38:39'),
(997, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:39:06'),
(998, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:39:37'),
(999, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 12:39:58'),
(1000, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 12:40:00'),
(1001, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:40:38'),
(1002, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-13 12:41:38'),
(1003, 1, '90.3661032', '23.7742891', 'f645a8cb39d5fb59', '2019-10-13 12:42:50'),
(1004, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 12:43:06'),
(1005, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 12:43:18'),
(1006, 1, '90.3660733', '23.7744545', 'f645a8cb39d5fb59', '2019-10-13 12:44:02'),
(1007, 1, '90.3660733', '23.7744545', 'f645a8cb39d5fb59', '2019-10-13 12:45:12'),
(1008, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-13 12:45:31'),
(1009, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:46:12'),
(1010, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:46:14'),
(1011, 1, '90.3661896', '23.7743383', 'f645a8cb39d5fb59', '2019-10-13 12:47:12'),
(1012, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:48:31'),
(1013, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 12:49:31'),
(1014, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 12:51:12'),
(1015, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:51:31'),
(1016, 1, '90.3661195', '23.7743472', 'f645a8cb39d5fb59', '2019-10-13 12:52:13'),
(1017, 1, '90.3660996', '23.7743626', 'f645a8cb39d5fb59', '2019-10-13 12:52:36'),
(1018, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:52:54'),
(1019, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:53:26'),
(1020, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:53:32'),
(1021, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:53:46'),
(1022, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:54:26'),
(1023, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:55:31'),
(1024, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:56:31'),
(1025, 1, '90.3661342', '23.7743277', 'f645a8cb39d5fb59', '2019-10-13 12:57:31'),
(1026, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:58:31'),
(1027, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 12:59:31'),
(1028, 1, '90.3661342', '23.7743277', 'f645a8cb39d5fb59', '2019-10-13 13:00:22'),
(1029, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 13:00:31'),
(1030, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 13:00:33'),
(1031, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-13 13:02:19'),
(1032, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 13:02:39'),
(1033, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 13:04:24'),
(1034, 1, '90.3660748', '23.7744606', 'f645a8cb39d5fb59', '2019-10-13 13:04:29'),
(1035, 1, '90.3660748', '23.7744606', 'f645a8cb39d5fb59', '2019-10-13 13:04:43'),
(1036, 1, '90.3660748', '23.7744606', 'f645a8cb39d5fb59', '2019-10-13 13:04:45'),
(1037, 1, '90.3661358', '23.7743135', 'f645a8cb39d5fb59', '2019-10-13 13:05:34'),
(1038, 1, '90.3660761', '23.7745186', 'f645a8cb39d5fb59', '2019-10-13 13:05:36'),
(1039, 1, '90.3660761', '23.7745186', 'f645a8cb39d5fb59', '2019-10-13 13:05:40'),
(1040, 1, '90.3660761', '23.7745186', 'f645a8cb39d5fb59', '2019-10-13 13:05:54'),
(1041, 1, '90.3661896', '23.7743383', 'f645a8cb39d5fb59', '2019-10-13 13:07:42'),
(1042, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 13:08:02'),
(1043, 1, '90.3661605', '23.7744873', 'f645a8cb39d5fb59', '2019-10-13 13:08:48'),
(1044, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 13:08:59'),
(1045, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 13:10:12'),
(1046, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 13:10:22'),
(1047, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 13:11:19'),
(1048, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 13:11:21'),
(1049, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 13:11:26'),
(1050, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 13:12:19'),
(1051, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 13:12:26'),
(1052, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 13:13:20'),
(1053, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-13 13:13:40'),
(1054, 1, '90.3660461', '23.7742521', 'f645a8cb39d5fb59', '2019-10-13 13:14:30'),
(1055, 1, '90.3660737', '23.7744457', 'f645a8cb39d5fb59', '2019-10-13 13:14:32'),
(1056, 1, '90.3660381', '23.7744148', 'f645a8cb39d5fb59', '2019-10-13 13:15:22'),
(1057, 1, '90.3660381', '23.7744148', 'f645a8cb39d5fb59', '2019-10-13 13:15:31'),
(1058, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 13:16:00'),
(1059, 1, '90.36621', '23.7741706', 'f645a8cb39d5fb59', '2019-10-13 13:16:20'),
(1060, 1, '90.3660798', '23.7745154', 'f645a8cb39d5fb59', '2019-10-13 13:17:26'),
(1061, 1, '90.3661697', '23.7743461', 'f645a8cb39d5fb59', '2019-10-13 13:17:46'),
(1062, 1, '90.3661236', '23.7744408', 'f645a8cb39d5fb59', '2019-10-13 13:20:51'),
(1063, 1, '90.3661236', '23.7744408', 'f645a8cb39d5fb59', '2019-10-13 13:21:04'),
(1064, 1, '90.3661236', '23.7744408', 'f645a8cb39d5fb59', '2019-10-13 13:21:06'),
(1065, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-13 13:22:06'),
(1066, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-13 13:23:07'),
(1067, 1, '90.3660207', '23.7742806', 'f645a8cb39d5fb59', '2019-10-13 13:24:29'),
(1068, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 13:24:51'),
(1069, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-13 13:26:07'),
(1070, 1, '90.3660438', '23.7744072', 'f645a8cb39d5fb59', '2019-10-13 13:26:28'),
(1071, 1, '90.3661358', '23.7743135', 'f645a8cb39d5fb59', '2019-10-13 13:28:51'),
(1072, 1, '90.3661358', '23.7743135', 'f645a8cb39d5fb59', '2019-10-13 13:29:01'),
(1073, 1, '90.3660733', '23.7744545', 'f645a8cb39d5fb59', '2019-10-13 13:29:08'),
(1074, 1, '90.3660733', '23.7744545', 'f645a8cb39d5fb59', '2019-10-13 13:29:21'),
(1075, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 13:30:31'),
(1076, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 13:30:32'),
(1077, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 13:30:37'),
(1078, 1, '90.3661515', '23.7741477', 'f645a8cb39d5fb59', '2019-10-13 13:36:32'),
(1079, 1, '90.3660768', '23.7742738', 'f645a8cb39d5fb59', '2019-10-13 13:36:44'),
(1080, 1, '90.3660768', '23.7742738', 'f645a8cb39d5fb59', '2019-10-13 13:36:52'),
(1081, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 13:42:13'),
(1082, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-13 13:42:21'),
(1083, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-13 13:42:32'),
(1084, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-13 13:42:34'),
(1085, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-13 13:43:32'),
(1086, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-13 13:44:31'),
(1087, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-13 13:45:32'),
(1088, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-13 13:45:58'),
(1089, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-13 13:46:14'),
(1090, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-13 13:46:16'),
(1091, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 13:52:32'),
(1092, 1, '90.3660968', '23.7744375', 'f645a8cb39d5fb59', '2019-10-13 13:53:01'),
(1093, 1, '90.3660968', '23.7744375', 'f645a8cb39d5fb59', '2019-10-13 13:53:21'),
(1094, 1, '90.366167', '23.7741485', 'f645a8cb39d5fb59', '2019-10-13 13:53:31'),
(1095, 1, '90.366167', '23.7741485', 'f645a8cb39d5fb59', '2019-10-13 13:53:51'),
(1096, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 13:54:32'),
(1097, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 13:55:15'),
(1098, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 13:56:29'),
(1099, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 13:56:50'),
(1100, 1, '90.3662248', '23.7744138', 'f645a8cb39d5fb59', '2019-10-13 13:57:31'),
(1101, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-13 13:58:31'),
(1102, 1, '90.3661107', '23.7744676', 'f645a8cb39d5fb59', '2019-10-13 13:59:31'),
(1103, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 14:00:31'),
(1104, 1, '90.3660545', '23.7745434', 'f645a8cb39d5fb59', '2019-10-13 14:01:31'),
(1105, 1, '90.3657889', '23.7745682', 'f645a8cb39d5fb59', '2019-10-13 14:02:31'),
(1106, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 14:03:31'),
(1107, 1, '90.3660767', '23.7744578', 'f645a8cb39d5fb59', '2019-10-13 14:04:31'),
(1108, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 14:05:31'),
(1109, 1, '90.3660333', '23.7745258', 'f645a8cb39d5fb59', '2019-10-13 14:06:31'),
(1110, 1, '90.3660941', '23.7744357', 'f645a8cb39d5fb59', '2019-10-13 14:07:31'),
(1111, 1, '90.3661215', '23.774459', 'f645a8cb39d5fb59', '2019-10-13 14:08:31'),
(1112, 1, '90.3661081', '23.7744759', 'f645a8cb39d5fb59', '2019-10-13 14:09:31'),
(1113, 1, '90.3661081', '23.7744759', 'f645a8cb39d5fb59', '2019-10-13 14:10:31'),
(1114, 1, '90.3661081', '23.7744759', 'f645a8cb39d5fb59', '2019-10-13 14:11:31'),
(1115, 1, '90.3661081', '23.7744759', 'f645a8cb39d5fb59', '2019-10-13 14:12:31'),
(1116, 1, '90.3661081', '23.7744759', 'f645a8cb39d5fb59', '2019-10-13 14:13:31'),
(1117, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 14:14:31'),
(1118, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 14:15:31'),
(1119, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 14:16:32'),
(1120, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 14:17:31'),
(1121, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 14:18:31'),
(1122, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 14:19:31'),
(1123, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 14:20:31'),
(1124, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 14:21:31'),
(1125, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 14:22:31'),
(1126, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 14:23:31'),
(1127, 1, '90.3663017', '23.7745323', 'f645a8cb39d5fb59', '2019-10-13 14:24:31'),
(1128, 1, '90.3663017', '23.7745323', 'f645a8cb39d5fb59', '2019-10-13 14:25:31'),
(1129, 1, '90.3663017', '23.7745323', 'f645a8cb39d5fb59', '2019-10-13 14:26:31'),
(1130, 1, '90.3663017', '23.7745323', 'f645a8cb39d5fb59', '2019-10-13 14:27:58'),
(1131, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 14:28:31'),
(1132, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 14:29:31'),
(1133, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 14:30:31'),
(1134, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 14:31:31'),
(1135, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 14:32:31'),
(1136, 1, '90.3661022', '23.7745326', 'f645a8cb39d5fb59', '2019-10-13 14:33:31'),
(1137, 1, '90.3661022', '23.7745326', 'f645a8cb39d5fb59', '2019-10-13 14:34:31'),
(1138, 1, '90.3661022', '23.7745326', 'f645a8cb39d5fb59', '2019-10-13 14:35:31'),
(1139, 1, '90.3661022', '23.7745326', 'f645a8cb39d5fb59', '2019-10-13 14:36:31'),
(1140, 1, '90.3660698', '23.7744509', 'f645a8cb39d5fb59', '2019-10-13 14:36:55'),
(1141, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-13 14:37:31'),
(1142, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-13 14:37:42'),
(1143, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 14:38:27'),
(1144, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 14:38:29'),
(1145, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 14:39:27'),
(1146, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-13 14:39:49'),
(1147, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-13 14:41:23'),
(1148, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 14:41:29'),
(1149, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 14:41:42'),
(1150, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 14:43:18'),
(1151, 1, '90.366098', '23.7742862', 'f645a8cb39d5fb59', '2019-10-13 14:43:20'),
(1152, 1, '90.366098', '23.7742862', 'f645a8cb39d5fb59', '2019-10-13 14:43:25'),
(1153, 1, '90.366098', '23.7742862', 'f645a8cb39d5fb59', '2019-10-13 14:44:44'),
(1154, 1, '90.3660733', '23.7744545', 'f645a8cb39d5fb59', '2019-10-13 14:44:52'),
(1155, 1, '90.3660733', '23.7744545', 'f645a8cb39d5fb59', '2019-10-13 14:45:04'),
(1156, 1, '90.3660733', '23.7744545', 'f645a8cb39d5fb59', '2019-10-13 14:45:37'),
(1157, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 14:45:57'),
(1158, 1, '90.3660701', '23.774457', 'f645a8cb39d5fb59', '2019-10-13 14:46:37'),
(1159, 1, '90.3660735', '23.7745231', 'f645a8cb39d5fb59', '2019-10-13 14:47:37'),
(1160, 1, '90.3660775', '23.7744413', 'f645a8cb39d5fb59', '2019-10-13 14:48:37'),
(1161, 1, '90.3661273', '23.7743676', 'f645a8cb39d5fb59', '2019-10-13 14:49:37'),
(1162, 1, '90.366123', '23.7744036', 'f645a8cb39d5fb59', '2019-10-13 14:50:37'),
(1163, 1, '90.3660927', '23.7742833', 'f645a8cb39d5fb59', '2019-10-13 14:51:37'),
(1164, 1, '90.3661342', '23.7743277', 'f645a8cb39d5fb59', '2019-10-13 14:52:38'),
(1165, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 14:53:38'),
(1166, 1, '90.3660858', '23.7744094', 'f645a8cb39d5fb59', '2019-10-13 14:54:38'),
(1167, 1, '90.3663988', '23.7739194', 'f645a8cb39d5fb59', '2019-10-13 14:55:40'),
(1168, 1, '90.3660799', '23.7745269', 'f645a8cb39d5fb59', '2019-10-13 14:55:42'),
(1169, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 14:57:09'),
(1170, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 14:57:19'),
(1171, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 14:57:39'),
(1172, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 14:59:01'),
(1173, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 14:59:09'),
(1174, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 14:59:21'),
(1175, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 14:59:45'),
(1176, 1, '90.3661087', '23.7744724', 'f645a8cb39d5fb59', '2019-10-13 15:01:31'),
(1177, 1, '90.3662516', '23.7744807', 'f645a8cb39d5fb59', '2019-10-13 15:02:31'),
(1178, 1, '90.3660985', '23.7745282', 'f645a8cb39d5fb59', '2019-10-13 15:03:31'),
(1179, 1, '90.3660711', '23.7745269', 'f645a8cb39d5fb59', '2019-10-13 15:05:37'),
(1180, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 15:05:39'),
(1181, 1, '90.3661173', '23.7744797', 'f645a8cb39d5fb59', '2019-10-13 15:07:13'),
(1182, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 15:07:33'),
(1183, 1, '90.3661173', '23.7744797', 'f645a8cb39d5fb59', '2019-10-13 15:08:04'),
(1184, 1, '90.3660661', '23.774447', 'f645a8cb39d5fb59', '2019-10-13 15:08:44'),
(1185, 1, '90.3661371', '23.7742978', 'f645a8cb39d5fb59', '2019-10-13 15:09:30'),
(1186, 1, '90.3663131', '23.7739891', 'f645a8cb39d5fb59', '2019-10-13 15:09:52'),
(1187, 1, '90.3663131', '23.7739891', 'f645a8cb39d5fb59', '2019-10-13 15:10:31'),
(1188, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 15:11:31'),
(1189, 1, '90.3661553', '23.7743522', 'f645a8cb39d5fb59', '2019-10-13 15:12:32'),
(1190, 1, '90.3661033', '23.7744723', 'f645a8cb39d5fb59', '2019-10-13 15:12:47'),
(1191, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 15:13:31'),
(1192, 1, '90.3661342', '23.7743277', 'f645a8cb39d5fb59', '2019-10-13 15:14:53'),
(1193, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 15:16:09'),
(1194, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 15:16:31'),
(1195, 1, '90.3660681', '23.7745291', 'f645a8cb39d5fb59', '2019-10-13 15:16:58'),
(1196, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 15:17:31'),
(1197, 1, '90.3661161', '23.7744836', 'f645a8cb39d5fb59', '2019-10-13 15:18:31'),
(1198, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 15:19:31'),
(1199, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 15:20:32'),
(1200, 1, '90.3660282', '23.7744536', 'f645a8cb39d5fb59', '2019-10-13 15:21:31'),
(1201, 1, '90.3660282', '23.7744536', 'f645a8cb39d5fb59', '2019-10-13 15:22:31'),
(1202, 1, '90.3660282', '23.7744536', 'f645a8cb39d5fb59', '2019-10-13 15:23:31'),
(1203, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 15:23:39'),
(1204, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 15:23:47'),
(1205, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 15:23:49'),
(1206, 1, '90.366132', '23.7744706', 'f645a8cb39d5fb59', '2019-10-13 15:24:48'),
(1207, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-13 15:25:48'),
(1208, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-13 15:26:46'),
(1209, 1, '90.3661522', '23.7742577', 'f645a8cb39d5fb59', '2019-10-13 15:27:06'),
(1210, 1, '90.3661371', '23.7742978', 'f645a8cb39d5fb59', '2019-10-13 15:27:46'),
(1211, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-13 15:28:46'),
(1212, 1, '90.3660823', '23.7743001', 'f645a8cb39d5fb59', '2019-10-13 15:29:47'),
(1213, 1, '90.3661544', '23.7741341', 'f645a8cb39d5fb59', '2019-10-13 15:30:46'),
(1214, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 15:31:46'),
(1215, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-13 15:32:46'),
(1216, 1, '90.3660799', '23.7743777', 'f645a8cb39d5fb59', '2019-10-13 15:33:47'),
(1217, 1, '90.3660967', '23.7742796', 'f645a8cb39d5fb59', '2019-10-13 15:34:46'),
(1218, 1, '90.3661527', '23.7742529', 'f645a8cb39d5fb59', '2019-10-13 15:35:46'),
(1219, 1, '90.3661527', '23.7742529', 'f645a8cb39d5fb59', '2019-10-13 15:36:46'),
(1220, 1, '90.3661527', '23.7742529', 'f645a8cb39d5fb59', '2019-10-13 15:37:46'),
(1221, 1, '90.3661527', '23.7742529', 'f645a8cb39d5fb59', '2019-10-13 15:38:46'),
(1222, 1, '90.3661527', '23.7742529', 'f645a8cb39d5fb59', '2019-10-13 15:39:46'),
(1223, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 15:40:59'),
(1224, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 15:42:18'),
(1225, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 15:43:00'),
(1226, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 15:43:46'),
(1227, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 15:45:22'),
(1228, 1, '90.366127', '23.7743992', 'f645a8cb39d5fb59', '2019-10-13 15:45:46'),
(1229, 1, '90.366127', '23.7743992', 'f645a8cb39d5fb59', '2019-10-13 15:46:46'),
(1230, 1, '90.366127', '23.7743992', 'f645a8cb39d5fb59', '2019-10-13 15:47:46'),
(1231, 1, '90.366127', '23.7743992', 'f645a8cb39d5fb59', '2019-10-13 15:48:48'),
(1232, 1, '90.366127', '23.7743992', 'f645a8cb39d5fb59', '2019-10-13 15:49:46'),
(1233, 1, '90.3661087', '23.7744732', 'f645a8cb39d5fb59', '2019-10-13 15:50:46'),
(1234, 1, '90.3661087', '23.7744732', 'f645a8cb39d5fb59', '2019-10-13 15:51:46'),
(1235, 1, '90.3661087', '23.7744732', 'f645a8cb39d5fb59', '2019-10-13 15:52:46'),
(1236, 1, '90.3661087', '23.7744732', 'f645a8cb39d5fb59', '2019-10-13 15:53:46'),
(1237, 1, '90.3661087', '23.7744732', 'f645a8cb39d5fb59', '2019-10-13 15:54:46'),
(1238, 1, '90.3661301', '23.7743752', 'f645a8cb39d5fb59', '2019-10-13 15:55:46'),
(1239, 1, '90.3661301', '23.7743752', 'f645a8cb39d5fb59', '2019-10-13 15:56:54'),
(1240, 1, '90.3661301', '23.7743752', 'f645a8cb39d5fb59', '2019-10-13 15:57:46'),
(1241, 1, '90.3661301', '23.7743752', 'f645a8cb39d5fb59', '2019-10-13 15:58:46'),
(1242, 1, '90.3661301', '23.7743752', 'f645a8cb39d5fb59', '2019-10-13 15:59:46'),
(1243, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 16:00:46'),
(1244, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 16:01:46'),
(1245, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 16:02:46'),
(1246, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 16:03:46'),
(1247, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 16:04:46'),
(1248, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 16:05:46'),
(1249, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 16:06:46'),
(1250, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 16:07:46'),
(1251, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 16:08:46'),
(1252, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 16:09:46'),
(1253, 1, '90.3661371', '23.7742978', 'f645a8cb39d5fb59', '2019-10-13 16:10:46'),
(1254, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 16:11:46'),
(1255, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-13 16:12:46'),
(1256, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 16:13:46'),
(1257, 1, '90.3660484', '23.7745249', 'f645a8cb39d5fb59', '2019-10-13 16:14:46'),
(1258, 1, '90.3662555', '23.7744286', 'f645a8cb39d5fb59', '2019-10-13 16:15:46'),
(1259, 1, '90.3662144', '23.7741511', 'f645a8cb39d5fb59', '2019-10-13 16:17:26'),
(1260, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 16:22:26'),
(1261, 1, '90.3662047', '23.7741973', 'f645a8cb39d5fb59', '2019-10-13 16:27:25'),
(1262, 1, '90.3662127', '23.7741584', 'f645a8cb39d5fb59', '2019-10-13 16:32:26'),
(1263, 1, '90.3661557', '23.7743041', 'f645a8cb39d5fb59', '2019-10-13 16:37:26'),
(1264, 1, '90.3661066', '23.7744765', 'f645a8cb39d5fb59', '2019-10-13 16:42:24'),
(1265, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 17:02:24'),
(1266, 1, '90.3661032', '23.7742891', 'f645a8cb39d5fb59', '2019-10-13 17:17:35'),
(1267, 1, '90.3661367', '23.7743048', 'f645a8cb39d5fb59', '2019-10-13 17:32:39'),
(1268, 1, '90.3661329', '23.7746286', 'f645a8cb39d5fb59', '2019-10-17 14:33:40'),
(1269, 1, '90.3665839', '23.7748518', 'f645a8cb39d5fb59', '2019-10-17 14:34:17'),
(1270, 1, '90.3664044', '23.7751232', 'f645a8cb39d5fb59', '2019-10-17 14:34:52'),
(1271, 1, '90.3662985', '23.7744776', 'f645a8cb39d5fb59', '2019-10-17 14:35:58'),
(1272, 1, '90.3664588', '23.7742795', 'f645a8cb39d5fb59', '2019-10-17 14:39:52'),
(1273, 1, '90.3669199', '23.7749702', 'f645a8cb39d5fb59', '2019-10-17 14:44:52'),
(1274, 1, '90.367375', '23.7750669', 'f645a8cb39d5fb59', '2019-10-17 14:49:52');
INSERT INTO `usr_location` (`id`, `usr_id`, `loc_long`, `loc_lati`, `loc_imei`, `loc_date_time`) VALUES
(1275, 1, '90.3667669', '23.7745697', 'f645a8cb39d5fb59', '2019-10-17 14:59:52'),
(1276, 1, '90.366048', '23.7746629', 'f645a8cb39d5fb59', '2019-10-17 15:40:38'),
(1277, 1, '90.365882', '23.7750487', 'f645a8cb39d5fb59', '2019-10-17 15:55:44'),
(1278, 1, '90.3660628', '23.7746859', 'f645a8cb39d5fb59', '2019-10-17 15:59:52'),
(1279, 1, '90.3660277', '23.7747814', 'f645a8cb39d5fb59', '2019-10-17 16:04:53'),
(1280, 1, '90.366047', '23.7747167', 'f645a8cb39d5fb59', '2019-10-17 16:09:53'),
(1281, 1, '90.3660273', '23.7746674', 'f645a8cb39d5fb59', '2019-10-17 16:14:53'),
(1282, 1, '90.3660942', '23.7748367', 'f645a8cb39d5fb59', '2019-10-17 16:19:52'),
(1283, 1, '90.366048', '23.7746629', 'f645a8cb39d5fb59', '2019-10-17 16:25:42'),
(1284, 1, '90.3660273', '23.7746674', 'f645a8cb39d5fb59', '2019-10-17 16:25:57'),
(1285, 1, '90.3660273', '23.7746674', 'f645a8cb39d5fb59', '2019-10-17 16:26:04'),
(1286, 1, '90.3660679', '23.7752713', 'f645a8cb39d5fb59', '2019-10-17 16:29:52'),
(1287, 1, '90.3660205', '23.7746779', 'f645a8cb39d5fb59', '2019-10-17 16:34:52'),
(1288, 1, '90.3659275', '23.7750828', 'f645a8cb39d5fb59', '2019-10-17 16:39:52'),
(1289, 1, '90.3659726', '23.7748761', 'f645a8cb39d5fb59', '2019-10-17 16:44:52'),
(1290, 1, '90.3660277', '23.7747814', 'f645a8cb39d5fb59', '2019-10-17 16:49:52'),
(1291, 1, '90.3660343', '23.7746623', 'f645a8cb39d5fb59', '2019-10-17 17:00:27'),
(1292, 1, '90.3660343', '23.7746623', 'f645a8cb39d5fb59', '2019-10-17 17:10:37'),
(1293, 1, '90.3660874', '23.7749294', 'f645a8cb39d5fb59', '2019-10-17 17:21:39'),
(1294, 1, '90.3660426', '23.7746311', 'f645a8cb39d5fb59', '2019-10-17 17:30:27'),
(1295, 1, '90.3660173', '23.7746524', 'f645a8cb39d5fb59', '2019-10-17 17:44:52'),
(1296, 1, '90.3895253', '23.824469', 'f645a8cb39d5fb59', '2019-10-17 21:04:45'),
(1297, 1, '90.3894658', '23.8229797', 'f645a8cb39d5fb59', '2019-10-17 21:04:49'),
(1298, 1, '90.3894658', '23.8229797', 'f645a8cb39d5fb59', '2019-10-17 21:04:51'),
(1299, 1, '90.3852147', '23.7864288', 'f645a8cb39d5fb59', '2019-10-17 21:29:52'),
(1300, 1, '90.3852147', '23.7864288', 'f645a8cb39d5fb59', '2019-10-17 21:45:27'),
(1301, 1, '90.3852147', '23.7864288', 'f645a8cb39d5fb59', '2019-10-17 22:25:31'),
(1302, 1, '90.3894772', '23.8246223', 'f645a8cb39d5fb59', '2019-10-17 22:29:51'),
(1303, 1, '90.3652573', '23.774805', 'f645a8cb39d5fb59', '2019-10-29 17:03:03'),
(1304, 1, '90.3660575', '23.7751097', 'f645a8cb39d5fb59', '2019-10-29 17:03:59'),
(1305, 1, '90.3660063', '23.7751162', 'f645a8cb39d5fb59', '2019-10-29 17:04:59'),
(1306, 1, '90.3660576', '23.7751098', 'f645a8cb39d5fb59', '2019-10-29 17:05:59'),
(1307, 1, '90.365986', '23.7752967', 'f645a8cb39d5fb59', '2019-10-29 17:06:44'),
(1308, 1, '90.3660582', '23.7751132', 'f645a8cb39d5fb59', '2019-10-29 17:08:21'),
(1309, 1, '90.366127', '23.774376', '1abcc3fda2040a1e', '2019-10-29 17:22:54'),
(1310, 1, '90.3659751', '23.7745693', '1abcc3fda2040a1e', '2019-10-29 17:23:05'),
(1311, 1, '90.3661208', '23.7742679', '1abcc3fda2040a1e', '2019-10-29 17:24:02'),
(1312, 1, '90.3659542', '23.7745981', '1abcc3fda2040a1e', '2019-10-29 17:25:12'),
(1313, 1, '90.3660465', '23.7745075', '1abcc3fda2040a1e', '2019-10-29 17:25:14'),
(1314, 1, '90.3660465', '23.7745075', '1abcc3fda2040a1e', '2019-10-29 17:25:19'),
(1315, 1, '90.3660603', '23.7744323', '1abcc3fda2040a1e', '2019-10-29 17:25:44'),
(1316, 1, '90.366036', '23.7743919', '1abcc3fda2040a1e', '2019-10-29 17:26:05'),
(1317, 1, '90.3659958', '23.774485', '1abcc3fda2040a1e', '2019-10-29 17:26:46'),
(1318, 1, '90.366228', '23.7742317', '1abcc3fda2040a1e', '2019-10-29 17:28:08'),
(1319, 1, '90.3662032', '23.7742592', '1abcc3fda2040a1e', '2019-10-29 17:28:54'),
(1320, 1, '90.3658897', '23.7746654', '1abcc3fda2040a1e', '2019-10-29 17:29:46'),
(1321, 1, '90.3658897', '23.7746654', '1abcc3fda2040a1e', '2019-10-29 17:30:48'),
(1322, 1, '90.3658897', '23.7746654', '1abcc3fda2040a1e', '2019-10-29 17:31:49'),
(1323, 1, '90.3662196', '23.7742417', '1abcc3fda2040a1e', '2019-10-29 17:33:13'),
(1324, 1, '90.3660835', '23.7742224', '1abcc3fda2040a1e', '2019-10-29 17:33:46'),
(1325, 1, '90.3662218', '23.7742152', '1abcc3fda2040a1e', '2019-10-29 17:34:50'),
(1326, 1, '90.3658897', '23.7746654', '1abcc3fda2040a1e', '2019-10-29 17:35:53'),
(1327, 1, '90.3658897', '23.7746654', '1abcc3fda2040a1e', '2019-10-29 17:36:53'),
(1328, 1, '90.3658897', '23.7746654', '1abcc3fda2040a1e', '2019-10-29 17:37:55'),
(1329, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 11:48:49'),
(1330, 1, '90.3660763', '23.7749321', 'f645a8cb39d5fb59', '2019-11-05 11:49:08'),
(1331, 1, '90.3660763', '23.7749321', 'f645a8cb39d5fb59', '2019-11-05 11:49:09'),
(1332, 1, '90.3661676', '23.7747612', 'f645a8cb39d5fb59', '2019-11-05 11:50:02'),
(1333, 1, '90.3661611', '23.7747486', 'f645a8cb39d5fb59', '2019-11-05 11:50:49'),
(1334, 1, '90.3661611', '23.7747486', 'f645a8cb39d5fb59', '2019-11-05 11:52:02'),
(1335, 1, '90.3661611', '23.7747486', 'f645a8cb39d5fb59', '2019-11-05 11:52:49'),
(1336, 1, '90.3661611', '23.7747486', 'f645a8cb39d5fb59', '2019-11-05 11:54:02'),
(1337, 1, '90.3661611', '23.7747486', 'f645a8cb39d5fb59', '2019-11-05 11:55:31'),
(1338, 1, '90.3659398', '23.7750045', 'f645a8cb39d5fb59', '2019-11-05 11:56:08'),
(1339, 1, '90.3659398', '23.7750045', 'f645a8cb39d5fb59', '2019-11-05 11:56:49'),
(1340, 1, '90.3659398', '23.7750045', 'f645a8cb39d5fb59', '2019-11-05 11:58:02'),
(1341, 1, '90.3659398', '23.7750045', 'f645a8cb39d5fb59', '2019-11-05 11:59:02'),
(1342, 1, '90.3659398', '23.7750045', 'f645a8cb39d5fb59', '2019-11-05 12:00:02'),
(1343, 1, '90.3660599', '23.7749183', 'f645a8cb39d5fb59', '2019-11-05 12:01:02'),
(1344, 1, '90.3660599', '23.7749183', 'f645a8cb39d5fb59', '2019-11-05 12:02:02'),
(1345, 1, '90.3660599', '23.7749183', 'f645a8cb39d5fb59', '2019-11-05 12:03:32'),
(1346, 1, '90.3660599', '23.7749183', 'f645a8cb39d5fb59', '2019-11-05 12:04:02'),
(1347, 1, '90.3660599', '23.7749183', 'f645a8cb39d5fb59', '2019-11-05 12:05:02'),
(1348, 1, '90.3660686', '23.7746572', 'f645a8cb39d5fb59', '2019-11-05 12:06:32'),
(1349, 1, '90.3660686', '23.7746572', 'f645a8cb39d5fb59', '2019-11-05 12:07:02'),
(1350, 1, '90.3660686', '23.7746572', 'f645a8cb39d5fb59', '2019-11-05 12:08:02'),
(1351, 1, '90.3660686', '23.7746572', 'f645a8cb39d5fb59', '2019-11-05 12:09:02'),
(1352, 1, '90.3660686', '23.7746572', 'f645a8cb39d5fb59', '2019-11-05 12:10:02'),
(1353, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 12:11:02'),
(1354, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 12:12:02'),
(1355, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 12:13:02'),
(1356, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 12:14:23'),
(1357, 1, '90.3660763', '23.7749321', 'f645a8cb39d5fb59', '2019-11-05 12:15:02'),
(1358, 1, '90.3660763', '23.7749321', 'f645a8cb39d5fb59', '2019-11-05 12:16:02'),
(1359, 1, '90.3660763', '23.7749321', 'f645a8cb39d5fb59', '2019-11-05 12:17:02'),
(1360, 1, '90.3660763', '23.7749321', 'f645a8cb39d5fb59', '2019-11-05 12:18:02'),
(1361, 1, '90.3660763', '23.7749321', 'f645a8cb39d5fb59', '2019-11-05 12:19:02'),
(1362, 1, '90.3660763', '23.7749321', 'f645a8cb39d5fb59', '2019-11-05 12:20:02'),
(1363, 1, '90.3660763', '23.7749321', 'f645a8cb39d5fb59', '2019-11-05 12:21:02'),
(1364, 1, '90.3660763', '23.7749321', 'f645a8cb39d5fb59', '2019-11-05 12:22:08'),
(1365, 1, '90.3660763', '23.7749321', 'f645a8cb39d5fb59', '2019-11-05 12:23:02'),
(1366, 1, '90.3660763', '23.7749321', 'f645a8cb39d5fb59', '2019-11-05 12:24:02'),
(1367, 1, '90.3661985', '23.7747009', 'f645a8cb39d5fb59', '2019-11-05 12:25:32'),
(1368, 1, '90.3661985', '23.7747009', 'f645a8cb39d5fb59', '2019-11-05 12:26:02'),
(1369, 1, '90.3661985', '23.7747009', 'f645a8cb39d5fb59', '2019-11-05 12:27:02'),
(1370, 1, '90.3661985', '23.7747009', 'f645a8cb39d5fb59', '2019-11-05 12:28:02'),
(1371, 1, '90.3661985', '23.7747009', 'f645a8cb39d5fb59', '2019-11-05 12:29:02'),
(1372, 1, '90.3661116', '23.7749684', 'f645a8cb39d5fb59', '2019-11-05 12:30:02'),
(1373, 1, '90.3661116', '23.7749684', 'f645a8cb39d5fb59', '2019-11-05 12:31:02'),
(1374, 1, '90.3661116', '23.7749684', 'f645a8cb39d5fb59', '2019-11-05 12:32:02'),
(1375, 1, '90.3661116', '23.7749684', 'f645a8cb39d5fb59', '2019-11-05 12:33:02'),
(1376, 1, '90.3661116', '23.7749684', 'f645a8cb39d5fb59', '2019-11-05 12:34:02'),
(1377, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 12:35:02'),
(1378, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 12:36:02'),
(1379, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 12:37:02'),
(1380, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 12:38:02'),
(1381, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 12:39:02'),
(1382, 1, '90.3660343', '23.7747697', 'f645a8cb39d5fb59', '2019-11-05 12:40:32'),
(1383, 1, '90.3660343', '23.7747697', 'f645a8cb39d5fb59', '2019-11-05 12:41:02'),
(1384, 1, '90.3660343', '23.7747697', 'f645a8cb39d5fb59', '2019-11-05 12:42:02'),
(1385, 1, '90.3660343', '23.7747697', 'f645a8cb39d5fb59', '2019-11-05 12:43:02'),
(1386, 1, '90.3660343', '23.7747697', 'f645a8cb39d5fb59', '2019-11-05 12:44:02'),
(1387, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 12:45:02'),
(1388, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 12:46:02'),
(1389, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 12:47:02'),
(1390, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 12:48:02'),
(1391, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 12:49:02'),
(1392, 1, '90.3660763', '23.7749321', 'f645a8cb39d5fb59', '2019-11-05 12:50:02'),
(1393, 1, '90.3660763', '23.7749321', 'f645a8cb39d5fb59', '2019-11-05 12:51:02'),
(1394, 1, '90.3660763', '23.7749321', 'f645a8cb39d5fb59', '2019-11-05 12:52:03'),
(1395, 1, '90.3660976', '23.7744072', '1abcc3fda2040a1e', '2019-11-05 12:52:27'),
(1396, 1, '90.3660763', '23.7749321', 'f645a8cb39d5fb59', '2019-11-05 12:53:02'),
(1397, 1, '90.3660469', '23.7745349', '1abcc3fda2040a1e', '2019-11-05 12:53:24'),
(1398, 1, '90.3660763', '23.7749321', 'f645a8cb39d5fb59', '2019-11-05 12:54:02'),
(1399, 1, '90.3661268', '23.7743896', '1abcc3fda2040a1e', '2019-11-05 12:54:29'),
(1400, 1, '90.3660749', '23.7744141', '1abcc3fda2040a1e', '2019-11-05 12:54:36'),
(1401, 1, '90.3660749', '23.7744141', '1abcc3fda2040a1e', '2019-11-05 12:54:49'),
(1402, 1, '90.3660989', '23.7746092', 'f645a8cb39d5fb59', '2019-11-05 12:55:32'),
(1403, 1, '90.3660039', '23.7745378', '1abcc3fda2040a1e', '2019-11-05 12:55:48'),
(1404, 1, '90.3660989', '23.7746092', 'f645a8cb39d5fb59', '2019-11-05 12:56:02'),
(1405, 1, '90.3659736', '23.774619', '1abcc3fda2040a1e', '2019-11-05 12:56:40'),
(1406, 1, '90.3660989', '23.7746092', 'f645a8cb39d5fb59', '2019-11-05 12:56:50'),
(1407, 1, '90.3659306', '23.7746553', '1abcc3fda2040a1e', '2019-11-05 12:57:38'),
(1408, 1, '90.3660989', '23.7746092', 'f645a8cb39d5fb59', '2019-11-05 12:58:02'),
(1409, 1, '90.3659601', '23.7746028', '1abcc3fda2040a1e', '2019-11-05 12:58:40'),
(1410, 1, '90.3660989', '23.7746092', 'f645a8cb39d5fb59', '2019-11-05 12:59:02'),
(1411, 1, '90.3659407', '23.7746442', '1abcc3fda2040a1e', '2019-11-05 12:59:40'),
(1412, 1, '90.3660686', '23.7746572', 'f645a8cb39d5fb59', '2019-11-05 13:00:02'),
(1413, 1, '90.3659713', '23.7746208', '1abcc3fda2040a1e', '2019-11-05 13:00:40'),
(1414, 1, '90.3660686', '23.7746572', 'f645a8cb39d5fb59', '2019-11-05 13:01:02'),
(1415, 1, '90.366005', '23.7745139', '1abcc3fda2040a1e', '2019-11-05 13:01:41'),
(1416, 1, '90.3660686', '23.7746572', 'f645a8cb39d5fb59', '2019-11-05 13:02:02'),
(1417, 1, '90.3659818', '23.7745645', '1abcc3fda2040a1e', '2019-11-05 13:02:42'),
(1418, 1, '90.3660686', '23.7746572', 'f645a8cb39d5fb59', '2019-11-05 13:03:02'),
(1419, 1, '90.3660006', '23.7745292', '1abcc3fda2040a1e', '2019-11-05 13:03:41'),
(1420, 1, '90.3660686', '23.7746572', 'f645a8cb39d5fb59', '2019-11-05 13:04:02'),
(1421, 1, '90.3659313', '23.7746539', '1abcc3fda2040a1e', '2019-11-05 13:04:48'),
(1422, 1, '90.3660763', '23.7749321', 'f645a8cb39d5fb59', '2019-11-05 13:05:02'),
(1423, 1, '90.3659742', '23.7746155', '1abcc3fda2040a1e', '2019-11-05 13:05:51'),
(1424, 1, '90.3660763', '23.7749321', 'f645a8cb39d5fb59', '2019-11-05 13:06:02'),
(1425, 1, '90.3659471', '23.7746342', '1abcc3fda2040a1e', '2019-11-05 13:06:53'),
(1426, 1, '90.3660763', '23.7749321', 'f645a8cb39d5fb59', '2019-11-05 13:07:02'),
(1427, 1, '90.3660237', '23.7745338', '1abcc3fda2040a1e', '2019-11-05 13:07:55'),
(1428, 1, '90.3660763', '23.7749321', 'f645a8cb39d5fb59', '2019-11-05 13:08:02'),
(1429, 1, '90.365935', '23.7746509', '1abcc3fda2040a1e', '2019-11-05 13:08:56'),
(1430, 1, '90.3660763', '23.7749321', 'f645a8cb39d5fb59', '2019-11-05 13:09:02'),
(1431, 1, '90.3660911', '23.774363', '1abcc3fda2040a1e', '2019-11-05 13:09:40'),
(1432, 1, '90.3661657', '23.7746371', 'f645a8cb39d5fb59', '2019-11-05 13:10:02'),
(1433, 1, '90.3661657', '23.7746371', 'f645a8cb39d5fb59', '2019-11-05 13:11:02'),
(1434, 1, '90.365943', '23.7746448', '1abcc3fda2040a1e', '2019-11-05 13:11:06'),
(1435, 1, '90.3660212', '23.7745338', '1abcc3fda2040a1e', '2019-11-05 13:11:48'),
(1436, 1, '90.3661657', '23.7746371', 'f645a8cb39d5fb59', '2019-11-05 13:12:03'),
(1437, 1, '90.3659658', '23.7746025', '1abcc3fda2040a1e', '2019-11-05 13:12:46'),
(1438, 1, '90.3661657', '23.7746371', 'f645a8cb39d5fb59', '2019-11-05 13:13:02'),
(1439, 1, '90.3660137', '23.7745354', '1abcc3fda2040a1e', '2019-11-05 13:13:47'),
(1440, 1, '90.3661657', '23.7746371', 'f645a8cb39d5fb59', '2019-11-05 13:14:02'),
(1441, 1, '90.366001', '23.7745209', '1abcc3fda2040a1e', '2019-11-05 13:14:53'),
(1442, 1, '90.3660201', '23.7747739', 'f645a8cb39d5fb59', '2019-11-05 13:15:02'),
(1443, 1, '90.3659714', '23.7745822', '1abcc3fda2040a1e', '2019-11-05 13:15:50'),
(1444, 1, '90.3660201', '23.7747739', 'f645a8cb39d5fb59', '2019-11-05 13:16:02'),
(1445, 1, '90.3661178', '23.7743984', '1abcc3fda2040a1e', '2019-11-05 13:16:54'),
(1446, 1, '90.3660201', '23.7747739', 'f645a8cb39d5fb59', '2019-11-05 13:17:02'),
(1447, 1, '90.3659943', '23.7743982', '1abcc3fda2040a1e', '2019-11-05 13:17:47'),
(1448, 1, '90.3660201', '23.7747739', 'f645a8cb39d5fb59', '2019-11-05 13:18:02'),
(1449, 1, '90.3660201', '23.7747739', 'f645a8cb39d5fb59', '2019-11-05 13:19:02'),
(1450, 1, '90.3661821', '23.7742723', '1abcc3fda2040a1e', '2019-11-05 13:19:19'),
(1451, 1, '90.3660122', '23.7743342', '1abcc3fda2040a1e', '2019-11-05 13:19:40'),
(1452, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 13:20:02'),
(1453, 1, '90.3661007', '23.7744156', '1abcc3fda2040a1e', '2019-11-05 13:20:45'),
(1454, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 13:20:59'),
(1455, 1, '90.3661049', '23.7743975', '1abcc3fda2040a1e', '2019-11-05 13:21:43'),
(1456, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 13:22:02'),
(1457, 1, '90.3661763', '23.7742595', '1abcc3fda2040a1e', '2019-11-05 13:22:45'),
(1458, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 13:23:02'),
(1459, 1, '90.3661241', '23.7743773', '1abcc3fda2040a1e', '2019-11-05 13:24:00'),
(1460, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 13:24:02'),
(1461, 1, '90.3660368', '23.7745068', '1abcc3fda2040a1e', '2019-11-05 13:24:41'),
(1462, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 13:25:32'),
(1463, 1, '90.3659233', '23.7746422', '1abcc3fda2040a1e', '2019-11-05 13:25:40'),
(1464, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 13:26:02'),
(1465, 1, '90.3661588', '23.7743603', '1abcc3fda2040a1e', '2019-11-05 13:26:41'),
(1466, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 13:27:11'),
(1467, 1, '90.3660252', '23.7744138', '1abcc3fda2040a1e', '2019-11-05 13:27:45'),
(1468, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 13:28:11'),
(1469, 1, '90.3659376', '23.7746188', '1abcc3fda2040a1e', '2019-11-05 13:28:50'),
(1470, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 13:29:13'),
(1471, 1, '90.3660857', '23.7744143', '1abcc3fda2040a1e', '2019-11-05 13:29:50'),
(1472, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 13:30:02'),
(1473, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 13:31:02'),
(1474, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 13:32:02'),
(1475, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 13:33:02'),
(1476, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 13:34:02'),
(1477, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 13:35:03'),
(1478, 1, '90.3659631', '23.7747762', 'f645a8cb39d5fb59', '2019-11-05 13:36:02'),
(1479, 1, '90.3659631', '23.7747762', 'f645a8cb39d5fb59', '2019-11-05 13:37:02'),
(1480, 1, '90.3659631', '23.7747762', 'f645a8cb39d5fb59', '2019-11-05 13:38:02'),
(1481, 1, '90.3659631', '23.7747762', 'f645a8cb39d5fb59', '2019-11-05 13:39:02'),
(1482, 1, '90.3659631', '23.7747762', 'f645a8cb39d5fb59', '2019-11-05 13:40:02'),
(1483, 1, '90.3659631', '23.7747762', 'f645a8cb39d5fb59', '2019-11-05 13:41:02'),
(1484, 1, '90.3659631', '23.7747762', 'f645a8cb39d5fb59', '2019-11-05 13:42:02'),
(1485, 1, '90.3659631', '23.7747762', 'f645a8cb39d5fb59', '2019-11-05 13:43:02'),
(1486, 1, '90.3659631', '23.7747762', 'f645a8cb39d5fb59', '2019-11-05 13:44:02'),
(1487, 1, '90.3659631', '23.7747762', 'f645a8cb39d5fb59', '2019-11-05 13:45:03'),
(1488, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 13:46:02'),
(1489, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 13:47:02'),
(1490, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 13:48:02'),
(1491, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 13:49:02'),
(1492, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 13:50:02'),
(1493, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 13:51:02'),
(1494, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 13:52:02'),
(1495, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 13:53:02'),
(1496, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 13:54:02'),
(1497, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 13:55:32'),
(1498, 1, '90.3660452', '23.7748253', 'f645a8cb39d5fb59', '2019-11-05 13:56:02'),
(1499, 1, '90.3660452', '23.7748253', 'f645a8cb39d5fb59', '2019-11-05 13:57:02'),
(1500, 1, '90.3660452', '23.7748253', 'f645a8cb39d5fb59', '2019-11-05 13:58:02'),
(1501, 1, '90.3660452', '23.7748253', 'f645a8cb39d5fb59', '2019-11-05 13:59:02'),
(1502, 1, '90.3660452', '23.7748253', 'f645a8cb39d5fb59', '2019-11-05 14:00:02'),
(1503, 1, '90.3660452', '23.7748253', 'f645a8cb39d5fb59', '2019-11-05 14:01:02'),
(1504, 1, '90.3660452', '23.7748253', 'f645a8cb39d5fb59', '2019-11-05 14:02:02'),
(1505, 1, '90.3660452', '23.7748253', 'f645a8cb39d5fb59', '2019-11-05 14:03:02'),
(1506, 1, '90.3660452', '23.7748253', 'f645a8cb39d5fb59', '2019-11-05 14:04:02'),
(1507, 1, '90.3660452', '23.7748253', 'f645a8cb39d5fb59', '2019-11-05 14:05:02'),
(1508, 1, '90.3660452', '23.7748253', 'f645a8cb39d5fb59', '2019-11-05 14:06:02'),
(1509, 1, '90.3660933', '23.7748533', 'f645a8cb39d5fb59', '2019-11-05 14:07:02'),
(1510, 1, '90.3660933', '23.7748533', 'f645a8cb39d5fb59', '2019-11-05 14:08:02'),
(1511, 1, '90.3660933', '23.7748533', 'f645a8cb39d5fb59', '2019-11-05 14:09:02'),
(1512, 1, '90.3660933', '23.7748533', 'f645a8cb39d5fb59', '2019-11-05 14:10:02'),
(1513, 1, '90.3660933', '23.7748533', 'f645a8cb39d5fb59', '2019-11-05 14:11:02'),
(1514, 1, '90.3660933', '23.7748533', 'f645a8cb39d5fb59', '2019-11-05 14:12:02'),
(1515, 1, '90.3660933', '23.7748533', 'f645a8cb39d5fb59', '2019-11-05 14:12:49'),
(1516, 1, '90.3660933', '23.7748533', 'f645a8cb39d5fb59', '2019-11-05 14:14:02'),
(1517, 1, '90.3660933', '23.7748533', 'f645a8cb39d5fb59', '2019-11-05 14:15:02'),
(1518, 1, '90.3660933', '23.7748533', 'f645a8cb39d5fb59', '2019-11-05 14:16:02'),
(1519, 1, '90.3660876', '23.7747001', 'f645a8cb39d5fb59', '2019-11-05 14:17:32'),
(1520, 1, '90.3660876', '23.7747001', 'f645a8cb39d5fb59', '2019-11-05 14:18:02'),
(1521, 1, '90.3660876', '23.7747001', 'f645a8cb39d5fb59', '2019-11-05 14:18:49'),
(1522, 1, '90.3660876', '23.7747001', 'f645a8cb39d5fb59', '2019-11-05 14:20:02'),
(1523, 1, '90.3660876', '23.7747001', 'f645a8cb39d5fb59', '2019-11-05 14:21:02'),
(1524, 1, '90.3660876', '23.7747001', 'f645a8cb39d5fb59', '2019-11-05 14:22:02'),
(1525, 1, '90.3660876', '23.7747001', 'f645a8cb39d5fb59', '2019-11-05 14:22:49'),
(1526, 1, '90.3660876', '23.7747001', 'f645a8cb39d5fb59', '2019-11-05 14:24:02'),
(1527, 1, '90.3660876', '23.7747001', 'f645a8cb39d5fb59', '2019-11-05 14:25:09'),
(1528, 1, '90.3660876', '23.7747001', 'f645a8cb39d5fb59', '2019-11-05 14:26:02'),
(1529, 1, '90.3660876', '23.7747001', 'f645a8cb39d5fb59', '2019-11-05 14:27:11'),
(1530, 1, '90.3661705', '23.7746678', 'f645a8cb39d5fb59', '2019-11-05 14:28:02'),
(1531, 1, '90.3661705', '23.7746678', 'f645a8cb39d5fb59', '2019-11-05 14:29:02'),
(1532, 1, '90.3661705', '23.7746678', 'f645a8cb39d5fb59', '2019-11-05 14:30:02'),
(1533, 1, '90.3661705', '23.7746678', 'f645a8cb39d5fb59', '2019-11-05 14:31:02'),
(1534, 1, '90.3661705', '23.7746678', 'f645a8cb39d5fb59', '2019-11-05 14:32:02'),
(1535, 1, '90.3661705', '23.7746678', 'f645a8cb39d5fb59', '2019-11-05 14:33:02'),
(1536, 1, '90.3661705', '23.7746678', 'f645a8cb39d5fb59', '2019-11-05 14:34:02'),
(1537, 1, '90.3661705', '23.7746678', 'f645a8cb39d5fb59', '2019-11-05 14:35:02'),
(1538, 1, '90.3661705', '23.7746678', 'f645a8cb39d5fb59', '2019-11-05 14:36:02'),
(1539, 1, '90.3661705', '23.7746678', 'f645a8cb39d5fb59', '2019-11-05 14:37:02'),
(1540, 1, '90.3661705', '23.7746678', 'f645a8cb39d5fb59', '2019-11-05 14:38:02'),
(1541, 1, '90.3660397', '23.7747308', 'f645a8cb39d5fb59', '2019-11-05 14:39:02'),
(1542, 1, '90.3660397', '23.7747308', 'f645a8cb39d5fb59', '2019-11-05 14:40:03'),
(1543, 1, '90.3660397', '23.7747308', 'f645a8cb39d5fb59', '2019-11-05 14:41:02'),
(1544, 1, '90.3660397', '23.7747308', 'f645a8cb39d5fb59', '2019-11-05 14:42:02'),
(1545, 1, '90.3660397', '23.7747308', 'f645a8cb39d5fb59', '2019-11-05 14:43:02'),
(1546, 1, '90.3660397', '23.7747308', 'f645a8cb39d5fb59', '2019-11-05 14:44:02'),
(1547, 1, '90.3660397', '23.7747308', 'f645a8cb39d5fb59', '2019-11-05 14:45:03'),
(1548, 1, '90.3660397', '23.7747308', 'f645a8cb39d5fb59', '2019-11-05 14:46:02'),
(1549, 1, '90.3660397', '23.7747308', 'f645a8cb39d5fb59', '2019-11-05 14:47:03'),
(1550, 1, '90.3660397', '23.7747308', 'f645a8cb39d5fb59', '2019-11-05 14:48:02'),
(1551, 1, '90.3660763', '23.7749321', 'f645a8cb39d5fb59', '2019-11-05 14:49:02'),
(1552, 1, '90.3660763', '23.7749321', 'f645a8cb39d5fb59', '2019-11-05 14:50:02'),
(1553, 1, '90.3660763', '23.7749321', 'f645a8cb39d5fb59', '2019-11-05 14:51:02'),
(1554, 1, '90.3660763', '23.7749321', 'f645a8cb39d5fb59', '2019-11-05 14:52:03'),
(1555, 1, '90.3660763', '23.7749321', 'f645a8cb39d5fb59', '2019-11-05 14:53:02'),
(1556, 1, '90.3660763', '23.7749321', 'f645a8cb39d5fb59', '2019-11-05 14:54:03'),
(1557, 1, '90.3660763', '23.7749321', 'f645a8cb39d5fb59', '2019-11-05 14:55:02'),
(1558, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 14:57:02'),
(1559, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 14:58:02'),
(1560, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 14:59:02'),
(1561, 1, '90.3660763', '23.7749321', 'f645a8cb39d5fb59', '2019-11-05 15:05:02'),
(1562, 1, '90.3660763', '23.7749321', 'f645a8cb39d5fb59', '2019-11-05 15:06:26'),
(1563, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 15:07:03'),
(1564, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 15:08:03'),
(1565, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 15:09:02'),
(1566, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 15:10:02'),
(1567, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 15:11:02'),
(1568, 1, '90.3661611', '23.7747486', 'f645a8cb39d5fb59', '2019-11-05 15:12:02'),
(1569, 1, '90.3661611', '23.7747486', 'f645a8cb39d5fb59', '2019-11-05 15:13:02'),
(1570, 1, '90.3661611', '23.7747486', 'f645a8cb39d5fb59', '2019-11-05 15:14:02'),
(1571, 1, '90.3661611', '23.7747486', 'f645a8cb39d5fb59', '2019-11-05 15:15:02'),
(1572, 1, '90.3661611', '23.7747486', 'f645a8cb39d5fb59', '2019-11-05 15:16:02'),
(1573, 1, '90.3661657', '23.7746371', 'f645a8cb39d5fb59', '2019-11-05 15:17:02'),
(1574, 1, '90.3661657', '23.7746371', 'f645a8cb39d5fb59', '2019-11-05 15:18:02'),
(1575, 1, '90.3661657', '23.7746371', 'f645a8cb39d5fb59', '2019-11-05 15:19:02'),
(1576, 1, '90.3661657', '23.7746371', 'f645a8cb39d5fb59', '2019-11-05 15:20:03'),
(1577, 1, '90.3661657', '23.7746371', 'f645a8cb39d5fb59', '2019-11-05 15:21:02'),
(1578, 1, '90.3659875', '23.7747216', 'f645a8cb39d5fb59', '2019-11-05 15:22:02'),
(1579, 1, '90.3659875', '23.7747216', 'f645a8cb39d5fb59', '2019-11-05 15:23:02'),
(1580, 1, '90.3659875', '23.7747216', 'f645a8cb39d5fb59', '2019-11-05 15:23:49'),
(1581, 1, '90.3659875', '23.7747216', 'f645a8cb39d5fb59', '2019-11-05 15:25:32'),
(1582, 1, '90.3659708', '23.7748897', 'f645a8cb39d5fb59', '2019-11-05 15:26:02'),
(1583, 1, '90.3659708', '23.7748897', 'f645a8cb39d5fb59', '2019-11-05 15:27:12'),
(1584, 1, '90.3659708', '23.7748897', 'f645a8cb39d5fb59', '2019-11-05 15:28:03'),
(1585, 1, '90.3659708', '23.7748897', 'f645a8cb39d5fb59', '2019-11-05 15:28:49'),
(1586, 1, '90.3659708', '23.7748897', 'f645a8cb39d5fb59', '2019-11-05 15:30:02'),
(1587, 1, '90.3661348', '23.7746976', 'f645a8cb39d5fb59', '2019-11-05 15:31:02');

-- --------------------------------------------------------

--
-- Table structure for table `usr_occupation`
--

CREATE TABLE `usr_occupation` (
  `occ_id` int(11) NOT NULL,
  `usr_id` int(11) NOT NULL,
  `occ_title` varchar(50) CHARACTER SET utf8 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `usr_phone`
--

CREATE TABLE `usr_phone` (
  `phn_id` int(11) NOT NULL,
  `usr_id` int(11) NOT NULL,
  `phn_business` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
  `phn_cell` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
  `phn_home` varchar(20) CHARACTER SET utf8 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `usr_phone`
--

INSERT INTO `usr_phone` (`phn_id`, `usr_id`, `phn_business`, `phn_cell`, `phn_home`) VALUES
(1, 1, '01911227945', NULL, NULL),
(2, 2, '01711842459', NULL, NULL),
(3, 3, '01922569875', NULL, NULL),
(4, 4, '01911967845', NULL, NULL),
(5, 5, '01911123456', NULL, NULL),
(6, 6, '01911986578', NULL, NULL),
(7, 7, '01911986123', NULL, NULL),
(8, 8, '01911123456', NULL, NULL),
(12, 18, '01911123456', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `vendor_profile`
--

CREATE TABLE `vendor_profile` (
  `ven_id` int(11) NOT NULL,
  `ven_name` varchar(50) NOT NULL,
  `ven_contact` varchar(30) NOT NULL,
  `ven_email` varchar(50) NOT NULL,
  `ven_company_code` varchar(50) NOT NULL,
  `ven_type` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0 = dma vendor and 1 = customer vendor',
  `ven_address` varchar(255) NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `vendor_profile`
--

INSERT INTO `vendor_profile` (`ven_id`, `ven_name`, `ven_contact`, `ven_email`, `ven_company_code`, `ven_type`, `ven_address`, `created_by`, `created_at`) VALUES
(1, 'TAFE', '86155', 'tafe@gmail.com', '001', 1, 'India', 1, '2019-07-25 09:35:39'),
(2, 'Cummins', '+86-18762343571', 'Cummins@gmail.com', '002', 1, 'Japan', 1, '2019-07-25 09:35:39');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `agent_account`
--
ALTER TABLE `agent_account`
  ADD PRIMARY KEY (`acc_id`);

--
-- Indexes for table `agent_target`
--
ALTER TABLE `agent_target`
  ADD PRIMARY KEY (`ata_id`);

--
-- Indexes for table `application`
--
ALTER TABLE `application`
  ADD PRIMARY KEY (`app_id`),
  ADD KEY `created_by` (`created_by`);

--
-- Indexes for table `assign_info`
--
ALTER TABLE `assign_info`
  ADD PRIMARY KEY (`ass_id`),
  ADD KEY `usr_id` (`usr_id`,`pro_id`,`created_by`),
  ADD KEY `pro_id` (`pro_id`);

--
-- Indexes for table `devices_gateway`
--
ALTER TABLE `devices_gateway`
  ADD PRIMARY KEY (`dev_id`),
  ADD KEY `dev_created_by` (`dev_created_by`),
  ADD KEY `dev_app_id` (`dev_app_id`),
  ADD KEY `dev_type` (`dev_type`);

--
-- Indexes for table `device_data`
--
ALTER TABLE `device_data`
  ADD PRIMARY KEY (`dvd_id`),
  ADD KEY `dev_id` (`dev_id`);

--
-- Indexes for table `dev_location`
--
ALTER TABLE `dev_location`
  ADD PRIMARY KEY (`loc_id`),
  ADD KEY `dev_id` (`dev_id`);

--
-- Indexes for table `dev_type`
--
ALTER TABLE `dev_type`
  ADD PRIMARY KEY (`dty_id`);

--
-- Indexes for table `product_model`
--
ALTER TABLE `product_model`
  ADD PRIMARY KEY (`pmo_id`),
  ADD KEY `created_by` (`created_by`);

--
-- Indexes for table `product_profile`
--
ALTER TABLE `product_profile`
  ADD PRIMARY KEY (`pro_id`),
  ADD KEY `ven_id` (`ven_id`,`created_by`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `pmo_id` (`pmo_id`),
  ADD KEY `dev_id` (`dev_id`),
  ADD KEY `type_id` (`type_id`);

--
-- Indexes for table `product_type`
--
ALTER TABLE `product_type`
  ADD PRIMARY KEY (`type_id`);

--
-- Indexes for table `servicing_schedule`
--
ALTER TABLE `servicing_schedule`
  ADD PRIMARY KEY (`ser_id`),
  ADD KEY `pro_id` (`pro_id`,`created_by`),
  ADD KEY `created_by` (`created_by`);

--
-- Indexes for table `user_log`
--
ALTER TABLE `user_log`
  ADD PRIMARY KEY (`log_id`),
  ADD KEY `usr_id` (`usr_id`);

--
-- Indexes for table `user_profile`
--
ALTER TABLE `user_profile`
  ADD PRIMARY KEY (`usr_id`),
  ADD KEY `app_id` (`app_id`);

--
-- Indexes for table `usr_address`
--
ALTER TABLE `usr_address`
  ADD PRIMARY KEY (`add_id`),
  ADD KEY `usr_id` (`usr_id`);

--
-- Indexes for table `usr_citizenship`
--
ALTER TABLE `usr_citizenship`
  ADD PRIMARY KEY (`cit_id`),
  ADD KEY `usr_id` (`usr_id`);

--
-- Indexes for table `usr_location`
--
ALTER TABLE `usr_location`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `usr_occupation`
--
ALTER TABLE `usr_occupation`
  ADD PRIMARY KEY (`occ_id`),
  ADD KEY `usr_id` (`usr_id`);

--
-- Indexes for table `usr_phone`
--
ALTER TABLE `usr_phone`
  ADD PRIMARY KEY (`phn_id`),
  ADD KEY `usr_id` (`usr_id`);

--
-- Indexes for table `vendor_profile`
--
ALTER TABLE `vendor_profile`
  ADD PRIMARY KEY (`ven_id`),
  ADD KEY `created_by` (`created_by`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `agent_account`
--
ALTER TABLE `agent_account`
  MODIFY `acc_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `agent_target`
--
ALTER TABLE `agent_target`
  MODIFY `ata_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `application`
--
ALTER TABLE `application`
  MODIFY `app_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `assign_info`
--
ALTER TABLE `assign_info`
  MODIFY `ass_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `devices_gateway`
--
ALTER TABLE `devices_gateway`
  MODIFY `dev_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `device_data`
--
ALTER TABLE `device_data`
  MODIFY `dvd_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6021;

--
-- AUTO_INCREMENT for table `dev_location`
--
ALTER TABLE `dev_location`
  MODIFY `loc_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `dev_type`
--
ALTER TABLE `dev_type`
  MODIFY `dty_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `product_model`
--
ALTER TABLE `product_model`
  MODIFY `pmo_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `product_profile`
--
ALTER TABLE `product_profile`
  MODIFY `pro_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `product_type`
--
ALTER TABLE `product_type`
  MODIFY `type_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `servicing_schedule`
--
ALTER TABLE `servicing_schedule`
  MODIFY `ser_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user_log`
--
ALTER TABLE `user_log`
  MODIFY `log_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user_profile`
--
ALTER TABLE `user_profile`
  MODIFY `usr_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `usr_address`
--
ALTER TABLE `usr_address`
  MODIFY `add_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `usr_citizenship`
--
ALTER TABLE `usr_citizenship`
  MODIFY `cit_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `usr_location`
--
ALTER TABLE `usr_location`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1588;

--
-- AUTO_INCREMENT for table `usr_occupation`
--
ALTER TABLE `usr_occupation`
  MODIFY `occ_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `usr_phone`
--
ALTER TABLE `usr_phone`
  MODIFY `phn_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `vendor_profile`
--
ALTER TABLE `vendor_profile`
  MODIFY `ven_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `assign_info`
--
ALTER TABLE `assign_info`
  ADD CONSTRAINT `assign_info_ibfk_1` FOREIGN KEY (`usr_id`) REFERENCES `user_profile` (`usr_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `assign_info_ibfk_2` FOREIGN KEY (`pro_id`) REFERENCES `product_profile` (`pro_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `devices_gateway`
--
ALTER TABLE `devices_gateway`
  ADD CONSTRAINT `devices_gateway_ibfk_1` FOREIGN KEY (`dev_created_by`) REFERENCES `user_profile` (`usr_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `devices_gateway_ibfk_2` FOREIGN KEY (`dev_app_id`) REFERENCES `user_profile` (`app_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `devices_gateway_ibfk_3` FOREIGN KEY (`dev_type`) REFERENCES `dev_type` (`dty_id`);

--
-- Constraints for table `device_data`
--
ALTER TABLE `device_data`
  ADD CONSTRAINT `device_data_ibfk_1` FOREIGN KEY (`dev_id`) REFERENCES `devices_gateway` (`dev_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `dev_location`
--
ALTER TABLE `dev_location`
  ADD CONSTRAINT `dev_location_ibfk_1` FOREIGN KEY (`dev_id`) REFERENCES `devices_gateway` (`dev_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `product_model`
--
ALTER TABLE `product_model`
  ADD CONSTRAINT `product_model_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `user_profile` (`usr_id`);

--
-- Constraints for table `product_profile`
--
ALTER TABLE `product_profile`
  ADD CONSTRAINT `product_profile_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `user_profile` (`usr_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `product_profile_ibfk_2` FOREIGN KEY (`ven_id`) REFERENCES `vendor_profile` (`ven_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `product_profile_ibfk_3` FOREIGN KEY (`pmo_id`) REFERENCES `product_model` (`pmo_id`),
  ADD CONSTRAINT `product_profile_ibfk_4` FOREIGN KEY (`dev_id`) REFERENCES `devices_gateway` (`dev_id`),
  ADD CONSTRAINT `product_profile_ibfk_5` FOREIGN KEY (`type_id`) REFERENCES `product_type` (`type_id`);

--
-- Constraints for table `servicing_schedule`
--
ALTER TABLE `servicing_schedule`
  ADD CONSTRAINT `servicing_schedule_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `user_profile` (`usr_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `servicing_schedule_ibfk_2` FOREIGN KEY (`pro_id`) REFERENCES `product_profile` (`pro_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `user_log`
--
ALTER TABLE `user_log`
  ADD CONSTRAINT `user_log_ibfk_1` FOREIGN KEY (`usr_id`) REFERENCES `user_profile` (`usr_id`);

--
-- Constraints for table `user_profile`
--
ALTER TABLE `user_profile`
  ADD CONSTRAINT `user_profile_ibfk_1` FOREIGN KEY (`app_id`) REFERENCES `application` (`app_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `usr_address`
--
ALTER TABLE `usr_address`
  ADD CONSTRAINT `usr_address_ibfk_1` FOREIGN KEY (`usr_id`) REFERENCES `user_profile` (`usr_id`);

--
-- Constraints for table `usr_citizenship`
--
ALTER TABLE `usr_citizenship`
  ADD CONSTRAINT `usr_citizenship_ibfk_1` FOREIGN KEY (`usr_id`) REFERENCES `user_profile` (`usr_id`);

--
-- Constraints for table `usr_occupation`
--
ALTER TABLE `usr_occupation`
  ADD CONSTRAINT `usr_occupation_ibfk_1` FOREIGN KEY (`usr_id`) REFERENCES `user_profile` (`usr_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `usr_phone`
--
ALTER TABLE `usr_phone`
  ADD CONSTRAINT `usr_phone_ibfk_1` FOREIGN KEY (`usr_id`) REFERENCES `user_profile` (`usr_id`);

--
-- Constraints for table `vendor_profile`
--
ALTER TABLE `vendor_profile`
  ADD CONSTRAINT `vendor_profile_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `user_profile` (`usr_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
