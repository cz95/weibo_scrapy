/*
 Navicat Premium Data Transfer

 Source Server         : blog
 Source Server Type    : SQLite
 Source Server Version : 3012001
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3012001
 File Encoding         : 65001

 Date: 28/01/2019 14:01:37
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for sina_blog
-- ----------------------------
DROP TABLE IF EXISTS "sina_blog";
CREATE TABLE "sina_blog" (
  "user_id" integer NOT NULL,
  "user_name" text,
  "verified_type" text,
  "user_followers" TEXT,
  "time" text,
  "weibo_id" INTEGER NOT NULL ON CONFLICT REPLACE COLLATE NOCASE,
  "text" TEXT,
  "text_len" TEXT,
  "source" TEXT,
  "pic_id" INTEGER,
  "vedio_url" TEXT,
  "reposts" TEXT,
  "comments" TEXT,
  "attitudes" TEXT,
  "isLongText" TEXT,
  "is_reposts" TEXT,
  "reposts_time" text,
  "reposts_id" INTEGER,
  "reposts_text" TEXT,
  "reposts_pic_id" text,
  "reposts_user_id" integer,
  "reposts_user_name" TEXT,
  "reposts_verified_type" TEXT,
  "reposts_user_followers" TEXT,
  "search_type" TEXT,
  "search_key" TEXT,
  PRIMARY KEY ("weibo_id") ON CONFLICT REPLACE
);

-- ----------------------------
-- Indexes structure for table sina_blog
-- ----------------------------
CREATE INDEX "main"."search_ix"
ON "sina_blog" (
  "search_type" COLLATE NOCASE ASC,
  "search_key" COLLATE NOCASE ASC
);
CREATE INDEX "main"."user_id_ix"
ON "sina_blog" (
  "user_id" COLLATE NOCASE ASC
);
CREATE INDEX "main"."user_name_ix"
ON "sina_blog" (
  "user_name" COLLATE NOCASE ASC
);

PRAGMA foreign_keys = true;
