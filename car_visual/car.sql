/*
 Navicat MySQL Data Transfer

 Source Server         : ssmLearn
 Source Server Type    : MySQL
 Source Server Version : 50731
 Source Host           : localhost:3306
 Source Schema         : 2024-04-14-300

 Target Server Type    : MySQL
 Target Server Version : 50731
 File Encoding         : 65001

 Date: 27/04/2024 19:54:28
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for car
-- ----------------------------
DROP TABLE IF EXISTS `car`;
CREATE TABLE `car`  (
  `id` int(11) NOT NULL,
  `x` double NULL DEFAULT NULL,
  `y` double NULL DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of car
-- ----------------------------
INSERT INTO `car` VALUES (100, 48.6, 81.63, 'Car A');
INSERT INTO `car` VALUES (101, 68.14, 56.56, 'Car A');
INSERT INTO `car` VALUES (102, 16.59, 42.63, 'Car A');
INSERT INTO `car` VALUES (103, 82.23, 16.34, 'Car A');
INSERT INTO `car` VALUES (104, 22.94, 79.76, 'Car A');
INSERT INTO `car` VALUES (105, 77.9, 9.42, 'Car A');
INSERT INTO `car` VALUES (106, 76.77, 63.16, 'Car A');
INSERT INTO `car` VALUES (107, 69.58, 10.7, 'Car A');
INSERT INTO `car` VALUES (108, 27.09, 54.73, 'Car A');
INSERT INTO `car` VALUES (109, 93.55, 86.03, 'Car A');
INSERT INTO `car` VALUES (110, 40.91, 39.02, 'Car A');
INSERT INTO `car` VALUES (111, 92.35, 85.31, 'Car A');
INSERT INTO `car` VALUES (112, 37.55, 50.71, 'Car A');
INSERT INTO `car` VALUES (113, 7.86, 6.11, 'Car A');
INSERT INTO `car` VALUES (114, 75.49, 24.92, 'Car A');
INSERT INTO `car` VALUES (115, 36.45, 18.83, 'Car A');
INSERT INTO `car` VALUES (116, 15.44, 1.01, 'Car A');
INSERT INTO `car` VALUES (117, 67.37, 77.62, 'Car A');
INSERT INTO `car` VALUES (118, 14.17, 4.1, 'Car A');
INSERT INTO `car` VALUES (119, 33.35, 91.23, 'Car A');
INSERT INTO `car` VALUES (200, 58.38, 68.58, 'Car B');
INSERT INTO `car` VALUES (201, 12.88, 85.74, 'Car B');
INSERT INTO `car` VALUES (202, 13.09, 20.13, 'Car B');
INSERT INTO `car` VALUES (203, 9.63, 38.48, 'Car B');
INSERT INTO `car` VALUES (204, 28.17, 28.9, 'Car B');
INSERT INTO `car` VALUES (205, 2.92, 64.22, 'Car B');
INSERT INTO `car` VALUES (206, 66.64, 30.42, 'Car B');
INSERT INTO `car` VALUES (207, 69.61, 70.14, 'Car B');
INSERT INTO `car` VALUES (208, 5.71, 66.08, 'Car B');
INSERT INTO `car` VALUES (209, 77.58, 22.99, 'Car B');
INSERT INTO `car` VALUES (210, 73.49, 19.96, 'Car B');
INSERT INTO `car` VALUES (211, 5.71, 25.18, 'Car B');
INSERT INTO `car` VALUES (212, 82.36, 58.73, 'Car B');
INSERT INTO `car` VALUES (213, 30.62, 14.69, 'Car B');
INSERT INTO `car` VALUES (214, 73.15, 64.43, 'Car B');
INSERT INTO `car` VALUES (215, 19.39, 73.52, 'Car B');
INSERT INTO `car` VALUES (216, 59.73, 56.91, 'Car B');
INSERT INTO `car` VALUES (217, 45.79, 15.73, 'Car B');
INSERT INTO `car` VALUES (218, 67.79, 93.86, 'Car B');
INSERT INTO `car` VALUES (219, 94.2, 68.02, 'Car B');
INSERT INTO `car` VALUES (300, 57.3, 88.64, 'Car C');
INSERT INTO `car` VALUES (301, 93.09, 64.74, 'Car C');
INSERT INTO `car` VALUES (302, 43.49, 98.46, 'Car C');
INSERT INTO `car` VALUES (303, 59.78, 51.56, 'Car C');
INSERT INTO `car` VALUES (304, 6.71, 70.83, 'Car C');
INSERT INTO `car` VALUES (305, 56.1, 92.42, 'Car C');
INSERT INTO `car` VALUES (306, 80.77, 1.44, 'Car C');
INSERT INTO `car` VALUES (307, 31.21, 51.44, 'Car C');
INSERT INTO `car` VALUES (308, 48.01, 79.59, 'Car C');
INSERT INTO `car` VALUES (309, 11.92, 34.52, 'Car C');
INSERT INTO `car` VALUES (310, 18.77, 13.82, 'Car C');
INSERT INTO `car` VALUES (311, 78.34, 7.01, 'Car C');
INSERT INTO `car` VALUES (312, 20.84, 75.53, 'Car C');
INSERT INTO `car` VALUES (313, 61.25, 41.34, 'Car C');
INSERT INTO `car` VALUES (314, 59.89, 78.96, 'Car C');
INSERT INTO `car` VALUES (315, 10.47, 84.97, 'Car C');
INSERT INTO `car` VALUES (316, 95.12, 39.02, 'Car C');
INSERT INTO `car` VALUES (317, 11.42, 8.25, 'Car C');
INSERT INTO `car` VALUES (318, 38.12, 75.95, 'Car C');
INSERT INTO `car` VALUES (319, 43.69, 33, 'Car C');
INSERT INTO `car` VALUES (400, 42.72, 5.58, 'Car D');
INSERT INTO `car` VALUES (401, 90.23, 83.64, 'Car D');
INSERT INTO `car` VALUES (402, 67.38, 32.46, 'Car D');
INSERT INTO `car` VALUES (403, 86.14, 20.58, 'Car D');
INSERT INTO `car` VALUES (404, 14.76, 82.34, 'Car D');
INSERT INTO `car` VALUES (405, 45.31, 31.06, 'Car D');
INSERT INTO `car` VALUES (406, 70.42, 39.28, 'Car D');
INSERT INTO `car` VALUES (407, 30.13, 68.43, 'Car D');
INSERT INTO `car` VALUES (408, 40.72, 94.78, 'Car D');
INSERT INTO `car` VALUES (409, 83.6, 6.57, 'Car D');
INSERT INTO `car` VALUES (410, 54.86, 94.98, 'Car D');
INSERT INTO `car` VALUES (411, 11.65, 73.26, 'Car D');
INSERT INTO `car` VALUES (412, 4.29, 58.84, 'Car D');
INSERT INTO `car` VALUES (413, 64.39, 33.91, 'Car D');
INSERT INTO `car` VALUES (414, 81.37, 27.23, 'Car D');
INSERT INTO `car` VALUES (415, 91.77, 95.04, 'Car D');
INSERT INTO `car` VALUES (416, 44.56, 8.71, 'Car D');
INSERT INTO `car` VALUES (417, 0.08, 97.16, 'Car D');
INSERT INTO `car` VALUES (418, 89.29, 70.92, 'Car D');
INSERT INTO `car` VALUES (419, 51.63, 98.17, 'Car D');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `phone` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `password` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('123', '123');
INSERT INTO `user` VALUES ('1', '1');
INSERT INTO `user` VALUES ('1', '1');

SET FOREIGN_KEY_CHECKS = 1;
