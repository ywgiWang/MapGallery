from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
import numpy as np
zoom_scale={
    0:591657550.49,
    1:295828775.245,
    2:147914387.6225,
    3:73957193.81125,
    4:36978596.905625,
    5:18489298.4528125,
    6:9244649.22640625,
    7:4622324.613203125,
    8:2311162.3066015625,
    9:1155581.1533007812,
    10:577790.5766503906,
    11:288895.2883251953,
    12:144447.64416259766,
    13:72223.82208129883,
    14:36111.911040649414,
    15:18055.955520324707,
    16:9027.977760162354,
    17:4513.988880081177,
    18:2256.9944400405885,
    19:1128.4972200202943,
    20:564.2486100101471,
    21:282.12430500507357,
    22:141.06215250253678
    }
def cluster_points(points,zoom):
    #根据leaflet的zoom级别，得出当前比例尺，再转换为经纬度，按10像素为一个cluster，得出eps
    scale=zoom_scale[zoom]
    #把scale单位米转为经纬度
    scale_lat=scale/111320

    # 假设points是从MySQL获取的点集，格式为[(lat1, lon1), (lat2, lon2), ...]
    X = np.array(points)

    # 应用DBSCAN算法
    # db = DBSCAN(eps=scale_lat, min_samples=2).fit_predict(points)  # 根据实际情况调整eps和min_samples参数
    y_pred = KMeans(n_clusters=3, random_state=9).fit_predict(X)
    # plt.scatter(X[:, 0], X[:, 1], c=y_pred)
    # plt.show()
    return y_pred.tolist()