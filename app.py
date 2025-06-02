from flask import Flask, jsonify, render_template,request
import mysql.connector
from flask_bootstrap import Bootstrap
from config import DatabaseConfig  # 新增导入

app = Flask(__name__)
class Config:
    HOST = "0.0.0.0"
    PORT = 5000
    Debug = True
    
app.config.from_object(Config)
Bootstrap(app)

# 应用启动时初始化连接池（建议放在app初始化后）
db_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="pic_pool",
    pool_size=5,  # 根据业务需求调整连接数
    host=DatabaseConfig.HOST,
    database=DatabaseConfig.DATABASE,
    user=DatabaseConfig.USER,
    password=DatabaseConfig.PASSWORD
)

@app.route("/api/photos", methods=["GET"])
def get_photos():
    #获取xmin等参数，从前端获取
    xmin = request.args.get('xmin', type=float, )
    xmax = request.args.get('xmax', type=float,)
    ymin = request.args.get('ymin', type=float, )
    ymax = request.args.get('ymax', type=float, )
    # 从连接池获取连接（替代直接connect）
    connection = db_pool.get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM photos"
    cursor.execute(query)
    photos = cursor.fetchall()
    cursor.close()
    connection.close()  # 实际是归还连接到池，而非真正关闭
    return jsonify(photos)


@app.route("/index", methods=["get"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
