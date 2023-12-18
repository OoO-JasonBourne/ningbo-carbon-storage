# -*- coding: utf-8 -*-
import rasterio
import numpy as np
import json

def pixelCount(file_name):
    # 读取TIFF影像
    file = './data/Imgs_carbon/' + file_name + '.tif'
    with rasterio.open(file) as src:
        # 读取影像数据
        image = src.read(1)  # 如果是多波段影像，可以选择读取其中一个波段

    # 将像素值均分为4个区间
    num_bins = 4
    hist, bin_edges = np.histogram(image, bins=num_bins, range=[image.min(), image.max()])


    # 统计每个区间内的像素值数量和百分比
    total_pixels = len(image.flatten())

    pixelData = []
    for i in range(num_bins):
        bin_range = f'{bin_edges[i]:.2f}-{bin_edges[i+1]:.2f}'
        bin_percentage = (hist[i] / total_pixels) * 100
        data_entry = {
            'name': '区间：' + bin_range + '（' + f'{bin_percentage:.2f}' + '%' + '）',
            'value': int(hist[i])
        }
        pixelData.append(data_entry)
    return json.dumps(pixelData)
