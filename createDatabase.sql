-- 创建数据库
CREATE DATABASE IF NOT EXISTS piconmap;

-- 使用指定的数据库
USE piconmap;

-- 删除表（注意：必须按照依赖关系逆序删除）
DROP TABLE IF EXISTS photos;

CREATE TABLE photos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    location POINT NOT NULL,  -- MySQL 5.7.36不支持SRID语法
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);