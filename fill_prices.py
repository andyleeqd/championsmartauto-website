#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 HONGQI Order.xlsx 文件中 G 列的价格复制到 H 列
"""

import os
import pandas as pd

# Windows 桌面路径
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
excel_file = os.path.join(desktop_path, "HONGQI Order.xlsx")

print(f"读取文件: {excel_file}")

# 读取 Excel 文件
df = pd.read_excel(excel_file, engine='openpyxl')

print(f"文件共有 {len(df)} 行数据")
print(f"列名: {list(df.columns)}")
print(f"G 列前5行: {df.iloc[:5, 6].tolist()}")  # G 列是第7列，索引6
print(f"H 列前5行: {df.iloc[:5, 7].tolist()}")  # H 列是第8列，索引7

# 检查 G 列是否有数据
if df.shape[1] >= 7:
    g_column = df.columns[6]  # G 列
    print(f"\nG 列列名: {g_column}")
    print(f"G 列非空数量: {df[g_column].notna().sum()}")
    
    # 把 G 列的值复制到 H 列
    if df.shape[1] >= 8:
        h_column = df.columns[7]  # H 列
        df[h_column] = df[g_column]
        print(f"\n已将 G 列的值复制到 H 列")
    else:
        # 如果 H 列不存在，创建它
        df['H'] = df[g_column]
        print(f"\n已创建 H 列并复制 G 列的值")
    
    # 保存文件
    df.to_excel(excel_file, index=False, engine='openpyxl')
    print(f"\n文件已保存!")
    
    # 验证结果
    print(f"\n验证 - H 列前5行: {df.iloc[:5, 7].tolist()}")
else:
    print("\n错误: 文件中 G 列不存在!")