# 检测设备采数APP

## 项目简介

这是一个用于生产线设备检测数据采集的移动端应用，支持离线数据采集和在线数据上传。

## 主要功能

1. **二维码扫描** - 扫描设备二维码，自动识别设备信息
2. **拍照识别** - 拍摄仪器读数，OCR通过多种方法识别测量数值
3. **数据录入** - 手动修正识别的数值，添加备注信息
4. **本地存储** - 离线存储检测数据到SQLite数据库
5. **数据上传** - 检测网络连接，上传数据到SQL Server或MySQL数据库
6. **历史数据** - 查看、筛选、删除本地数据
7. **设置管理** - 配置数据库连接信息

## 技术栈

- **开发语言**: Python
- **UI框架**: Kivy 2.3.0
- **数据库**: SQLite (本地), SQL Server/MySQL (服务器)
- **OCR识别**: pytesseract (支持多种方法)
- **图像处理**: OpenCV, Pillow
- **二维码识别**: OpenCV QRCodeDetector

## 项目结构

```
检测设备采数APP/
├── main.py                 # 应用入口
├── requirements.txt        # 依赖库
├── ui/                     # 界面模块
│   ├── main_screen.py      # 主界面
│   ├── scan_screen.py      # 扫描界面
│   ├── data_entry_screen.py # 数据录入界面
│   ├── upload_screen.py    # 上传界面
│   ├── history_screen.py   # 历史数据界面
│   └── settings_screen.py  # 设置界面
├── services/               # 业务逻辑
│   ├── database_service.py # 本地数据库服务
│   ├── qr_scanner.py      # 二维码扫描服务
│   ├── ocr_service.py     # OCR识别服务
│   ├── network_service.py  # 网络检测服务
│   └── upload_service.py   # 数据上传服务
├── models/                 # 数据模型
│   ├── inspection_data.py  # 检测数据模型
│   └── device_info.py      # 设备信息模型
├── utils/                  # 工具类
│   ├── image_utils.py      # 图片处理工具
│   └── date_utils.py       # 日期时间工具
├── config/                 # 配置文件
│   └── app_config.py       # 应用配置
└── data/                   # 数据目录
    ├── app.db              # SQLite数据库
    ├── config.json         # 配置文件
    └── images/             # 存储拍摄图片
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行应用

```bash
python main.py
```

## 二维码格式

设备二维码应包含以下JSON格式的信息：

```json
{
    "device_id": "设备ID",
    "device_name": "设备名称",
    "production_line": "生产线",
    "inspection_type": "检测类型",
    "unit": "单位"
}
```

## 数据库配置

### SQL Server

- 主机: zjzx.cpicfiber.com
- 端口: 1433
- 数据库: CPIC_QMI
- 用户名: sa
- 密码: Cpic1234$

### MySQL

- 主机: 10.12.0.130
- 端口: 9030
- 数据库: cpic_doris
- 用户名: root
- 密码: root

### 管理员账户

- 用户名: CPIC
- 密码: CPIC

## 使用流程

1. 打开应用，进入主界面
2. 点击"扫描二维码"，扫描设备二维码
3. 拍照识别仪器读数数值
4. 确认或修正识别的数值
5. 保存数据到本地
6. 连接到公司内网后，点击"上传数据"
7. 查看上传结果

## 注意事项

1. 首次使用需要安装Tesseract OCR引擎
2. 确保设备有相机权限
3. 网络上传需要连接到公司内网
4. 数据上传前会自动检测网络连接
5. 支持离线使用，数据暂存本地

## 开发者

- 项目名称: 检测设备采数APP
- 开发语言: Python
- UI框架: Kivy
