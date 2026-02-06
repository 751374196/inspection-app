# SQL Server 数据库配置说明

## 数据库信息
- **服务器**: zjzx.cpicfiber.com
- **数据库**: CPIC_QMI
- **用户名**: sa
- **密码**: Cpic1234$

## 表结构
- **表名**: inspection_records
- **用途**: 存储检测设备采数记录

## 建表步骤

### 1. 连接到SQL Server
使用SQL Server Management Studio (SSMS)或其他数据库管理工具连接到服务器。

### 2. 执行建表脚本
打开 `create_tables.sql` 文件，在SQL Server中执行该脚本。

### 3. 验证表是否创建成功
执行以下SQL查询：
```sql
USE CPIC_QMI;
SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'inspection_records';
```

## 表结构说明

| 列名 | 数据类型 | 说明 | 是否必填 |
|------|----------|------|----------|
| id | INT | 主键ID，自增 | 是 |
| GUID_MAIN | UNIQUEIDENTIFIER | 全局唯一标识符 | 否 |
| device_id | NVARCHAR(100) | 设备ID | 是 |
| device_name | NVARCHAR(200) | 设备名称 | 是 |
| production_line | NVARCHAR(100) | 生产线 | 是 |
| inspection_type | NVARCHAR(100) | 检测类型 | 是 |
| unit | NVARCHAR(50) | 单位 | 是 |
| measured_value | DECIMAL(18,6) | 测量数值 | 是 |
| remark | NVARCHAR(500) | 备注 | 否 |
| capture_time | DATETIME | 采集时间 | 是 |
| upload_time | DATETIME | 上传时间 | 是 |
| IsDelete | BIT | 逻辑删除标记(0-未删除,1-已删除) | 否 |
| START_MEMBER_ID | NVARCHAR(50) | 获取数据的用户ID | 否 |
| START_DATE | DATETIME | 获取数据的时间 | 否 |
| MODIFY_MEMBER_ID | NVARCHAR(50) | 修改数据的用户ID | 否 |
| MODIFY_DATE | DATETIME | 修改时间 | 否 |
| MODIFY_LOGS | NVARCHAR(MAX) | 修改日志 | 否 |
| created_at | DATETIME | 记录创建时间 | 是（默认值） |

## 索引说明
为了提高查询性能，已创建以下索引：
- idx_device_id: 设备ID索引
- idx_production_line: 生产线索引
- idx_capture_time: 采集时间索引
- idx_upload_time: 上传时间索引

## 应用配置
在应用程序的设置界面中配置以下信息：
- 主机地址: zjzx.cpicfiber.com
- 数据库名: CPIC_QMI
- 用户名: sa
- 密码: Cpic1234$

## 上传说明
应用程序现在只上传数据到SQL Server数据库，不再上传到MySQL数据库。

每次上传时会记录：
- 设备信息（ID、名称、生产线、检测类型、单位）
- 测量数值
- 备注（如果有）
- 采集时间
- 上传时间
- 全局唯一标识符（GUID_MAIN）
- 获取数据的用户ID（START_MEMBER_ID）
- 获取数据的时间（START_DATE）

## 测试连接
在应用程序的设置界面中点击"测试连接"按钮，可以测试SQL Server连接是否正常。
