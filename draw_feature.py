import numpy as np
from PIL import Image, ImageDraw

# 数据
toBrainDataList = [
    1,
    [
        -0.97925669,
        -0.0226464737,
        0.201353967,
        3.12717795,
        0.190879956,
        0.230286807,
        0.954218447,
        -0.544997215,
        -0.067978844,
        0.972859263,
        -0.221187145,
        -12.4227257,
        0,
        0,
        0,
        1,
    ],
    [
        {"x": -0.278370142, "y": -1.19587886, "z": -2.89893794},
        {"x": -0.0784591734, "y": -0.583455324, "z": 2.82526064},
        {"x": -0.212015241, "y": 0.504983127, "z": -2.89935064},
        {"x": 1, "y": -1.2959584, "z": 1.23797739},
        {"x": -0.991835654, "y": -1.29371405, "z": 1.24649072},
        {"x": 0.588554144, "y": -0.912980378, "z": -1.56381893},
        {"x": -0.8598755, "y": -0.918947458, "z": -1.5490365},
        {"x": -0.00923740957, "y": 0.754633784, "z": 0.0190324504},
    ],
    {
        "0": 1,
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0,
        "5": 1,
        "6": 0,
        "7": 0,
        "8": 0,
        "9": 0,
        "10": 1,
        "11": 0,
        "12": 0,
        "13": 0,
        "14": 0,
        "15": 1,
    },
    {
        "0": 1.904197335243225,
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0,
        "5": 1.328406810760498,
        "6": 0,
        "7": 0,
        "8": 0,
        "9": 0,
        "10": -1.0000200271606445,
        "11": -1,
        "12": 0,
        "13": 0,
        "14": -0.02000020071864128,
        "15": 0,
    },
]


# 定义 NDC 到屏幕坐标的转换函数
def ndc_to_screen_coords(x_ndc, y_ndc, width, height):
    x_screen = (x_ndc + 1) * width / 2
    y_screen = (1 - y_ndc) * height / 2  # 翻转Y轴方向
    return x_screen, y_screen


# 提取数据
transform = toBrainDataList[1]
points3d = toBrainDataList[2]
viewMat = toBrainDataList[3]
projMat = toBrainDataList[4]

# 将字典中的值提取为列表
viewMat_values = [viewMat[str(i)] for i in range(16)]
projMat_values = [projMat[str(i)] for i in range(16)]

# 转换为numpy数组
transform_matrix = np.array(transform).reshape(4, 4)
view_matrix = np.array(viewMat_values).reshape(4, 4)
proj_matrix = np.array(projMat_values).reshape(4, 4)

# 转换为齐次坐标
points_homogeneous = [[point["x"], point["y"], point["z"], 1] for point in points3d]

# 打开图片
image_path = "./images/without_points.jpg"
image = Image.open(image_path).convert("RGBA")
width, height = image.size

# 计算MVP矩阵
mvp_matrix = proj_matrix @ view_matrix @ transform_matrix

# 投影到2D屏幕坐标并转换为图像坐标系
projected_points = []
for point in points_homogeneous:
    point = np.array(point)
    projected_point = mvp_matrix @ point
    projected_point = projected_point / projected_point[3]
    x_ndc, y_ndc = projected_point[0], projected_point[1]
    x_screen, y_screen = ndc_to_screen_coords(x_ndc, y_ndc, width, height)
    projected_points.append([x_screen, y_screen])

# 打印投影后的坐标
print("投影后的坐标：", projected_points)

# 计算外接矩形
projected_points = np.array(projected_points)
min_x, min_y = np.min(projected_points, axis=0)
max_x, max_y = np.max(projected_points, axis=0)

# 打印外接矩形的范围
print("外接矩形范围：", min_x, min_y, max_x, max_y)

# 裁剪外接矩形以确保在图像范围内
min_x = max(0, min_x)
min_y = max(0, min_y)
max_x = min(width, max_x)
max_y = min(height, max_y)

# 确保矩形的范围是合理的
if max_x <= min_x or max_y <= min_y:
    print("外接矩形的范围不正确，跳过绘制。")
else:
    # 创建一个透明的遮盖层
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # 绘制外接矩形并填充半透明颜色
    draw.rectangle(
        [(min_x, min_y), (max_x, max_y)],
        fill=(255, 0, 0, 128),
        outline=(255, 0, 0, 255),
    )

    # 将遮盖层与原图合并
    result_image = Image.alpha_composite(image, overlay)

    # 显示图片
    result_image.show()
