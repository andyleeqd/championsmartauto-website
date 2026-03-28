#!/usr/bin/env python3
"""
Extract and format car specification data from Chinese car websites.

This script takes car specification data and converts it to CSV format
with proper formatting for both Chinese and English versions.
"""

import csv
import re
import sys
from typing import List, Tuple, Dict

# Chinese category to English category mapping
CATEGORY_MAP = {
    "基本信息": "Basic Information",
    "车身": "Body",
    "发动机": "Engine",
    "变速箱": "Transmission",
    "底盘/转向": "Chassis/Steering",
    "车轮/制动": "Wheels/Brakes",
    "主动安全": "Active Safety",
    "被动安全": "Passive Safety",
    "辅助/操控配置": "Driving Assistance",
    "外部配置": "Exterior",
    "内部配置": "Interior",
    "座椅配置": "Seats",
    "智能互联": "Intelligent Connectivity",
    "影音娱乐": "Infotainment",
    "灯光配置": "Lighting",
    "玻璃/后视镜": "Windows/Mirrors",
    "空调/冰箱": "AC/Refrigerator",
    "智能化配置": "Smart Technology",
    "选装包": "Optional Packages",
}

# Complete English translation table - CRITICAL for complete English CSV
# Sorted by length descending to avoid partial replacements
SPEC_TRANSLATIONS = {
    # Price & Warranty (longer first)
    "终身质保(责任免除条款以官方为准)": "Lifetime warranty (subject to official liability exclusion clauses)",
    "4年或10万公里": "4 years or 100,000 km",
    "3年或10万公里": "3 years or 100,000 km",
    "14.99万": "149,900 RMB",
    "16.99万": "169,900 RMB",

    # Configuration markers (longer first to avoid partial matches)
    "●标配": "● Standard",
    "○选配3000元": "○ Optional (3000 RMB)",
    "○选配2000元": "○ Optional (2000 RMB)",
    "○选配": "○ Optional",
    "●前": "● Front",
    "●后": "● Rear",
    "●主驾驶位": "● Driver",
    "●副驾驶位": "● Passenger",
    "●前排": "● Front",
    "●后排": "● Rear",
    "●全车": "● All",
    "●第二排": "● 2nd Row",
    "●第三排": "● 3rd Row",

    # Manufacturers
    "奇瑞汽车": "Chery Automobile",
    "长城汽车": "Great Wall Motor",
    "比亚迪": "BYD",
    "吉利汽车": "Geely",
    "长安汽车": "Changan Automobile",

    # Segments
    "紧凑型SUV": "Compact SUV",
    "中型SUV": "Mid-size SUV",
    "中大型SUV": "Full-size SUV",
    "小型SUV": "Subcompact SUV",
    "紧凑型轿车": "Compact Sedan",

    # Body structures
    "5门5座SUV": "5-door, 5-seat SUV",
    "5门7座SUV": "5-door, 7-seat SUV",
    "4门5座轿车": "4-door, 5-seat Sedan",

    # Transmission
    "7挡湿式双离合（DCT）": "7-speed Wet DCT",
    "湿式双离合变速箱（DCT）": "Wet DCT",
    "7挡双离合": "7-speed DCT",
    "8挡手自一体": "8-speed AT",
    "6挡手动": "6-speed Manual",
    "CVT无级变速": "CVT",
    "双离合": "DCT",

    # Engine
    "涡轮增压": "Turbocharged",
    "自然吸气": "Naturally Aspirated",
    "自吸": "Naturally Aspirated",
    "横置": "Transverse",
    "纵置": "Longitudinal",
    "L型": "L",
    "V型": "V",
    "W型": "W",
    "缸内直喷": "Direct Injection",
    "多点电喷": "Multi-point Injection",

    # Fuel
    "插电混动": "Plug-in Hybrid",
    "油电混动": "Hybrid",
    "汽油": "Gasoline",
    "柴油": "Diesel",
    "纯电动": "Electric",

    # Materials
    "铝合金": "Aluminum Alloy",
    "铸铁": "Cast Iron",
    "Alcantara": "Alcantara",

    # Emissions
    "国VI": "China VI",
    "国V": "China V",

    # Drive type
    "适时四驱": "On-demand 4WD",
    "分时四驱": "Part-time 4WD",
    "全时四驱": "Full-time 4WD",
    "前置前驱": "FWD",
    "前置四驱": "4WD",
    "后置后驱": "RWD",

    # Suspension (longer first)
    "麦弗逊式独立悬挂": "MacPherson Independent",
    "多连杆式独立悬挂": "Multi-link Independent",
    "扭力梁式非独立悬挂": "Torsion Beam",
    "双叉臂式独立悬挂": "Double Wishbone",
    "整体桥式非独立悬挂": "Solid Axle",

    # Steering
    "电动助力": "Electric Power Steering",
    "机械液压助力": "Hydraulic Power Steering",

    # Brakes
    "通风盘式": "Vented Disc",
    "实心盘式": "Solid Disc",
    "电子驻车": "Electronic Parking Brake",
    "手刹": "Hand Brake",
    "脚刹": "Foot Brake",

    # Body structure type
    "承载式": "Unibody",
    "非承载式": "Body-on-frame",

    # Door type
    "平开门": "Standard",
    "侧滑门": "Sliding Door",
    "鸥翼门": "Gullwing",
    "剪刀门": "Scissor Door",

    # Spare tire
    "全尺寸": "Full-size",
    "非全尺寸": "Temporary",
    "背负式": "Rear-mounted",

    # Camera
    "360°全景影像": "360° Surround View",
    "车侧盲区影像": "Side-view Camera",
    "倒车影像": "Backup Camera",
    "透明影像": "Transparent Chassis View",

    # Cruise
    "全速自适应巡航": "Full-speed ACC",
    "自适应巡航": "Adaptive Cruise Control",
    "定速巡航": "Cruise Control",

    # ADAS Level
    "L2级": "L2",
    "L2+": "L2+",
    "L3级": "L3",

    # Shifter
    "电子挡把": "Electronic Gear Stick",
    "旋钮式": "Rotary Dial",
    "怀挡": "Column Shifter",

    # Display
    "全液晶": "Full Digital",
    "传统": "Traditional",

    # Key
    "智能遥控钥匙": "Smart Remote Key",
    "手机蓝牙钥匙": "Bluetooth Phone Key",
    "手机NFC钥匙": "NFC Key",

    # Side steps
    "固定": "Fixed",
    "电动": "Electric",
    "手动": "Manual",

    # Navigation
    "高德": "Amap",
    "百度": "Baidu",
    "腾讯": "Tencent",

    # Phone connect (longer first)
    "HUAWEI HiCar": "HUAWEI HiCar",
    "HiCar": "HiCar",
    "CarPlay": "CarPlay",
    "Android Auto": "Android Auto",
    "MirrorLink": "MirrorLink",

    # Voice assistant (longer first)
    "你好小捷": "Hi Jietour",
    "你好博越": "Hi Boyue",
    "你好哈弗": "Hi Haval",
    "你好逸动": "Hi Eado",
    "你好吉利": "Hi Geely",
    "你好奇瑞": "Hi Chery",

    # Seat positions (longer markers first)
    "主驾驶位": "Driver",
    "副驾驶位": "Passenger",
    "第二排": "2nd Row",
    "第三排": "3rd Row",
    "前排": "Front",
    "后排": "Rear",
    "全车": "All",

    # Common short terms
    "标配": "Standard",
    "选配": "Optional",

    # Seat adjustments
    "前后移动": "Fore/Aft",
    "靠背角度调节": "Recline",
    "靠背角度": "Recline",
    "高低调节": "Height",
    "头枕": "Headrest",
    "腰部": "Lumbar",
    "腿托": "Leg Rest",

    # Seat features
    "加热": "Heated",
    "通风": "Ventilated",
    "按摩": "Massage",
    "记忆": "Memory",

    # Driving modes
    "标准舒适": "Standard",
    "运动": "Sport",
    "越野": "Off-road",
    "雪地": "Snow",
    "ECO/经济": "ECO",

    # Steering wheel (longer first)
    "上下+前后": "Tilt & Telescope",
    "多功能控制": "Multi-function",
    "换挡": "Shift Paddles",

    # Sunroof (longer first)
    "可开启全景天窗": "Openable Panoramic Sunroof",
    "全景天窗": "Panoramic Sunroof",
    "电动天窗": "Electric Sunroof",
    "普通天窗": "Standard Sunroof",

    # Glass
    "后排隐私玻璃": "Rear Privacy Glass",
    "多层隔音玻璃": "Acoustic Glass (Front)",

    # Wipers
    "雨量感应式雨刷": "Rain-sensing Wipers",
    "自动雨刷": "Automatic Wipers",
    "后雨刷": "Rear Wiper",

    # Mirrors
    "电动调节": "Electric Adjustment",
    "电动折叠": "Power Folding",
    "倒车自动下翻": "Auto-tilt in Reverse",
    "锁车自动折叠": "Auto-fold on Lock",

    # Vanity mirror (longer first)
    "车内化妆镜(无照明)": "Vanity Mirror (No Light)",
    "车内化妆镜(带照明)": "Vanity Mirror (With Light)",
    "Driver+无照明": "Driver + No Light",
    "Passenger+无照明": "Passenger + No Light",
    "主驾驶位+无照明": "Driver + No Light",
    "副驾驶位+无照明": "Passenger + No Light",

    # Lights
    "多色": "Multi-color",
    "LED": "LED",
    "卤素": "Halogen",
    "氙气": "Xenon",
    "激光": "Laser",

    # Climate
    "自动空调": "Automatic",
    "手动空调": "Manual",
    "三区": "Tri-zone",
    "双区": "Dual-zone",
    "单区": "Single-zone",

    # USB
    "前排3个": "Front: 3",
    "后排2个": "Rear: 2",

    # Soft-close doors
    "电动吸合门": "Electric Soft-close Doors",
    "吸合门": "Soft-close Doors",

    # Common suffixes to remove/replace
    "(个)": "",
    "(英寸)": " (inches)",
    "(EBD/CBC等)": "",
    "等": "",

    # Other
    "马力": "hp",
    "胎压显示": "Tire Pressure Display",
    "未提供": "-",
    "N/A": "-",
}

# Sort by length descending to ensure longer strings are replaced first
SORTED_TRANSLATIONS = sorted(SPEC_TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)


def translate_value(value: str) -> str:
    """
    Translate specification values from Chinese to English.
    Uses sorted translations for best results.
    """
    if not value or value == "-" or value == "未提供":
        return "-"

    # Replace "未提供(需加价)" with "-"
    value = value.replace("未提供(需加价)", "-")

    # Apply all translations in length order (longest first)
    for cn, en in SORTED_TRANSLATIONS:
        value = value.replace(cn, en)

    return value


def verify_no_chinese(file_path: str) -> bool:
    """
    Verify that the English CSV file contains NO Chinese characters.

    Returns:
        True if no Chinese found, False otherwise
    """
    import csv
    chinese_found = []
    
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader, 1):
            for j, cell in enumerate(row, 1):
                if any('\u4e00' <= c <= '\u9fff' for c in cell):
                    chinese_found.append(f"Line {i}, Col {j}: {cell[:50]}")
    
    if chinese_found:
        print(f"❌ Found {len(chinese_found)} cells with Chinese:")
        for item in chinese_found[:20]:
            print(f"  {item}")
        if len(chinese_found) > 20:
            print(f"  ... and {len(chinese_found) - 20} more")
        return False
    
    print("✅ SUCCESS! No Chinese characters found!")
    return True


def translate_category(category: str) -> str:
    """Translate Chinese category name to English."""
    return CATEGORY_MAP.get(category, category)


def create_specs_csv(
    specs: List[Tuple[str, str]],
    output_path: str,
    translate: bool = False
) -> None:
    """
    Create a CSV file with car specifications.

    Args:
        specs: List of (parameter_name, specification_value) tuples
        output_path: Output file path
        translate: Whether to translate to English
    """
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(["Parameter Name", "Specification"])

        for param, value in specs:
            if translate:
                # Translate parameter if it's a category
                if param and not value and param in CATEGORY_MAP:
                    param = CATEGORY_MAP[param]
                elif value:
                    value = translate_value(value)

            writer.writerow([param if param else "", value if value else ""])


def parse_dongchedi_data(text: str, model_index: int) -> List[Tuple[str, str]]:
    """
    Parse car specification data from Dongchedi website.

    Args:
        text: HTML or text content from the page
        model_index: Index of the model to extract (0-based)

    Returns:
        List of (category, parameter, value) tuples
    """
    # This is a simplified parser - in production, use proper HTML parsing
    # For now, return empty list - the actual parsing should be done
    # by reading the web_fetch result and extracting data

    print("Error: Please provide actual specification data")
    print("This script is designed to format extracted data, not scrape websites")
    sys.exit(1)


if __name__ == "__main__":
    print("Car Specifications Extractor")
    print("=" * 50)
    print()
    print("This script formats car specification data into CSV files.")
    print("Use it from OpenClaw skill workflow, not directly.")
    print()
    print("For standalone usage, prepare specs data as list of")
    print("(parameter_name, specification_value) tuples and call:")
    print("  create_specs_csv(specs, output_path)")
