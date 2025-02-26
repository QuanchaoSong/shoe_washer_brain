import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 打开图片
image_path = "./images/without_points.jpg"
image = Image.open(image_path)

# 定义变换矩阵
transform_matrix = np.array(
    [
        [-0.997660458, -0.0459239595, 0.0506417491, -1.99356627],
        [0.0417475961, 0.177342117, 0.983263373, 0.228435054],
        [-0.0541362613, 0.983077168, -0.175009996, -9.90731335],
        [0, 0, 0, 1],
    ]
)

# 定义四个角点
points = np.array([[0, 0, 0, 1], [1, 0, 0, 1], [1, 1, 0, 1], [0, 1, 0, 1]])

# 应用变换
transformed_points = np.dot(transform_matrix, points.T).T

# 提取二维坐标
transformed_points_2d = transformed_points[:, :2]

# 输出变换后的点，检查它们是否在图片的坐标范围内
print("Transformed Points 2D:", transformed_points_2d)

# 绘制图片和多边形
fig, ax = plt.subplots()
ax.imshow(image)

# 创建多边形补丁
polygon = patches.Polygon(
    transformed_points_2d, closed=True, fill=True, color="red", alpha=0.5
)
ax.add_patch(polygon)

plt.show()
