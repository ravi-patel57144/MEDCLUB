-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 11, 2020 at 07:10 PM
-- Server version: 10.4.14-MariaDB
-- PHP Version: 7.4.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dbsite`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `email`, `password`) VALUES
(1, 'admin1@gmail.com', 'admin123');

-- --------------------------------------------------------

--
-- Table structure for table `donate`
--

CREATE TABLE `donate` (
  `id` int(11) NOT NULL,
  `medicine_name` varchar(20) NOT NULL,
  `donater_user_id` int(11) DEFAULT NULL,
  `receiver_ngo_id` int(11) DEFAULT NULL,
  `donation_date` datetime NOT NULL,
  `quantity` int(11) NOT NULL,
  `medicine_img` varchar(20) NOT NULL,
  `accepted` tinyint(1) NOT NULL,
  `rejected` tinyint(1) NOT NULL,
  `comment` varchar(150) DEFAULT NULL,
  `rejected_by` int(10) DEFAULT NULL,
  `delivered` tinyint(1) DEFAULT 0,
  `expiry_date` varchar(50) DEFAULT NULL
) ;

--
-- Dumping data for table `donate`
--

INSERT INTO `donate` (`id`, `medicine_name`, `donater_user_id`, `receiver_ngo_id`, `donation_date`, `quantity`, `medicine_img`, `accepted`, `rejected`, `comment`, `rejected_by`, `delivered`, `expiry_date`) VALUES
(1, 'stapr', 1, 1, '2020-11-16 16:29:52', 33, 'c1ae35708590fac8.jpg', 0, 1, 'not valid medicine name', 1, 0, '1/2/2021'),
(2, 'stopache', 1, 1, '2020-11-16 18:44:08', 44, 'b61779929ba461fd.jpg', 1, 0, NULL, NULL, 0, '1/2/2021'),
(3, 'xitrol', 1, 1, '2020-11-17 06:19:47', 50, '91f8448bd9d5af92.jpg', 1, 0, NULL, NULL, 0, '1/2/2022'),
(4, 'deizwe', 1, 1, '2020-11-17 06:20:06', 40, 'f8f86ee83f1253ce.jpg', 1, 0, NULL, NULL, 0, '1/2/2023'),
(5, 'med01', 1, 1, '2020-12-05 06:49:28', 50, '8985b644023bffac.jpg', 1, 0, NULL, NULL, 0, '1/2/2021'),
(6, 'stopache', 1, 1, '2020-12-06 05:28:11', 100, 'ed5cdada19a56961.jpg', 1, 0, NULL, NULL, 0, '1/2/2025'),
(7, 'stopache', 1, 1, '2020-12-11 14:28:18', 45, 'db7e2c7f0b5f64e3.PNG', 1, 0, NULL, NULL, 0, '1/2/2024'),
(8, 'zindox', 1, 1, '2020-12-11 15:11:36', 21, '2b6a59413b905896.png', 1, 0, NULL, NULL, 0, '1/2/2021'),
(9, 'coronil', 1, 1, '2020-12-11 15:19:27', 20, '4970d3be6b79a04b.jpg', 1, 0, NULL, NULL, 0, '1/2/2021'),
(10, 'med02', 1, 1, '2020-12-11 17:05:42', 15, '952e7d544fc2eeb4.jpg', 0, 0, NULL, NULL, 0, '25/2/2022');

-- --------------------------------------------------------

--
-- Table structure for table `ngo`
--

CREATE TABLE `ngo` (
  `id` int(11) NOT NULL,
  `ngo_name` varchar(20) NOT NULL,
  `owner_name` varchar(20) NOT NULL,
  `email` varchar(80) NOT NULL,
  `mobile` varchar(10) NOT NULL,
  `address` varchar(500) NOT NULL,
  `password` varchar(100) NOT NULL,
  `upload_verified_doc` varchar(20) NOT NULL,
  `is_verified` tinyint(1) NOT NULL,
  `rejected` tinyint(1) NOT NULL DEFAULT 0,
  `blocked` tinyint(1) NOT NULL DEFAULT 0
) ;

--
-- Dumping data for table `ngo`
--

INSERT INTO `ngo` (`id`, `ngo_name`, `owner_name`, `email`, `mobile`, `address`, `password`, `upload_verified_doc`, `is_verified`, `rejected`, `blocked`) VALUES
(1, 'ngo1', 'owner1', 'ngo1@gmail.com', '7896541230', 'ujala', '$5$rounds=535000$XFmuyCPrzB7Y5FSG$sIrRg8DbiyV7G9LZfERdGKuJNZaKeq8UJvEg/.PjtA7', '9aaab3c10ce5e64e.jpg', 1, 0, 0),
(2, 'ngo2@gmail.com', 'owner2', 'ngo2@gmail.com', '9974598657', 'uajala', '$5$rounds=535000$Nq0z5IoV11.qZ/LP$rnHM2qEnRHphMbSn.xAGMAhGcCnS4P/NsYC49xXozA7', '8b331f71c54a745c.jpg', 0, 1, 1),
(3, 'ngo3', 'owner 3', 'ngo3@gmail.com', '7878786543', 'sarkhej', '$5$rounds=535000$89lTfv8o5VEciOpc$q1r4FCj5flUIz4NHodNdlR7xFgq4YzcXUH21dzl8TA.', '744fc08d942a4b55.png', 0, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `report`
--

CREATE TABLE `report` (
  `id` int(11) NOT NULL,
  `medicine_name` varchar(20) NOT NULL,
  `ngo_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `ngo_name` varchar(50) NOT NULL DEFAULT 'none'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `report`
--

INSERT INTO `report` (`id`, `medicine_name`, `ngo_id`, `quantity`, `ngo_name`) VALUES
(1, 'sotppp', 1, 25, 'ngo1'),
(2, 'deizwe', 1, 40, 'ngo1'),
(3, 'xitrol', 1, 50, 'ngo1'),
(4, 'med1', 1, 13, 'ngo1'),
(5, 'paracetamol', 1, 39, 'ngo1'),
(6, 'stopache', 1, 189, 'ngo1'),
(7, 'zinic', 1, 30, 'ngo1'),
(8, 'zindox', 1, 21, 'ngo1'),
(9, 'coronil', 1, 20, 'ngo1'),
(10, 'med01', 1, 50, 'ngo1');

-- --------------------------------------------------------

--
-- Table structure for table `request`
--

CREATE TABLE `request` (
  `id` int(11) NOT NULL,
  `medicine_name` varchar(20) NOT NULL,
  `requester_user_id` int(11) DEFAULT NULL,
  `donater_ngo_id` int(11) DEFAULT NULL,
  `request_date` datetime NOT NULL,
  `quantity` int(11) NOT NULL,
  `prescription` varchar(20) NOT NULL,
  `doctor_name` varchar(20) NOT NULL,
  `accepted` tinyint(1) NOT NULL,
  `rejected` tinyint(1) NOT NULL,
  `comment` varchar(150) DEFAULT NULL,
  `rejected_by` int(10) DEFAULT NULL,
  `delivered` tinyint(1) NOT NULL DEFAULT 0
) ;

--
-- Dumping data for table `request`
--

INSERT INTO `request` (`id`, `medicine_name`, `requester_user_id`, `donater_ngo_id`, `request_date`, `quantity`, `prescription`, `doctor_name`, `accepted`, `rejected`, `comment`, `rejected_by`, `delivered`) VALUES
(1, 'med1', 1, 1, '2020-11-15 10:19:58', 13, '649ed0ad3bbca07e.jpg', 'santosh', 1, 0, 'fgfghgjhggh', 1, 0),
(2, 'zinic', 1, 1, '2020-11-16 16:25:16', 30, '70ba322f1700d72d.jpg', 'sikwmm', 1, 0, 'pres invalid', NULL, 0),
(3, 'sotppp', 1, 1, '2020-11-16 16:26:36', 25, 'e4bff79c30156908.jpg', 'sriokl', 1, 0, NULL, NULL, 1),
(4, 'paracetamol', 1, 1, '2020-11-16 18:44:29', 39, '2f8bf9dd0065a914.jpg', 'sadrt', 1, 0, 'plz uplod valid prescription', 1, 0),
(5, 'stoper', 1, NULL, '2020-11-17 05:00:41', 25, '250268cb9fc65dd5.jpg', 'santoshii', 0, 1, 'prescription not valiad', 1, 0),
(6, 'nirta', 1, NULL, '2020-11-17 06:19:17', 15, '96afbee7f9197563.jpg', 'serif', 0, 1, 'prescription invalid', 1, 0),
(7, 'zinide', 1, NULL, '2020-12-11 16:46:21', 14, 'a6c6b13cb4dfa899.png', 'mahesh', 0, 0, NULL, NULL, 0);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `fname` varchar(20) NOT NULL,
  `lname` varchar(20) NOT NULL,
  `email` varchar(80) NOT NULL,
  `mobile` varchar(10) NOT NULL,
  `address` varchar(500) NOT NULL,
  `password` varchar(100) NOT NULL,
  `is_verified` tinyint(1) NOT NULL,
  `rejected` tinyint(1) NOT NULL DEFAULT 0,
  `blocked` tinyint(1) NOT NULL DEFAULT 0
) ;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `fname`, `lname`, `email`, `mobile`, `address`, `password`, `is_verified`, `rejected`, `blocked`) VALUES
(1, 'sandip', 'mahato', 'sandip@gmail.com', '9974599357', 'changodar', '$5$rounds=535000$fOjZC1xKZuaHJ9si$LSuplR9FU8.XmRam1N7v6b9SKVcBPfybMlpSCDSfsg7', 1, 0, 0),
(2, 'pradip', 'mahato', 'pradip@gmail.com', '9632587456', 'ujala', '$5$rounds=535000$q4JVP4C66x8Qns4t$Z6sx1UZpYFecwgLyrRN/RmyQO85KGoyyIn6S9UZitu9', 0, 1, 0),
(3, 'sudhir', 'mahato', 'sudhir@gmail.com', '9632587469', 'sarkhej', '$5$rounds=535000$NhQuHhvp4LTdqC5V$qvqeGeTU4gpveqONYKLwtRc1TBlCFsXs0TtU94ysYj2', 0, 0, 0),
(5, 'gita', 'mahato', 'gita@gmail.com', '8000220265', 'chamgodar', '$5$rounds=535000$5amrjHY/IoWCM35S$OlfxMMq3nksmt6mJTTQaPfresPx3Im1KxsIuGA7nvg5', 0, 0, 0),
(6, 'ravi', 'patel', 'ravi@gmail.com', '9601669139', 'ujala', '$5$rounds=535000$gqWbq9d6tRUzfFlp$4jkUWi1zUs.4K4anpVKApvv2ga9iAG7B8/NuA3.8GQ/', 1, 0, 1),
(7, 'user f', 'userl', 'user1@gmail.com', '9632587415', 'safgyg', '$5$rounds=535000$.hruU1.0jXxOXSYn$asIAtY9Rf1tKZLW.4nXck7x1w6m1R99YE71r40B6WaB', 0, 1, 1),
(8, 'fake fname', 'fake lname', 'fake@gmail.com', '8768769876', 'sarkhej', '$5$rounds=535000$d3YN.DqdiKircbdC$QzsRO954mJUiLbRUjmdW3cY6en1PAM/2Jm2VqGAS2wB', 1, 0, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `donate`
--
ALTER TABLE `donate`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `ngo`
--
ALTER TABLE `ngo`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ngo_name` (`ngo_name`),
  ADD UNIQUE KEY `owner_name` (`owner_name`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `mobile` (`mobile`);

--
-- Indexes for table `report`
--
ALTER TABLE `report`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `medicine_name` (`medicine_name`);

--
-- Indexes for table `request`
--
ALTER TABLE `request`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `mobile` (`mobile`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `donate`
--
ALTER TABLE `donate`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ngo`
--
ALTER TABLE `ngo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `report`
--
ALTER TABLE `report`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `request`
--
ALTER TABLE `request`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
