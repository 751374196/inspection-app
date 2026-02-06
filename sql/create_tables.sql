-- SQL Server 建表语句
-- 数据库: CPIC_QMI
-- 表名: inspection_records

USE CPIC_QMI;
GO

-- 检查表是否存在，如果存在则删除
IF OBJECT_ID('dbo.inspection_records', 'U') IS NOT NULL
    DROP TABLE dbo.inspection_records;
GO

-- 创建检测记录表
CREATE TABLE dbo.inspection_records (
    id INT IDENTITY(1,1) PRIMARY KEY,
    GUID_MAIN UNIQUEIDENTIFIER NULL,
    device_id NVARCHAR(100) NOT NULL,
    device_name NVARCHAR(200) NOT NULL,
    production_line NVARCHAR(100) NOT NULL,
    inspection_type NVARCHAR(100) NOT NULL,
    unit NVARCHAR(50) NOT NULL,
    measured_value DECIMAL(18, 6) NOT NULL,
    remark NVARCHAR(500) NULL,
    capture_time DATETIME NOT NULL,
    upload_time DATETIME NOT NULL,
    IsDelete BIT NULL DEFAULT 0,
    START_MEMBER_ID NVARCHAR(50) NULL,
    START_DATE DATETIME NULL,
    MODIFY_MEMBER_ID NVARCHAR(50) NULL,
    MODIFY_DATE DATETIME NULL,
    MODIFY_LOGS NVARCHAR(MAX) NULL,
    created_at DATETIME DEFAULT GETDATE()
);
GO

-- 创建索引以提高查询性能
CREATE INDEX idx_device_id ON dbo.inspection_records(device_id);
CREATE INDEX idx_production_line ON dbo.inspection_records(production_line);
CREATE INDEX idx_capture_time ON dbo.inspection_records(capture_time);
CREATE INDEX idx_upload_time ON dbo.inspection_records(upload_time);
CREATE INDEX idx_GUID_MAIN ON dbo.inspection_records(GUID_MAIN);
CREATE INDEX idx_IsDelete ON dbo.inspection_records(IsDelete);
GO

-- 添加表注释
EXEC sp_addextendedproperty 
    @name=N'MS_Description', 
    @value=N'检测设备采数记录表', 
    @level0type=N'SCHEMA', @level0name=N'dbo', 
    @level1type=N'TABLE', @level1name=N'inspection_records';
GO

-- 添加列注释
EXEC sp_addextendedproperty 
    @name=N'MS_Description', @value=N'主键ID', 
    @level0type=N'SCHEMA', @level0name=N'dbo', 
    @level1type=N'TABLE', @level1name=N'inspection_records',
    @level2type=N'COLUMN', @level2name=N'id';
GO

EXEC sp_addextendedproperty 
    @name=N'MS_Description', @value=N'全局唯一标识符', 
    @level0type=N'SCHEMA', @level0name=N'dbo', 
    @level1type=N'TABLE', @level1name=N'inspection_records',
    @level2type=N'COLUMN', @level2name=N'GUID_MAIN';
GO

EXEC sp_addextendedproperty 
    @name=N'MS_Description', @value=N'设备ID', 
    @level0type=N'SCHEMA', @level0name=N'dbo', 
    @level1type=N'TABLE', @level1name=N'inspection_records',
    @level2type=N'COLUMN', @level2name=N'device_id';
GO

EXEC sp_addextendedproperty 
    @name=N'MS_Description', @value=N'设备名称', 
    @level0type=N'SCHEMA', @level0name=N'dbo', 
    @level1type=N'TABLE', @level1name=N'inspection_records',
    @level2type=N'COLUMN', @level2name=N'device_name';
GO

EXEC sp_addextendedproperty 
    @name=N'MS_Description', @value=N'生产线', 
    @level0type=N'SCHEMA', @level0name=N'dbo', 
    @level1type=N'TABLE', @level1name=N'inspection_records',
    @level2type=N'COLUMN', @level2name=N'production_line';
GO

EXEC sp_addextendedproperty 
    @name=N'MS_Description', @value=N'检测类型', 
    @level0type=N'SCHEMA', @level0name=N'dbo', 
    @level1type=N'TABLE', @level1name=N'inspection_records',
    @level2type=N'COLUMN', @level2name=N'inspection_type';
GO

EXEC sp_addextendedproperty 
    @name=N'MS_Description', @value=N'单位', 
    @level0type=N'SCHEMA', @level0name=N'dbo', 
    @level1type=N'TABLE', @level1name=N'inspection_records',
    @level2type=N'COLUMN', @level2name=N'unit';
GO

EXEC sp_addextendedproperty 
    @name=N'MS_Description', @value=N'测量数值', 
    @level0type=N'SCHEMA', @level0name=N'dbo', 
    @level1type=N'TABLE', @level1name=N'inspection_records',
    @level2type=N'COLUMN', @level2name=N'measured_value';
GO

EXEC sp_addextendedproperty 
    @name=N'MS_Description', @value=N'备注', 
    @level0type=N'SCHEMA', @level0name=N'dbo', 
    @level1type=N'TABLE', @level1name=N'inspection_records',
    @level2type=N'COLUMN', @level2name=N'remark';
GO

EXEC sp_addextendedproperty 
    @name=N'MS_Description', @value=N'采集时间', 
    @level0type=N'SCHEMA', @level0name=N'dbo', 
    @level1type=N'TABLE', @level1name=N'inspection_records',
    @level2type=N'COLUMN', @level2name=N'capture_time';
GO

EXEC sp_addextendedproperty 
    @name=N'MS_Description', @value=N'上传时间', 
    @level0type=N'SCHEMA', @level0name=N'dbo', 
    @level1type=N'TABLE', @level1name=N'inspection_records',
    @level2type=N'COLUMN', @level2name=N'upload_time';
GO

EXEC sp_addextendedproperty 
    @name=N'MS_Description', @value=N'逻辑删除标记(0-未删除,1-已删除)', 
    @level0type=N'SCHEMA', @level0name=N'dbo', 
    @level1type=N'TABLE', @level1name=N'inspection_records',
    @level2type=N'COLUMN', @level2name=N'IsDelete';
GO

EXEC sp_addextendedproperty 
    @name=N'MS_Description', @value=N'获取数据的用户ID', 
    @level0type=N'SCHEMA', @level0name=N'dbo', 
    @level1type=N'TABLE', @level1name=N'inspection_records',
    @level2type=N'COLUMN', @level2name=N'START_MEMBER_ID';
GO

EXEC sp_addextendedproperty 
    @name=N'MS_Description', @value=N'获取数据的时间', 
    @level0type=N'SCHEMA', @level0name=N'dbo', 
    @level1type=N'TABLE', @level1name=N'inspection_records',
    @level2type=N'COLUMN', @level2name=N'START_DATE';
GO

EXEC sp_addextendedproperty 
    @name=N'MS_Description', @value=N'修改数据的用户ID', 
    @level0type=N'SCHEMA', @level0name=N'dbo', 
    @level1type=N'TABLE', @level1name=N'inspection_records',
    @level2type=N'COLUMN', @level2name=N'MODIFY_MEMBER_ID';
GO

EXEC sp_addextendedproperty 
    @name=N'MS_Description', @value=N'修改时间', 
    @level0type=N'SCHEMA', @level0name=N'dbo', 
    @level1type=N'TABLE', @level1name=N'inspection_records',
    @level2type=N'COLUMN', @level2name=N'MODIFY_DATE';
GO

EXEC sp_addextendedproperty 
    @name=N'MS_Description', @value=N'修改日志', 
    @level0type=N'SCHEMA', @level0name=N'dbo', 
    @level1type=N'TABLE', @level1name=N'inspection_records',
    @level2type=N'COLUMN', @level2name=N'MODIFY_LOGS';
GO

EXEC sp_addextendedproperty 
    @name=N'MS_Description', @value=N'记录创建时间', 
    @level0type=N'SCHEMA', @level0name=N'dbo', 
    @level1type=N'TABLE', @level1name=N'inspection_records',
    @level2type=N'COLUMN', @level2name=N'created_at';
GO

PRINT '表 inspection_records 创建成功！';
GO
