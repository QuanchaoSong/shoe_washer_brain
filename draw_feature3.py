import cv2
import numpy as np

# 图片路径
image_path = "./images/without_points.jpg"

# 读取图片
image = cv2.imread(image_path)
if image is None:
    print("Error: Could not read image.")
    exit()

# transform 数据（示例）
transform = [
    -0.997660458,
    -0.0459239595,
    0.0506417491,
    -1.99356627,
    0.0417475961,
    0.177342117,
    0.983263373,
    0.228435054,
    -0.0541362613,
    0.983077168,
    -0.175009996,
    -9.90731335,
    0,
    0,
    0,
    1,
]

# 重新格式化 transform 为 4x4 矩阵（行主序）
transform_matrix = np.array(transform).reshape(4, 4)

# 假设我们有一个单位矩形（鞋子的初始大小为 1x1）
# 这个矩形的四个顶点在鞋子的局部坐标系中
unit_rectangle = np.array(
    [
        [-0.5, -0.5, 0, 1],  # 左下角
        [0.5, -0.5, 0, 1],  # 右下角
        [0.5, 0.5, 0, 1],  # 右上角
        [-0.5, 0.5, 0, 1],  # 左上角
    ],
    dtype=np.float64,
)

# 应用 transform 矩阵到单位矩形的顶点
transformed_points = np.dot(unit_rectangle, transform_matrix.T)

# 转换为齐次坐标（x, y, z, w）到屏幕坐标（x/w, y/w）
transformed_points[:, :2] /= transformed_points[:, 3:4]

# 提取 2D 坐标（x, y）
polygon_points = transformed_points[:, :2].astype(int)

# 创建一个 mask 层（半透明）
mask = np.zeros_like(image, dtype=np.uint8)
cv2.fillPoly(mask, [polygon_points], (0, 255, 0))  # 填充为绿色

# 将 mask 转换为半透明
alpha = 0.5  # 透明度
overlay = cv2.addWeighted(image, alpha, mask, 1 - alpha, 0)

# 绘制多边形边框
cv2.polylines(overlay, [polygon_points], isClosed=True, color=(0, 255, 0), thickness=2)

# 显示结果
cv2.imshow("Shoe Detection", overlay)
cv2.waitKey(0)
cv2.destroyAllWindows()
