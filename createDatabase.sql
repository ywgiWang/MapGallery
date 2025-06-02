

CREATE TABLE locations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    location POINT SRID 4326  -- 使用SRID 4326来表示WGS 84坐标系统中的地理位置
);