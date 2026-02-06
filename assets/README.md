# Assets 目录说明

本目录用于存放应用打包所需的资源文件。

## 所需文件

### 1. Android 图标 (icon.png)
- **用途**：Android 应用图标
- **尺寸**：512x512 像素
- **格式**：PNG（推荐透明背景）
- **位置**：`assets/icon.png`

### 2. Windows 图标 (icon.ico)
- **用途**：Windows 可执行文件图标
- **尺寸**：256x256 像素
- **格式**：ICO
- **位置**：`assets/icon.ico`
- **转换工具**：https://icoconvert.com/

### 3. Android 启动画面 (presplash.png)
- **用途**：Android 应用启动时的欢迎画面
- **尺寸**：1024x1024 像素
- **格式**：PNG
- **位置**：`assets/presplash.png`

## 如何准备图标

### 从 PNG 转换为 ICO
1. 访问 https://icoconvert.com/
2. 上传 PNG 512x512 图标
3. 选择 ICO 格式
4. 下载并保存为 `assets/icon.ico`

### 设计建议
- 使用简洁的设计
- 确保在小尺寸下仍然清晰
- 使用品牌色
- 避免过多细节

## 注意事项

- 图标文件是可选的，但强烈建议提供
- 如果缺少图标，将使用默认图标
- 确保文件名和大小写正确
- 测试打包后的应用图标是否正常显示
