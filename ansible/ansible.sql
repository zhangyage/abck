/*
Navicat MySQL Data Transfer

Source Server         : mytest
Source Server Version : 50634
Source Host           : 47.94.188.237:3306
Source Database       : ansible

Target Server Type    : MYSQL
Target Server Version : 50634
File Encoding         : 65001

Date: 2018-01-29 16:41:46
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for auth
-- ----------------------------
DROP TABLE IF EXISTS `auth`;
CREATE TABLE `auth` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `url` (`url`),
  KEY `ix_auth_addtime` (`addtime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth
-- ----------------------------

-- ----------------------------
-- Table structure for group
-- ----------------------------
DROP TABLE IF EXISTS `group`;
CREATE TABLE `group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_name` varchar(255) DEFAULT NULL,
  `description` text,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_name` (`group_name`),
  KEY `ix_group_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of group
-- ----------------------------
INSERT INTO `group` VALUES ('1', 'yunshididai', '核心服务器组', '2017-11-08 09:50:29');
INSERT INTO `group` VALUES ('2', 'yanzhoujuejin', '核心服务器组', '2017-11-08 09:51:32');
INSERT INTO `group` VALUES ('3', 'iysdd', 'iysdd', '2017-11-16 16:41:32');

-- ----------------------------
-- Table structure for host
-- ----------------------------
DROP TABLE IF EXISTS `host`;
CREATE TABLE `host` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `alias` varchar(255) DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL,
  `ip1` varchar(100) DEFAULT NULL,
  `ip2` varchar(100) DEFAULT NULL,
  `port` smallint(6) DEFAULT NULL,
  `remote_user` varchar(255) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `alias` (`alias`),
  KEY `group_id` (`group_id`),
  KEY `ix_host_addtime` (`addtime`),
  CONSTRAINT `host_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of host
-- ----------------------------
INSERT INTO `host` VALUES ('4', 'mysql5.6', '1', '192.168.75.6', '192.168.129.6', '22', 'root', '2017-11-13 10:14:59');
INSERT INTO `host` VALUES ('7', 'rabbit', '1', '192.168.75.3', '192.168.129.3', '22', 'root', '2017-11-16 16:40:39');
INSERT INTO `host` VALUES ('8', 'opq', '2', '192.168.75.9', '192.168.129.9', '22', 'root', '2017-11-16 18:29:15');
INSERT INTO `host` VALUES ('9', 'mysql5.7', '3', '192.168.75.5', '192.168.129.5', '22', 'root', '2017-11-16 19:53:06');

-- ----------------------------
-- Table structure for jobs
-- ----------------------------
DROP TABLE IF EXISTS `jobs`;
CREATE TABLE `jobs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object` varchar(255) DEFAULT NULL,
  `started` varchar(100) DEFAULT NULL,
  `finished` varchar(100) DEFAULT NULL,
  `template_name` varchar(255) DEFAULT NULL,
  `args` varchar(255) DEFAULT NULL,
  `status` int(10) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_jobs_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of jobs
-- ----------------------------
INSERT INTO `jobs` VALUES ('44', 'mysql5.6', '2017-11-16 19:43:31.411368', '2017-11-16 19:44:01.747949', '_add_user', '(dp0\nS\'username\'\np1\nVzhangsanfeng\np2\nsS\'host\'\np3\nV192.168.75.6\np4\nsS\'password\'\np5\nV123456\np6\nsS\'user\'\np7\nVroot\np8\ns.', '3', null);
INSERT INTO `jobs` VALUES ('45', 'mysql5.6', '2017-11-16 19:56:36.229371', '2017-11-16 19:57:02.289722', '_add_user', '(dp0\nS\'username\'\np1\nVadmin\np2\nsS\'host\'\np3\nV192.168.75.6\np4\nsS\'password\'\np5\nV123456\np6\nsS\'user\'\np7\nVroot\np8\ns.', '3', null);
INSERT INTO `jobs` VALUES ('46', 'mysql5.7', '2017-11-16 19:57:37.052375', '2017-11-16 19:58:01.870441', '_add_user', '(dp0\nS\'username\'\np1\nVryry\np2\nsS\'host\'\np3\nV192.168.75.5\np4\nsS\'password\'\np5\nVgjgjgh\np6\nsS\'user\'\np7\nVroot\np8\ns.', '1', null);
INSERT INTO `jobs` VALUES ('47', 'mysql5.6', '2017-11-16 20:16:35.680281', '2017-11-16 20:16:53.572308', '_add_user', '(dp0\nS\'username\'\np1\nVadmin\np2\nsS\'host\'\np3\nV192.168.75.6\np4\nsS\'password\'\np5\nVadfsdfsfs\np6\nsS\'user\'\np7\nVroot\np8\ns.', '3', null);
INSERT INTO `jobs` VALUES ('48', 'mysql5.7', '2017-11-16 20:17:32.779826', '2017-11-16 20:17:56.592970', '_add_user', '(dp0\nS\'username\'\np1\nVadmin\np2\nsS\'host\'\np3\nV192.168.75.5\np4\nsS\'password\'\np5\nV123456\np6\nsS\'user\'\np7\nVroot\np8\ns.', '1', null);
INSERT INTO `jobs` VALUES ('49', 'mysql5.7', '2017-11-16 21:59:58.412673', '2017-11-16 22:00:54.544988', '_add_user', '(dp0\nS\'username\'\np1\nVzhangyage\np2\nsS\'host\'\np3\nV192.168.75.5\np4\nsS\'password\'\np5\nV1234566\np6\nsS\'user\'\np7\nVroot\np8\ns.', '3', null);

-- ----------------------------
-- Table structure for oplog
-- ----------------------------
DROP TABLE IF EXISTS `oplog`;
CREATE TABLE `oplog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `reason` varchar(600) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_oplog_addtime` (`addtime`),
  CONSTRAINT `oplog_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of oplog
-- ----------------------------

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `auths` varchar(600) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_role_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of role
-- ----------------------------
INSERT INTO `role` VALUES ('1', '超级管理员', '', '2017-11-07 14:36:10');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  `active` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('1', 'zhangyage', 'pbkdf2:sha256:50000$OkFURyZm$a734b722356c3521e76c48705e90f37268dee796c2801e92e659ef830b343c8d', '1', '1');

-- ----------------------------
-- Table structure for userlog
-- ----------------------------
DROP TABLE IF EXISTS `userlog`;
CREATE TABLE `userlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_userlog_addtime` (`addtime`),
  CONSTRAINT `userlog_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of userlog
-- ----------------------------
