/*
 Navicat Premium Data Transfer

 Source Server         : pro
 Source Server Type    : MySQL
 Source Server Version : 80035
 Source Host           : localhost:3306
 Source Schema         : final

 Target Server Type    : MySQL
 Target Server Version : 80035
 File Encoding         : 65001

 Date: 21/12/2023 18:03:34
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for language
-- ----------------------------
DROP TABLE IF EXISTS `language`;
CREATE TABLE `language`  (
  `language_id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `language_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`language_id`) USING HASH,
  UNIQUE INDEX `name`(`language_name` ASC) USING BTREE
) AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of language
-- ----------------------------
INSERT INTO `language` VALUES (1, 'C');
INSERT INTO `language` VALUES (2, 'C++');
INSERT INTO `language` VALUES (4, 'Java');
INSERT INTO `language` VALUES (3, 'Python');
INSERT INTO `language` VALUES (5, 'Rust');

-- ----------------------------
-- Table structure for problems
-- ----------------------------
DROP TABLE IF EXISTS `problems`;
CREATE TABLE `problems`  (
  `problem_id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `problem` blob NULL,
  PRIMARY KEY (`problem_id`) USING HASH
) AUTO_INCREMENT = 1002 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of problems
-- ----------------------------
INSERT INTO `problems` VALUES (1001, NULL);
INSERT INTO `problems` VALUES (1002, NULL);

-- ----------------------------
-- Table structure for record
-- ----------------------------
DROP TABLE IF EXISTS `record`;
CREATE TABLE `record`  (
  `submit_id` bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  `time_slot` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `problem_id` int UNSIGNED NOT NULL,
  `user_id` int UNSIGNED NOT NULL,
  `code` blob NULL,
  `language_id` int UNSIGNED NOT NULL,
  `status_id` int UNSIGNED NOT NULL DEFAULT 1,
  `code_len` int UNSIGNED NULL DEFAULT NULL,
  `time` float UNSIGNED NULL DEFAULT 0,
  PRIMARY KEY (`submit_id`) USING HASH,
  INDEX `language`(`language_id`) USING HASH,
  INDEX `status`(`status_id`) USING HASH,
  INDEX `problem`(`problem_id`) USING HASH,
  INDEX `user`(`user_id`) USING HASH,
  INDEX `time`(`time_slot` ASC) USING BTREE,
  CONSTRAINT `language` FOREIGN KEY (`language_id`) REFERENCES `language` (`language_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `problem` FOREIGN KEY (`problem_id`) REFERENCES `problems` (`problem_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `status` FOREIGN KEY (`status_id`) REFERENCES `status` (`status_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `user` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of record
-- ----------------------------

-- ----------------------------
-- Table structure for status
-- ----------------------------
DROP TABLE IF EXISTS `status`;
CREATE TABLE `status`  (
  `status_id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `status_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`status_id`) USING BTREE
) AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of status
-- ----------------------------
INSERT INTO `status` VALUES (1, 'Pending');
INSERT INTO `status` VALUES (2, 'Accepted');
INSERT INTO `status` VALUES (3, 'Wrong Answer');
INSERT INTO `status` VALUES (4, 'Time Limit Error');
INSERT INTO `status` VALUES (5, 'Memory Limit Error');
INSERT INTO `status` VALUES (6, 'Runtime Error');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `user_id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '',
  `user_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `grant` BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY (`user_id`) USING HASH,
  UNIQUE INDEX `user_code`(`user_code`) USING HASH,
  INDEX `name`(`user_name` ASC) USING BTREE
) AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'c1', 'coder_1','123456',TRUE);
INSERT INTO `user` VALUES (3, 'admin', 'admin','123456',TRUE);
INSERT INTO `user` VALUES (2, 'c2', 'coder_2','654321',FALSE);

-- ----------------------------
-- Triggers structure for table record
-- ----------------------------
DROP TRIGGER IF EXISTS `insert`;
delimiter ;;
CREATE TRIGGER `insert` BEFORE INSERT ON `record` FOR EACH ROW SET NEW.code_len=LENGTH(NEW.`code`)
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;

