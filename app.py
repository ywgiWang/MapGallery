from flask import Flask, jsonify, render_template,request
import mysql.connector
from flask_bootstrap import Bootstrap
from config import DatabaseConfig  # 新增导入
from appfunc import cluster_points


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
    zoom = request.args.get('zoom', type=int, )
    # 从连接池获取连接（替代直接connect）
    connection = db_pool.get_connection()
    cursor = connection.cursor(dictionary=True)
    # 修改查询语句，使用ST_X和ST_Y函数提取坐标
    query = """
    SELECT 
        id, 
        name as path, 
        ST_X(location) AS lng, 
        ST_Y(location) AS lat,
        created_at
    FROM photos
    WHERE 
        ST_X(location) BETWEEN %s AND %s
        AND ST_Y(location) BETWEEN %s AND %s
    """
    # 执行查询时传入参数
    cursor.execute(query, (xmin, xmax, ymin, ymax))
    photos = cursor.fetchall()
    cursor.close()
    connection.close()  # 实际是归还连接到池，而非真正关闭
    points=[]
    for photo in photos:
        points.append((photo["lat"],photo["lng"]))
    clusters=cluster_points(points,zoom)
    print(clusters)
    return jsonify(photos)


@app.route("/index", methods=["get"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
