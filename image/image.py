import os
import cv2
import numpy as np
from logger_zk.logger_types import logger_run


class ImageMatch:
    template_path = ""  # 模板图片地址
    target_path = ""  # 目标图片地址

    def __init__(self, template_path, target_path):
        self.template_path = template_path
        self.target_path = target_path

    def match(self):
        try:
            target = cv2.imread(self.target_path)
            template = cv2.imread(self.template_path)

            # 检查图像是否读取成功
            if template is None or target is None:
                return None

            sift = cv2.SIFT_create()

            kp1, des1 = sift.detectAndCompute(template, None)
            kp2, des2 = sift.detectAndCompute(target, None)

            bf = cv2.BFMatcher()

            matches = bf.knnMatch(des1, des2, k=2)

            good = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append(m)

            if len(good) > 0:
                # 获取匹配点的坐标
                # 模板图片匹配坐标
                src_pts = np.float32([kp1[m.queryIdx].pt for m in good])

                # 目标图片匹配坐标
                dst_pts = np.float32([kp2[m.trainIdx].pt for m in good])

                # 使用均值和标准差来检测和过滤离群点
                mean = np.mean(dst_pts, axis=0)
                std_dev = np.std(dst_pts, axis=0)

                # 设置一个阈值，3倍标准差为过滤的标准
                threshold = 1
                lower_bound = mean - threshold * std_dev
                upper_bound = mean + threshold * std_dev

                # 过滤掉超出上下限的点
                filtered_pts = dst_pts[
                    np.all((dst_pts >= lower_bound) & (dst_pts <= upper_bound), axis=1)
                ]

                if filtered_pts.size == 0:
                    return None

                else:
                    # 计算匹配点的中心
                    # 模板图片中心
                    center_src = tuple(map(int, np.mean(src_pts, axis=0)))

                    # 目标图片中心
                    center_dst = tuple(map(int, np.mean(filtered_pts, axis=0)))

                    # 打印匹配点的中心
                    # 打印模板图片匹配到的中心点
                    print(f"Center of matching points in small image: {center_src}")
                    # 打印目标图片匹配到的中心点
                    print(f"Center of matching points in large image: {center_dst}")

                    # 在大图中标记匹配区域的中心点
                    img2_with_center = target.copy()
                    cv2.circle(img2_with_center, center_dst, 10, (0, 255, 0), -1)

                    # 画出匹配结果
                    img3 = cv2.drawMatches(template, kp1, img2_with_center, kp2, good, None,
                                           flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

                    # 获取当前脚本的执行目录
                    current_directory = os.getcwd()

                    # 保存图片到当前目录
                    result_path = os.path.join(current_directory, 'matched_result.png')
                    isTrue = cv2.imwrite(result_path, img3)
                    if isTrue:
                        print("匹配成功且将图片拉取到了本地")
                    print(f"Matching result saved at: {result_path}")

                    # 返回目标图片匹配到的中心点
                    return center_dst
            else:
                return None
        except FileNotFoundError as e:
            logger_run.error(f"error: {e}")
            return None


if __name__ == "__main__":
    # 示例：匹配两张图片并保存结果
    center = ImageMatch('temp.png', 'main.png').match()
    print(center)
