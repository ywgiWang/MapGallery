from flask import Flask, jsonify, render_template
import mysql.connector
from flask_bootstrap import Bootstrap
from config import DatabaseConfig  # 新增导入

app = Flask(__name__)
class Config:
    HOST = "0.0.0.0"
    PORT = 5001
    Debug = True
    
app.config.from_object(Config)
Bootstrap(app)

@app.route("/api/photos", methods=["GET"])
def get_photos():
    connection = mysql.connector.connect(
        host=DatabaseConfig.HOST, 
        database=DatabaseConfig.DATABASE, 
        user=DatabaseConfig.USER, 
        password=DatabaseConfig.PASSWORD
    )
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM photos"
    cursor.execute(query)
    photos = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(photos)


@app.route("/index", methods=["get"])
def index():
    return render_template("index.html")

@app.route("/", methods=["get"])
def base():
    return render_template("base.html")

if __name__ == "__main__":
    app.run(debug=True,port=5001)
