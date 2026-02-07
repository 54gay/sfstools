# sfstools
🚀 SFS Tools - 航天模拟器工具箱

https://img.shields.io/badge/Kivy-2.3.0-blue.svg
https://img.shields.io/badge/Python-3.8+-green.svg
https://img.shields.io/badge/Platform-Android-brightgreen.svg
https://img.shields.io/badge/License-MIT-yellow.svg

一个专为《航天模拟器》(Space Flight Simulator) 设计的多功能工具箱应用，提供蓝图生成、字体设计、图像转换等强大功能，帮助玩家更高效地构建和设计航天器。

📱 应用截图

(截图位置 - 实际使用中请替换)

✨ 核心功能

🛠️ 五大工具模块

模块 图标 功能描述
环生成器 🌀 自动生成环形结构蓝图，支持自定义参数
方向调整 🔄 3D旋转、翻转、缩放蓝图
部件对齐 📐 精确计算部件相对位置
字体生成器 🔤 将文字转换为SFS蓝图
图像转换器 🖼️ 图片转蓝图，支持单色/自动识别

🎯 特色功能

· ✅ 离线工作 - 无需网络连接
· ✅ 自动保存 - 所有蓝图本地存储
· ✅ 中文本地化 - 全中文界面，操作友好
· ✅ 多级目录 - 按类型自动整理文件
· ✅ 智能验证 - 输入实时检查和提示

📂 文件结构

```
📁 SFS Tools/
├── 📁 Blueprints Folder/     # 蓝图存储
├── 📁 Fonts/                # 字体文件
├── 📁 Images/               # 图片素材
└── 📁 应用缓存/
```

🔧 技术架构

开发框架

· GUI框架: Kivy 2.x (跨平台移动应用)
· 语言: Python 3.8+
· 打包: Buildozer (Android APK)
· 图像处理: Pillow (PIL)

核心依赖

```python
kivy >= 2.3.0
Pillow >= 10.0.0
math, json, os (Python标准库)
```

权限要求

```xml
<!-- Android权限 -->
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>
```

🚀 快速开始

安装APK

1. 从 Releases 下载最新APK
2. 允许安装未知来源应用
3. 安装并运行

首次使用

1. 启动应用后自动创建目录结构
2. 授予存储权限
3. 开始使用任意工具模块

📖 使用指南

1. 环生成器使用

```markdown
步骤：
1. 输入X/Y坐标
2. 设置分段宽度和角度
3. 选择部件类型（燃料箱、整流罩等）
4. 选择颜色纹理
5. 点击"生成"按钮
```

2. 图像转蓝图

```markdown
支持格式：PNG, JPG, JPEG
工作模式：
- 单色模式：指定单一颜色
- 自动模式：智能识别6种SFS颜色
输出：自动排列的部件蓝图
```

3. 字体生成器

```markdown
前提：需要先导入字体文件包
功能：
- 支持自定义文字
- 自动调整字间距
- 指定生成位置
- 批量生成文字蓝图
```

💾 文件管理

支持的导入格式

· 蓝图: .txt (SFS蓝图格式)
· 字体: 专用字体包文件夹
· 图片: .png, .jpg, .jpeg

自动命名规则

```
当名称重复时自动添加序号：
原名称：我的飞船
重复时：我的飞船 1
再次重复：我的飞船 2
...
```

🎨 界面设计

主题风格

· 航天器工业风格配色
· 大按钮设计，便于触摸操作
· 清晰的视觉反馈
· 直观的图标指示

交互特性

· 按钮状态实时反馈
· 输入验证即时提示
· 滑动条数值联动
· 开关按钮直观切换

🔄 更新日志

v1.0.0 (当前版本)

· ✅ 五大核心工具模块
· ✅ 中文本地化界面
· ✅ 文件系统自动管理
· ✅ 基础错误处理
· ✅ Android平台适配

计划功能

· 云同步功能
· 更多预制模板
· 3D预览功能
· 社区分享平台

🛠️ 开发者信息

构建说明

```bash
# 环境要求
Python 3.8+
Buildozer
Android SDK/NDK

# 构建APK
buildozer android debug
```

项目结构

```python
sfstools/
├── main.py              # 主程序入口
├── buildozer.spec      # 打包配置
├── assets/             # 资源文件
│   ├── icon.png       # 应用图标
│   ├── *.kv           # 界面布局文件
│   └── button_*.png   # 按钮素材
└── requirements.txt    # 依赖列表
```

❓ 常见问题

Q1: 为什么需要存储权限？

A: 应用需要在设备上创建和保存蓝图文件、字体包和图片素材。

Q2: 支持哪些Android版本？

A: Android 5.0 (API 21) 及以上版本。

Q3: 能与其他SFS工具兼容吗？

A: 生成的蓝图文件是标准SFS格式，与其他工具完全兼容。

Q4: 如何处理大图片？

A: 建议使用分辨率适中的图片，过大的图片可能导致处理时间较长。

Q5: 字体包如何获取？

A: 可从SFS社区获取字体包，或使用工具自行创建。

📞 支持与反馈

问题报告

1. 检查常见问题
2. 在 Issues 页面提交问题
3. 提供详细的操作步骤和设备信息

功能建议

欢迎在GitHub Discussions中提出新功能建议！

🤝 贡献指南

欢迎提交Pull Request改进项目：

1. Fork 本仓库
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 新建Pull Request

📄 许可证

本项目采用 MIT 许可证 - 查看 LICENSE 文件了解详情。

🙏 致谢

· Kivy团队 - 优秀的跨平台框架
· Space Flight Simulator社区 - 灵感来源
· 所有测试用户 - 宝贵的反馈意见

---

<div align="center">

🚀 探索无限可能，构建你的太空梦想！

下载APK · 报告问题 · 功能建议

</div>

🔗 相关链接

· Space Flight Simulator官网
· Kivy官方文档
· SFS蓝图格式说明

📊 版本兼容性

应用版本 SFS游戏版本 Android版本 Python版本
v1.0.0 1.5.2.5+ 5.0+ (API 21) 3.8+

⚡ 性能优化提示

1. 图片处理：使用适当分辨率的图片
2. 蓝图规模：建议一次生成不超过500个部件
3. 存储空间：定期清理不需要的蓝图文件
4. 电池优化：长时间处理时连接电源

🌐 多语言支持

当前支持：简体中文
计划支持：English, Español, Русский, 日本語

---

📢 注意：本工具为第三方辅助应用，与《航天模拟器》官方无直接关联。
