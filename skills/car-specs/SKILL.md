---
name: car-specs
description: Extract car specification sheets from Chinese car websites (Dongchedi, Autohome) into professional CSV files with Chinese and English versions. Use when creating car spec documents, comparing car models, preparing vehicle documentation, maintaining spec databases, or translating Chinese car specs.
---

# Car Specifications Formatter

Extract and format car specification data from Chinese car websites into professional CSV files with both Chinese and English versions.

## Quick Start

1. **Fetch car spec data**: Use `web_fetch` to get the specification page from Dongchedi/Autohome
2. **Extract specifications**: Parse the data maintaining original order and parameter names
3. **Generate CSV files**: Create Chinese and English versions with proper formatting

## Data Sources

Supported websites:
- **Dongchedi** (懂车帝): https://www.dongchedi.com/auto/params-carIds-{id}
- **Autohome** (汽车之家): https://www.autohome.com.cn/spec/{id}/
- Alternative sources with similar spec layout

## Format Rules

### File Format

- **Format**: CSV (UTF-8-BOM, Excel compatible)
- **Structure**: Two columns
  - Column A: Parameter Name (参数名称)
  - Column B: Specification (规格内容)
- **Encoding**: UTF-8-BOM (ensures Excel displays Chinese correctly)

### Category Headers

- **Format**: Pure text, Column B left empty
- **Example**: `基本信息,`
- **Do NOT use**: `=== 分类名称 ===` (symbols)
- **Purpose**: Separate and organize specification sections

### Empty Value Handling

- Replace all "未提供", "N/A", or similar with single hyphen: `-`

### Configuration Markers

- `●标配` (Chinese) → `● Standard` (English)
- `○选配` (Chinese) → `○ Optional` (English)
- Keep original markers (●/○) intact

## Data Extraction Rules

### Strict Order Preservation

1. **Maintain original web page order** - Do not reorder parameters
2. **Keep parameter names unchanged** - Even if duplicates exist
3. **Do not de-duplicate** - If the same parameter appears in multiple sections, keep all occurrences
4. **Do not skip any parameters** - All 300+ parameters must be included

### Common Duplicate Parameters

These parameters may appear in multiple sections - keep all instances:
- `最大功率(kW)` - in Basic Info and Engine sections
- `最大扭矩(N·m)` - in Basic Info and Engine sections
- `车身结构` - in Basic Info and Body sections
- Repeat parameter names as they appear on the website

## English Translation Rules

### CRITICAL REQUIREMENT

**ALL CHINESE TEXT MUST BE TRANSLATED TO ENGLISH** - The English CSV file must contain NO Chinese characters. Every parameter name, category header, and specification value must be translated.

### Categories

Translate category headers to concise English:
- 基本信息 → Basic Information
- 车身 → Body
- 发动机 → Engine
- 变速箱 → Transmission
- 底盘/转向 → Chassis/Steering
- 车轮/制动 → Wheels/Brakes
- 主动安全 → Active Safety
- 被动安全 → Passive Safety
- 辅助/操控配置 → Driving Assistance
- 外部配置 → Exterior
- 内部配置 → Interior
- 座椅配置 → Seats
- 智能互联 → Intelligent Connectivity
- 影音娱乐 → Infotainment
- 灯光配置 → Lighting
- 玻璃/后视镜 → Windows/Mirrors
- 空调/冰箱 → AC/Refrigerator
- 智能化配置 → Smart Technology

### Complete English Translation Table

#### Price & Warranty
- 14.99万 → 149,900 RMB
- 16.99万 → 169,900 RMB
- 4年或10万公里 → 4 years or 100,000 km
- 终身质保(责任免除条款以官方为准) → Lifetime warranty (subject to official liability exclusion clauses)

#### Manufacturers
- 奇瑞汽车 → Chery Automobile
- 长城汽车 → Great Wall Motor
- 比亚迪 → BYD
- 吉利汽车 → Geely
- 长安汽车 → Changan Automobile

#### Segments
- 紧凑型SUV → Compact SUV
- 中型SUV → Mid-size SUV
- 中大型SUV → Full-size SUV
- 小型SUV → Subcompact SUV
- 紧凑型轿车 → Compact Sedan

#### Body Structures
- 5门5座SUV → 5-door, 5-seat SUV
- 5门7座SUV → 5-door, 7-seat SUV
- 4门5座轿车 → 4-door, 5-seat Sedan
- SUV → SUV
- 轿车 → Sedan

#### Transmission
- 7挡双离合 → 7-speed DCT
- 8挡手自一体 → 8-speed AT
- 6挡手动 → 6-speed Manual
- CVT无级变速 → CVT
- 7挡湿式双离合（DCT） → 7-speed Wet DCT
- 湿式双离合变速箱（DCT） → Wet DCT

#### Engine
- 涡轮增压 → Turbocharged
- 自然吸气/自吸 → Naturally Aspirated
- 横置 → Transverse
- 纵置 → Longitudinal
- L型 → L
- V型 → V
- W型 → W
- 缸内直喷 → Direct Injection
- 多点电喷 → Multi-point Injection
- DOHC → DOHC
- SOHC → SOHC

#### Fuel
- 汽油 → Gasoline
- 柴油 → Diesel
- 纯电动 → Electric
- 插电混动 → Plug-in Hybrid
- 油电混动 → Hybrid
- 92#/95# → 92#/95#

#### Materials
- 铝合金 → Aluminum Alloy
- 铸铁 → Cast Iron
- 皮质 → Leather
- 真皮 → Genuine Leather
- 仿皮 → Synthetic Leather
- 织物 → Cloth
- Alcantara → Alcantara

#### Emissions
- 国VI → China VI
- 国V → China V

#### Drive Type
- 前置前驱 → FWD
- 前置四驱 → 4WD
- 后置后驱 → RWD
- 适时四驱 → On-demand 4WD
- 分时四驱 → Part-time 4WD
- 全时四驱 → Full-time 4WD

#### Suspension
- 麦弗逊式独立悬挂 → MacPherson Independent
- 多连杆式独立悬挂 → Multi-link Independent
- 扭力梁式非独立悬挂 → Torsion Beam
- 双叉臂式独立悬挂 → Double Wishbone
- 整体桥式非独立悬挂 → Solid Axle

#### Steering
- 电动助力 → Electric Power Steering
- 机械液压助力 → Hydraulic Power Steering

#### Brakes
- 通风盘式 → Vented Disc
- 实心盘式 → Solid Disc
- 盘式 → Disc
- 鼓式 → Drum
- 电子驻车 → Electronic Parking Brake
- 手刹 → Hand Brake
- 脚刹 → Foot Brake

#### Body Structure Type
- 承载式 → Unibody
- 非承载式 → Body-on-frame

#### Door Type
- 平开门 → Standard
- 侧滑门 → Sliding Door
- 鸥翼门 → Gullwing
- 剪刀门 → Scissor Door

#### Spare Tire
- 全尺寸 → Full-size
- 非全尺寸 → Temporary
- 背负式 → Rear-mounted

#### Camera
- 倒车影像 → Backup Camera
- 车侧盲区影像 → Side-view Camera
- 360°全景影像 → 360° Surround View
- 透明影像 → Transparent Chassis View

#### Cruise Control
- 定速巡航 → Cruise Control
- 自适应巡航 → Adaptive Cruise Control
- 全速自适应巡航 → Full-speed ACC

#### ADAS Level
- L2级 → L2
- L2+ → L2+
- L3级 → L3

#### Shifter
- 电动挡把 → Electronic Gear Stick
- 旋钮式 → Rotary Dial
- 怀挡 → Column Shifter

#### Display
- 全液晶 → Full Digital
- 传统 → Traditional
- LCD → LCD
- OLED → OLED

#### Key
- 智能遥控钥匙 → Smart Remote Key
- 手机蓝牙钥匙 → Bluetooth Phone Key
- 手机NFC钥匙 → NFC Key

#### Side Steps
- 固定 → Fixed
- 电动 → Electric
- 手动 → Manual

#### Navigation
- 高德 → Amap
- 百度 → Baidu
- 腾讯 → Tencent

#### Phone Connectivity
- CarPlay → CarPlay
- HUAWEI HiCar → HUAWEI HiCar
- HiCar → HiCar
- Android Auto → Android Auto
- MirrorLink → MirrorLink

#### Network
- 4G → 4G
- 5G → 5G

#### Voice Assistant
- 你好小捷 → Hi Jietour
- 你好博越 → Hi Boyue
- 你好哈弗 → Hi Haval
- 你好逸动 → Hi Eado
- 你好吉利 → Hi Geely
- 你好奇瑞 → Hi Chery

#### Configuration Markers
- ●标配 → ● Standard
- ○选配3000元 → ○ Optional (3000 RMB)
- ○选配2000元 → ○ Optional (2000 RMB)
- ○选配 → ○ Optional
- ●前 → ● Front
- ●后 → ● Rear
- ●主驾驶位 → ● Driver
- ●副驾驶位 → ● Passenger
- ●前排 → ● Front
- ●后排 → ● Rear
- ●全车 → ● All
- ●第二排 → ● 2nd Row
- ●第三排 → ● 3rd Row
- 标配 → Standard
- 选配 → Optional

#### Seat Adjustments
- 前后移动 → Fore/Aft
- 靠背角度调节/靠背角度 → Recline
- 高低调节 → Height
- 头枕 → Headrest
- 腰部 → Lumbar
- 腿托 → Leg Rest

#### Seat Features
- 加热 → Heated
- 通风 → Ventilated
- 按摩 → Massage
- 记忆 → Memory

#### Driving Modes
- 运动 → Sport
- 越野 → Off-road
- 雪地 → Snow
- ECO/经济 → ECO
- 标准舒适 → Standard

#### Steering Wheel Features
- 上下+前后 → Tilt & Telescope
- 上下调节 → Tilt
- 前后调节 → Telescope
- 多功能控制 → Multi-function
- 换挡 → Shift Paddles

#### Sunroof
- 可开启全景天窗 → Openable Panoramic Sunroof
- 全景天窗 → Panoramic Sunroof
- 电动天窗 → Electric Sunroof
- 普通天窗 → Standard Sunroof

#### Glass
- 后排隐私玻璃 → Rear Privacy Glass
- 多层隔音玻璃 → Acoustic Glass (Front)
- 前排 → Front
- 后排 → Rear

#### Wipers
- 雨量感应式雨刷 → Rain-sensing Wipers
- 自动雨刷 → Automatic Wipers
- 前后雨刷 → Front and Rear Wipers
- 后雨刷 → Rear Wiper

#### Mirrors
- 电动调节 → Electric Adjustment
- 电动折叠 → Power Folding
- 倒车自动下翻 → Auto-tilt in Reverse
- 锁车自动折叠 → Auto-fold on Lock
- 记忆 → Memory

#### Vanity Mirror
- 车内化妆镜(无照明) → Vanity Mirror (No Light)
- 车内化妆镜(带照明) → Vanity Mirror (With Light)
- Driver+无照明/主驾驶位+无照明 → Driver + No Light
- Passenger+无照明/副驾驶位+无照明 → Passenger + No Light

#### Lights
- LED → LED
- 卤素 → Halogen
- 氙气 → Xenon
- 激光 → Laser
- 多色 → Multi-color

#### Climate Control
- 自动空调 → Automatic
- 手动空调 → Manual
- 三区 → Tri-zone
- 双区 → Dual-zone
- 单区 → Single-zone

#### USB Ports
- 前排3个 → Front: 3
- 后排2个 → Rear: 2

#### Electric Soft-close Doors
- 电动吸合门 → Electric Soft-close Doors
- 吸合门 → Soft-close Doors

#### Unit Suffixes
- (个) → (remove - just use the number)
- (英寸) → (inches)
- (EBD/CBC等) → (remove)
- 等 → (remove)

#### Horsepower
- 马力 → hp

#### TPMS
- 胎压显示 → Tire Pressure Display

#### Positions (Long forms)
- 主驾驶位 → Driver
- 副驾驶位 → Passenger
- 前排 → Front
- 后排 → Rear
- 第二排 → 2nd Row
- 第三排 → 3rd Row
- 全车 → All

#### Parameter Names (Complete)
- 官方指导价 → Official Price
- 厂商 → Manufacturer
- 级别 → Segment
- 能源类型 → Energy Type
- 上市时间 → Launch Date
- 发动机 → Engine
- 变速箱 → Transmission
- 长/宽/高 → Length/Width/Height
- 车身结构 → Body Structure
- 最高车速 → Max Speed
- 官方百公里加速时间 → 0-100km/h Acceleration
- WLTC综合油耗 → WLTC Combined Fuel Consumption
- 整车保修期限 → Warranty Period
- 首任车主保修期限 → First Owner Warranty
- 轴距 → Wheelbase
- 前轮距 → Front Track
- 后轮距 → Rear Track
- 最小离地间隙 → Min Ground Clearance
- 车门数 → Doors
- 车门开启方式 → Door Opening Type
- 座位数 → Seats
- 整备质量 → Curb Weight
- 满载质量 → Max Load
- 油箱容积 → Fuel Tank Capacity
- 行李舱容积 → Trunk Volume
- 最小转弯半径 → Turning Radius
- 发动机型号 → Engine Model
- 排量 → Displacement
- 进气形式 → Intake Type
- 发动机布局形式 → Engine Layout
- 气缸排列形式 → Cylinder Configuration
- 气缸数 → Cylinders
- 每缸气门数 → Valves per Cylinder
- 压缩比 → Compression Ratio
- 配气机构 → Valve Train
- 最大马力 → Max Horsepower
- 最大功率 → Max Power
- 最大净功率 → Max Net Power
- 最大功率转速 → Max Power RPM
- 最大扭矩 → Max Torque
- 最大扭矩转速 → Max Torque RPM
- 发动机特有技术 → Engine Technology
- 燃料形式 → Fuel Type
- 燃油标号 → Fuel Rating
- 供油方式 → Fuel Injection
- 缸盖材料 → Cylinder Head Material
- 缸体材料 → Cylinder Block Material
- 环保标准 → Emission Standard
- 变速箱描述 → Transmission Description
- 挡位数 → Gears
- 变速箱类型 → Transmission Type
- 驱动方式 → Drive Type
- 四驱类型 → 4WD Type
- 中央差速器结构 → Center Differential
- 前悬挂形式 → Front Suspension
- 后悬挂形式 → Rear Suspension
- 转向类型 → Steering Type
- 车体结构 → Body Structure Type
- 前制动器类型 → Front Brake Type
- 后制动器类型 → Rear Brake Type
- 驻车制动类型 → Parking Brake Type
- 前轮胎规格尺寸 → Front Tire Size
- 后轮胎规格尺寸 → Rear Tire Size
- 备胎规格 → Spare Tire
- 备胎放置方式 → Spare Tire Placement
- ABS防抱死 → ABS
- 制动力分配 → EBD/CBC
- 刹车辅助 → Brake Assist
- 牵引力控制 → Traction Control
- 车身稳定系统 → ESP
- 车道偏离预警 → Lane Departure Warning
- 前方碰撞预警 → Forward Collision Warning
- 后方碰撞预警 → Rear Collision Warning
- 倒车车侧预警 → Rear Cross Traffic Alert
- DOW开门预警 → Door Open Warning
- 主动刹车 → Autonomous Emergency Braking
- 并线辅助 → Blind Spot Monitor
- 车道保持辅助系统 → Lane Keep Assist
- 车道居中保持 → Lane Centering
- 疲劳驾驶提示 → Fatigue Alert
- 主动式DMS疲劳检测 → DMS Fatigue Detection
- 车内生命体征检测 → Passenger Presence Detection
- 道路交通标识识别 → Traffic Sign Recognition
- 信号灯识别 → Traffic Light Recognition
- 夜视系统 → Night Vision
- 前排安全气囊(主驾驶位) → Front Airbag (Driver)
- 前排安全气囊(副驾驶位) → Front Airbag (Passenger)
- 侧安全气囊 → Side Airbags
- 侧安全气帘 → Side Curtains
- 前排膝部气囊 → Knee Airbags
- 中央安全气囊 → Center Airbag
- 安全带未系提示 → Seatbelt Warning
- 胎压监测系统 → TPMS
- 儿童座椅接口(ISOFIX) → ISOFIX
- 被动行人保护 → Pedestrian Protection
- 安全轮胎 → Run-flat Tires
- 驻车雷达-前 → Parking Radar - Front
- 驻车雷达-后 → Parking Radar - Rear
- 前车驶离提醒 → Vehicle Departure Alert
- 驾驶辅助影像 → Driving Assistance Camera
- 巡航系统 → Cruise Control
- 自动变道辅助 → Automatic Lane Change
- 匝道自动驶出（入） → Ramp Assist
- 导航辅助驾驶 → Navigation Assist
- 辅助驾驶级别 → ADAS Level
- 自动泊车入位 → Auto Parking
- 循迹倒车 → Trail Reversing
- 记忆泊车 → Memory Parking
- 自动驻车 → Auto Hold
- 上坡辅助 → Hill Start Assist
- 陡坡缓降 → Hill Descent Control
- 发动机启停技术 → Auto Start/Stop
- 可变悬挂调节 → Adjustable Suspension
- 空气悬挂 → Air Suspension
- 空气悬挂类型 → Air Suspension Type
- 电磁感应悬挂 → Magnetic Suspension
- 可变转向比系统 → Variable Steering Ratio
- 前桥限滑方式 → Front Limited-slip
- 后桥限滑方式 → Rear Limited-slip
- 中央差速器锁止功能 → Center Diff Lock
- 低速四驱 → Low Range 4WD
- 整体主动转向系统 → Active Steering
- 蠕行模式 → Crawl Mode
- 驾驶模式选择 → Driving Modes
- 涉水感应系统 → Water Level Detection
- 天窗类型 → Sunroof Type
- 智能调光天幕 → Smart Glass Roof
- 车顶行李架 → Roof Rack
- 运动外观套件 → Sport Package
- 电动扰流板 → Active Spoiler
- 主动闭合式进气格栅 → Active Grille Shutter
- 铝合金轮毂 → Aluminum Wheels
- 车侧脚踏板 → Side Steps
- 无框设计车门 → Frameless Doors
- 隐藏式门把手 → Hidden Door Handles
- 拖挂钩 → Towing Hitch
- 舒适/防盗配置 → Comfort and Security
- 方向盘材质 → Steering Wheel Material
- 方向盘调节 → Steering Adjustment
- 方向盘电动调节 → Electric Steering Adjustment
- 方向盘功能 → Steering Wheel Functions
- 换挡形式 → Shifter Type
- 液晶仪表样式 → Instrument Display Type
- 液晶仪表尺寸 → Instrument Display Size
- 电动吸合门 → Soft Close Doors
- 电动吸合尾门 → Power Tailgate
- 感应式后尾门 → Hands-free Tailgate
- 电动后尾门位置记忆 → Tailgate Memory
- 发动机电子防盗 → Engine Immobilizer
- 车内中控锁 → Central Locking
- 遥控钥匙类型 → Remote Key Type
- 无钥匙进入 → Keyless Entry
- 无钥匙启动 → Keyless Start
- 远程启动 → Remote Start
- 遥控移动车辆 → Remote Move
- 车辆召唤功能 → Summon
- 抬头显示系统 → HUD
- 内置行车记录仪 → Dashcam
- 主动降噪 → Active Noise Cancellation
- 手机无线充电 → Wireless Phone Charger
- 手机无线充电最大功率 → Wireless Charging Max Power
- 电源插座/110V/220V/230V电源插座 → Power Outlet
- 行李舱12V电源接口 → Trunk 12V Outlet
- 座椅材质 → Seat Material
- 座椅布局 → Seat Layout
- 第二排独立座椅 → 2nd Row Captain Seats
- 第三排座椅 → 3rd Row Seats
- 座椅电动调节 → Power Seat Adjustment
- 下沉式后排座椅收折 → Fold-flat Rear Seats
- 主驾座椅整体调节 → Driver Seat Adjustment
- 主驾座椅局部调节 → Driver Seat Local Adjustment
- 副驾座椅整体调节 → Passenger Seat Adjustment
- 副驾座椅局部调节 → Passenger Seat Local Adjustment
- 第二排座椅整体调节 → 2nd Row Adjustment
- 第二排座椅局部调节 → 2nd Row Local Adjustment
- 前排座椅功能 → Front Seat Features
- 第二排座椅功能 → 2nd Row Features
- 第三排座椅功能 → 3rd Row Features
- 老板键 → Boss Button
- 前/后扶手 → Front/Rear Armrests
- 后排杯架 → Rear Cup Holders
- 可加热/制冷杯架 → Heated/Cooled Cup Holders
- 后排座椅放倒比例 → Rear Seat Fold Ratio
- 后排座椅电动放倒 → Power Rear Seat Fold
- 第二排小桌板 → 2nd Row Tray Table
- 中控屏尺寸 → Central Screen Size
- 中控屏幕材质 → Screen Material
- 中控台彩色屏幕分辨率 → Screen Resolution
- 副驾驶屏幕尺寸 → Passenger Screen Size
- 卫星导航系统 → GPS Navigation
- 导航路况信息展示 → Real-time Traffic
- AR实景导航 → AR Navigation
- 地图品牌 → Map Provider
- 道路救援服务 → Roadside Assistance
- 蓝牙/车载电话 → Bluetooth
- 手机互联映射 → Phone Projection
- 车联网 → Connected Car
- 4G/5G网络 → 4G/5G Network
- OTA升级 → OTA Update
- 面部识别 → Face Recognition
- 指纹识别 → Fingerprint Scanner
- 声纹识别 → Voice Print
- 情绪识别 → Emotion Recognition
- 语音识别控制系统 → Voice Control
- 语音免唤醒功能 → Voice Command Without Wake Word
- 语音分区域唤醒识别功能 → Zone Voice Recognition
- 连续性语音识别 → Continuous Voice Recognition
- 可见即可说 → Visible, Speakable
- 语音助手唤醒词 → Voice Assistant Wake Word
- 手势控制功能 → Gesture Control
- Wi-Fi热点 → Wi-Fi Hotspot
- 多指飞屏操控 → Multi-touch Control
- 应用商店 → App Store
- 多媒体接口 → Media Interface
- USB/Type-C接口数量 → USB/Type-C Ports
- USB/Type-C最大充电功率 → USB/Type-C Max Charging Power
- 车载电视 → Rear Entertainment
- 后排液晶屏 → Rear Display
- 模拟声浪 → Active Exhaust Sound
- K歌功能 → Karaoke
- 音响品牌 → Audio Brand
- 扬声器数量 → Speakers
- 后排多媒体控制 → Rear Media Control
- 近光灯 → Low Beam
- 远光灯 → High Beam
- 日间行车灯 → DRL
- 自适应远近光 → Adaptive Headlights
- 自动大灯 → Auto Headlights
- 转向辅助灯 → Cornering Lights
- 前雾灯 → Front Fog Lights
- 大灯随动转向 → AFS
- 大灯高度调节 → Headlight Adjustment
- 大灯清洗功能 → Headlight Washers
- 车内氛围灯 → Ambient Light
- 主动式环境氛围灯 → Active Ambient Light
- 灯光特色功能 → Lighting Features
- 灯光投影技术 → Projection Lights
- 大灯延时关闭 → Headlight Delay Off
- 前大灯雨雾模式 → Rain/Fog Headlight Mode
- 电动车窗 → Power Windows
- 车窗一键升降 → One-touch Windows
- 车窗防夹手功能 → Anti-pinch Windows
- 外后视镜功能 → Exterior Mirror Functions
- 内后视镜功能 → Interior Mirror Functions
- 车内化妆镜 → Vanity Mirror
- 后排隐私玻璃 → Rear Privacy Glass
- 车内遮阳帘 → Sunshades
- 雨量感应式雨刷 → Rain-sensing Wipers
- 后雨刷 → Rear Wiper
- 后窗玻璃开启 → Rear Window Open
- 多层隔音玻璃 → Acoustic Glass
- 前风挡电加热 → Heated Windshield
- 可加热喷水嘴 → Heated Washer Nozzles
- 空调控制方式 → Climate Control Type
- 后排出风口 → Rear Air Vents
- 温度分区控制 → Zone Climate Control
- 车载冰箱 → Car Refrigerator
- 香氛系统 → Fragrance System
- 空气净化器 → Air Purifier
- 车载空气净化器 → Car Air Purifier
- 车内PM2.5过滤装置 → PM2.5 Filter
- 辅助驾驶芯片 → ADAS Chip
- 辅助驾驶芯片算力 → ADAS Computing Power
- 摄像头数量 → Number of Cameras
- 毫米波雷达数量 → Number of Millimeter-wave Radar
- 超声波雷达数量 → Number of Ultrasonic Sensors
- 激光雷达数量 → LiDAR
- 高精地图 → HD Map
- 选装包 → Optional Packages

### Technical Terms (Summary)
- MacPherson Independent (麦弗逊独立悬挂)
- Multi-link Independent (多连杆独立悬挂)
- Torsion Beam (扭力梁)
- Double Wishbone (双叉臂)
- Wet DCT (湿式双离合)
- Direct Injection (缸内直喷)
- On-demand 4WD (适时四驱)
- Tire Pressure Display (胎压显示)
- Unibody (承载式)
- Body-on-frame (非承载式)

## Output File Naming

### Chinese Version
`{车型名}_Specifications_CN.csv`

Example: `JETOUR_Traveler_2025_2.0TD_XWD_Crossing_Specifications_CN.csv`

### English Version
`{车型名}_Specifications_EN.csv`

Example: `JETOUR_Traveler_2025_2.0TD_XWD_Crossing_Specifications_EN.csv`

## Workflow

### Step 1: Fetch Data

Use `web_fetch` to get the specification page:
```
web_fetch(url="https://www.dongchedi.com/auto/params-carIds-{carId}")
```

### Step 2: Parse Data

Extract all specifications maintaining original:
- Parameter names (do not modify)
- Parameter order (do not reorder)
- All categories (do not skip)

### Step 3: Generate Chinese CSV

1. Create specs list with all parameters
2. Insert category headers with empty Column B
3. Replace "未提供" with "-"
4. Save as UTF-8-BOM CSV to Windows desktop: `/mnt/c/Users/Administrator/Desktop/`

### Step 4: Generate English CSV

1. Use Chinese CSV as base
2. Translate category names
3. Translate specification values
4. Save as UTF-8-BOM CSV to Windows desktop

### Step 5: Verify

#### Check Critical Parameters
- Engine (发动机)
- Max Power (最大功率)
- Max Torque (最大扭矩)
- Price (官方指导价)
- Transmission (变速箱)
- Dimensions (车身尺寸)

#### Verify English CSV Translation - CRITICAL

After generating the English CSV, ALWAYS verify that NO Chinese characters remain:

```python
import csv

def verify_no_chinese(csv_path):
    chinese_found = []
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            for j, cell in enumerate(row):
                if any('\u4e00' <= c <= '\u9fff' for c in cell):
                    chinese_found.append(f"Line {i+1}, Col {j+1}: {cell}")
    
    if chinese_found:
        print(f"❌ Found {len(chinese_found)} cells with Chinese!")
        for item in chinese_found[:20]:
            print(f"  {item}")
        return False
    else:
        print("✅ SUCCESS! No Chinese characters in English CSV!")
        return True

# Run verification
verify_no_chinese("/mnt/c/Users/Administrator/Desktop/{车型名}_Specifications_EN.csv")
```

**The English CSV is NOT complete until NO Chinese characters remain.**

If Chinese is found, add the missing translations to the translation table and regenerate.

## File Lock Handling

If the output CSV is locked (open in Excel):

```python
# Save to temp file first
temp_path = "/tmp/car_specs.csv"
# ... save to temp_path ...
# Then move to final destination
exec("mv /tmp/car_specs.csv /mnt/c/Users/Administrator/Desktop/final.csv")
```

Or use alternative filename:
`{车型名}_Specifications_new.csv`

## Example Output Structure

```csv
Parameter Name,Specification
基本信息,
官方指导价,¥169,900
厂商,奇瑞汽车
级别,紧凑型SUV
...
车身,
长(mm),4785
宽(mm),2006
...
发动机,
发动机型号,SQRF4J20
排量(mL),1998
...
```

## Key Parameters to Verify

Always verify these critical parameters match the source:

| Parameter | Example Value | Importance |
|-----------|--------------|------------|
| 官方指导价 | ¥169,900 | Pricing |
| 发动机 | 2.0T 254马力 L4 | Powertrain |
| 最大功率 | 187(254Ps) | Performance |
| 最大扭矩 | 390 Nm | Performance |
| 变速箱 | 7挡双离合 | Powertrain |
| 长x宽x高 | 4785x2006x1880 mm | Dimensions |
| 轴距 | 2800 mm | Dimensions |
| 综合油耗 | 8.83 L/100km | Efficiency |
| 保修 | 4年或10万公里 | Warranty |

## Common Mistakes to Avoid

### ❌ Leaving Chinese in English CSV
- **Wrong**: English CSV still has "●前排", "涡轮增压", "门" etc.
- **Right**: ALL Chinese must be translated - use the complete translation table

### ❌ De-duplicating Parameters
- **Wrong**: Removing duplicate `最大功率(kW)` entries
- **Right**: Keep all occurrences as they appear

### ❌ Reordering Parameters
- **Wrong**: Sorting alphabetically or grouping logically
- **Right**: Maintain web page order exactly

### ❌ Modifying Parameter Names
- **Wrong**: Changing "官方百公里加速时间(s)" to "0-100km/h加速"
- **Right**: Keep original name exactly

### ❌ Using Symbols in Categories
- **Wrong**: `=== 基本信息 ===`
- **Right**: `基本信息,`

### ❌ Wrong Encoding
- **Wrong**: UTF-8 (no BOM)
- **Right**: UTF-8-BOM

## Tips for Different Car Websites

### Dongchedi (懂车帝)
- Clean HTML structure
- All specs in one page
- Easy to extract with web_fetch

### Autohome (汽车之家)
- May require multiple requests
- Specs often spread across tabs
- Check for JavaScript-loaded content

### General
- Always verify the extracted count (typically 300-350 parameters)
- Compare with website's total parameter count
- If missing data, check for collapsed/hidden sections

## Troubleshooting

### CSV Displays Gibberish in Excel
- **Cause**: UTF-8 without BOM
- **Fix**: Use UTF-8-BOM encoding

### File Won't Save
- **Cause**: File locked by Excel
- **Fix**: Close Excel or save to temp file then move

### Missing Parameters
- **Cause**: Truncation from web_fetch
- **Fix**: Use `web_fetch` with higher `maxChars` limit

### Wrong Order
- **Cause**: Parsing or sorting during extraction
- **Fix**: Extract exactly as ordered in source HTML

## Validation

After generation, verify:

### Chinese Version
1. **Line count**: Should be ~330 lines (header + categories + parameters)
2. **Parameter count**: Should be 300-350 parameters
3. **Critical specs**: Engine, power, torque match source
4. **Encoding**: Opens correctly in Excel with Chinese
5. **Categories**: 18-19 category headers
6. **Empty values**: All show "-" not "未提供"

### English Version - CRITICAL
1. **NO Chinese characters**: Use Python script to verify
2. **All parameters translated**: Parameter names in English
3. **All values translated**: Specification values in English
4. **Categories translated**: 18 category headers in English
5. **Encoding**: UTF-8-BOM for Excel compatibility

```python
# English CSV verification script
import csv

def verify_english_csv(csv_path):
    """Verify English CSV has NO Chinese characters"""
    issues = []
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader, 1):
            for j, cell in enumerate(row, 1):
                if any('\u4e00' <= c <= '\u9fff' for c in cell):
                    issues.append(f"Row {i}, Col {j}: {cell[:50]}")
    
    if issues:
        print(f"❌ {len(issues)} cells still contain Chinese:")
        for issue in issues[:30]:
            print(f"  {issue}")
        return False
    print("✅ English CSV clean - no Chinese characters!")
    return True

# Use:
verify_english_csv("/path/to/{车型名}_Specifications_EN.csv")
```
