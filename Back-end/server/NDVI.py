# -*- coding: utf-8 -*-
import gdal2tiles
from osgeo import gdal
import numpy as np
import os

import sql


def calculate_ndvi(red_band, nir_band):
    # 忽略除法时的警告
    np.seterr(divide='ignore', invalid='ignore')
    # 计算 NDVI
    ndvi = (nir_band - red_band) / (nir_band + red_band)
    return ndvi

def main(input_path, output_path, red_band_number, nir_band_number):
    # 打开遥感影像
    dataset = gdal.Open(input_path, gdal.GA_ReadOnly)

    # 读取红光波段和近红外波段
    red_band = dataset.GetRasterBand(red_band_number).ReadAsArray().astype(np.float32)
    nir_band = dataset.GetRasterBand(nir_band_number).ReadAsArray().astype(np.float32)

    # 计算 NDVI
    ndvi = calculate_ndvi(red_band, nir_band)

    # 如果输出文件已经存在，删除它
    if os.path.exists(output_path):
        os.remove(output_path)
    # 创建输出影像
    driver = gdal.GetDriverByName('GTiff')
    ndvi_dataset = driver.Create(output_path, dataset.RasterXSize, dataset.RasterYSize, 1, gdal.GDT_Float32)
    ndvi_dataset.SetGeoTransform(dataset.GetGeoTransform())
    ndvi_dataset.SetProjection(dataset.GetProjection())
    ndvi_band = ndvi_dataset.GetRasterBand(1)

    # 将 NDVI 写入影像
    ndvi_band.WriteArray(ndvi)

    # 关闭数据集
    dataset = None
    ndvi_dataset = None



# 数据切片
def generateTiles(input, output):
    gdal2tiles.generate_tiles(input,
                              output,
                              np_process=2,
                              zoom='6-12',
                              srcnodata=0
                              )

def startNDVI(id, name):
    input_image_path = "./data/Img_Origin/" + name + ".tif"
    output_ndvi_path = "./data/Img_Res/" + name + "_Res.tif"
    output_tile_ndvi_path = "./data/Img_Tiles/" + name + "_Tiles/"

    # 定义红光和近红外波段的波段号
    red_band_number = 3
    nir_band_number = 4

    main(input_image_path, output_ndvi_path, red_band_number, nir_band_number)


    # 将结果地址存入数据库
    sql.resSaveSql(output_ndvi_path[7:], id, 'res')

    # 切片
    generateTiles(input_image_path, output_tile_ndvi_path)

    # 将切片地址存入数据库
    sql.resSaveSql(output_tile_ndvi_path[7:], id, 'tile')

    return 'OK'
