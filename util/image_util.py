#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/20 14:00
# @Author : limber
# @desc :
import cv2
import numpy as np

from util.config_util import MATCH_RESULT_FOLDER, RESOURCES
from util.path_util import PathUtil


class ImageUtil:
    @staticmethod
    def match(target_path: str, template_path: str) -> tuple | None:
        try:
            target = cv2.imread(target_path)
            template = cv2.imread(template_path)

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
                    # 目标图片中心
                    center_dst = tuple(map(int, np.mean(filtered_pts, axis=0)))

                    # 需要输出匹配结果就打开下面这段代码注释
                    #####################################################
                    # # 模板图片中心
                    # center_src = tuple(map(int, np.mean(src_pts, axis=0)))
                    # # 打印匹配点的中心
                    # # 打印模板图片匹配到的中心点
                    # print(f"Center of matching points in small image: {center_src}")
                    # # 打印目标图片匹配到的中心点
                    # print(f"Center of matching points in large image: {center_dst}")
                    #
                    # # 在大图中标记匹配区域的中心点
                    # img2_with_center = target.copy()
                    # cv2.circle(img2_with_center, center_dst, 10, (0, 0, 255), -1)
                    # # 画出匹配结果
                    # img3 = cv2.drawMatches(template, kp1, img2_with_center, kp2, good, None,
                    #                        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
                    # # 保存图片
                    # root_path = PathUtil.get_root_path(__file__, 2)
                    # image_store_path = str(root_path.joinpath(MATCH_RESULT_FOLDER).joinpath('match_image_result.png'))
                    # cv2.imwrite(image_store_path, img3)
                    ######################################################
                    # 输出中心点
                    return center_dst
            else:
                return None
        except FileNotFoundError:
            return None


if __name__ == '__main__':
    root_path = PathUtil.get_root_path(__file__, 2)
    target_path = str(root_path.joinpath(RESOURCES).joinpath("test").joinpath("target.png"))
    template_path = str(root_path.joinpath(RESOURCES).joinpath("test").joinpath("template.png"))
    result = ImageUtil.match(target_path, template_path)
    print(result)
