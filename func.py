import mysql.connector
from PIL import Image
from PIL.ExifTags import TAGS
import os, random


def get_exif_data(image_path):
    image = Image.open(image_path)
    exif_data = image._getexif()
    if exif_data is not None:
        for tag, value in exif_data.items():
            decoded_tag = TAGS.get(tag, tag)
            if decoded_tag == "GPSInfo":
                return value
    return None


def get_coordinates(exif_data):
    lat = exif_data[2]
    lon = exif_data[4]

    lat_deg = lat[0][0] / lat[0][1]
    lat_min = lat[1][0] / lat[1][1]
    lat_sec = lat[2][0] / lat[2][1]
    lat_value = lat_deg + (lat_min / 60.0) + (lat_sec / 3600.0)

    lon_deg = lon[0][0] / lon[0][1]
    lon_min = lon[1][0] / lon[1][1]
    lon_sec = lon[2][0] / lon[2][1]
    lon_value = lon_deg + (lon_min / 60.0) + (lon_sec / 3600.0)

    lat_ref = exif_data[1]
    lon_ref = exif_data[3]

    if lat_ref == "S":
        lat_value = -lat_value
    if lon_ref == "W":
        lon_value = -lon_value

    return lat_value, lon_value


"""
CREATE TABLE photos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    path VARCHAR(255) NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    taken_at DATETIME
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""


def insert_photo_to_db(path, latitude, longitude, taken_at):
    connection = mysql.connector.connect(
        host="localhost", database="piconmap", user="pic", password="onmap_&123"
    )
    cursor = connection.cursor()
    query = """
    INSERT INTO photos (path, latitude, longitude, taken_at)
    VALUES (%s, %s, %s, %s)
    """
    values = (path, latitude, longitude, taken_at)
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    # 示例使用
    folder = "static/img"
    for file in os.listdir(folder):
        insert_photo_to_db(
            os.path.join(folder, file),
            29 + random.random(),
            120 + random.random(),
            "2023-10-01 12:00:00",
        )
    # 示例使用
    # image_path = 'path/to/your/photo.jpg'
    # exif_data = get_exif_data(image_path)
    # if exif_data:
    #     coordinates = get_coordinates(exif_data)
    #     print(coordinates)
