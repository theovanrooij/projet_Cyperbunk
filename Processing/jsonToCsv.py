# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 02:42:58 2022

@author: 50340
"""

import json
import csv

"""
需求：将json中的数据转换成csv文件
"""
def csv_json():
    json_fp = open("./booknode.json", "r",encoding='utf-8')
    csv_fp = open("./word.csv", "w",encoding='utf-8',newline='')

    data_list = json.load(json_fp)
    sheet_title = data_list[0].keys()
    sheet_data = []
    for data in data_list:
        sheet_data.append(data.values())

    writer = csv.writer(csv_fp)

    writer.writerow(sheet_title)

    writer.writerows(sheet_data)

    json_fp.close()
    csv_fp.close()


if __name__ == "__main__":
    csv_json()