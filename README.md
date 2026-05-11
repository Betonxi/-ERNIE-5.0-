# 视频脚本解析系统：基于ERNIE 5.0的智能视频内容识别与脚本提取

## 一、项目简介

本项目基于百度文心ERNIE 5.0大模型，开发了一个智能视频脚本解析系统。系统能够自动分析视频内容并生成结构化的视频脚本，为视频创作者、内容分析师和媒体工作者提供高效的视频内容处理工具。

**项目亮点：**

 集成ERNIE 5.0原生全模态大模型，实现智能视频内容理解
 
 支持多种视频格式，自动生成结构化脚本
 
 纯Python后端实现，简洁高效
 
 开源可扩展，便于二次开发
 
 支持本地视频文件和抖音视频链接处理

### ERNIE 5.0技术优势

参考文心5.0的技术特性，本项目充分利用了ERNIE 5.0的以下优势：

#### 原生全模态能力

ERNIE 5.0具备真正的原生全模态能力，能够同时处理图片、音频、视频等多种媒体格式。相比其他模型的"插件式多模态"，ERNIE 5.0在视频内容理解方面展现出更强的协同能力。

#### 开发效率提升

根据实际测试，使用ERNIE 5.0进行开发相比传统开发路径，效率提升可达833%。本项目正是基于这一优势，快速实现了视频脚本解析的核心功能。

### 中文场景优化

ERNIE 5.0对中文技术文档和本土化业务场景的理解明显优于国际模型，特别适合处理中文视频内容的脚本提取任务。

## 二、项目背景

随着短视频和在线视频内容的爆炸式增长，视频内容分析和脚本提取成为内容创作、版权保护和内容推荐的重要环节。传统的人工视频分析耗时耗力，而现有的AI工具往往功能单一或价格昂贵。本项目旨在开发一个开源、易用的视频脚本解析系统，降低视频内容分析的门槛。

**解决痛点：**

 1.视频内容分析效率低下
 
 2.脚本提取过程繁琐
 
 3.缺乏结构化的视频内容描述
 
 4.中小创作者难以获得专业分析工具

## 三、项目方案

### 系统架构

![](https://ai-studio-static-online.cdn.bcebos.com/4e5579c4e0a4431ab6c796dc9f7c16e3db616935c98a4be49f0479e8f76d83e4)


### 技术栈

 **核心语言：** Python 3.8+
 
 **AI模型：** ERNIE 5.0大模型（通过OpenAI兼容接口）
 
 **文件处理：** 视频编码、base64转换
 
 **数据存储：** JSON和TXT格式结果保存
 
 **网络请求：** requests库处理抖音链接解析

### 核心功能模块

1. **视频管理模块**
    * 视频文件读取和验证
    * 自动重命名和存储
    * 文件大小和格式检查
    * 抖音视频链接解析和下载

2. **内容识别模块**
    * 视频编码处理
    * ERNIE 5.0 API调用
    * 流式响应处理

3. **脚本提取模块**
    * 结构化脚本生成
    * 多维度内容分析
    * 结果格式化输出

4. **结果管理模块**
    * 脚本文件保存
    * 历史记录管理
    * 多格式导出

## 四、数据说明

### 输入数据

* **视频文件格式：** MP4、AVI、MOV等常见格式
* **文件大小限制：** 最大100MB（可配置）
* **视频时长：** 支持各种时长视频
* **内容类型：** 教学视频、vlog、宣传片、纪录片等
* **抖音链接：** 支持抖音分享链接解析和无水印视频下载

### 输出数据

* **脚本格式：** JSON和TXT双格式

* **内容结构：**

  ```json
  {
    "video_info": {
      "title": "视频标题",
      "type": "视频类型",
      "estimated_duration": "时长估计"
    },
    "scenes": [
      {
        "scene_description": "画面描述",
        "dialogue": "文案/台词",
        "audio_effects": "音乐/音效"
      }
    ],
    "core_themes": {
      "key_points": ["核心信息点"],
      "emotional_tone": "情感基调",
      "target_audience": "目标受众"
    }
  }
  ```

### 数据样例

项目包含示例视频文件 `example.mp4` 用于测试，处理后的脚本文件保存在 `scripts/` 目录中。

## 五、代码实现

### 核心类设计

```python
class IntegratedVideoAnalyzer:
    """整合视频分析器"""
    
    def __init__(self, api_key=None, base_url=None):
        """初始化解析器"""
        
    def save_uploaded_video(self, source_path):
        """保存上传的视频文件"""
        
    def encode_video_to_base64(self, video_path):
        """视频文件base64编码"""
        
    def extract_video_script(self, video_path, save_result=True):
        """提取视频脚本"""
        
    def save_script_result(self, video_path, script_content):
        """保存脚本结果"""
        
    # 抖音相关功能
    def extract_url_from_text(self, text):
        """从分享文本中提取抖音链接"""
        
    def get_douyin_video_url(self, share_url):
        """获取抖音无水印视频链接"""
        
    def download_douyin_video(self, video_url, filename=None):
        """下载抖音视频到本地"""
```

### 主要代码片段

#### 视频文件管理

```python
def save_uploaded_video(self, source_path):
    """保存视频文件"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.basename(source_path)
    name, ext = os.path.splitext(filename)
    new_filename = f"{name}_{timestamp}{ext}"
    
    save_path = os.path.join(self.uploads_dir, new_filename)
    shutil.copy2(source_path, save_path)
    return save_path
```

#### ERNIE 5.0 API调用

```python
def extract_video_script(self, video_path, save_result=True):
    """提取视频脚本"""
    video_base64 = self.encode_video_to_base64(video_path)
    video_data_url = f"data:video/mp4;base64,{video_base64}"
    
    # 使用ERNIE 5.0的OpenAI兼容接口
    chat_completion = self.client.chat.completions.create(
        model="ernie-5.0-thinking-preview",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "video_url", "video_url": {"url": video_data_url}}
            ]
        }],
        stream=True,
        max_tokens=8192
    )
```

#### 抖音视频处理

```python
def get_douyin_video_url(self, share_url):
    """获取抖音无水印视频链接"""
    try:
        # 导入douyin.py中的函数
        import sys
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from douyin import get_video_url
        return get_video_url(share_url)
    except ImportError:
        # 如果导入失败，则使用内置实现
        return self._get_douyin_video_url_internal(share_url)
```

### 运行说明

* **环境要求：**

    * Python 3.8+
    * 安装依赖：`pip install openai requests`
    * ERNIE 5.0 API密钥（通过AI Studio获取）

* **配置说明：**

    * 在`IntegratedVideoAnalyzer`类初始化时传入API密钥和基础URL
    * 或者修改`integrated_video_analyzer.py`文件中的默认配置

## 六、快捷使用方式

### 1. 命令行快速使用

项目提供了交互式命令行界面，可以通过以下命令启动：

```bash
python ytong.py
```

启动后将显示交互菜单：

```
============================================================
欢迎使用整合视频分析系统
支持本地视频文件和抖音视频链接的脚本解析
============================================================

请选择视频来源:
1. 本地视频文件
2. 抖音视频链接
3. 退出程序

请输入选项 (1/2/3): 
```
![](https://ai-studio-static-online.cdn.bcebos.com/c9b7f0c39df84fdebe5aa63831be4f51482ebf1434394bfcb6363a43aff35353)
![](https://ai-studio-static-online.cdn.bcebos.com/2e72bbd865904cc9ad95df6f99bc709f22868121953648f08ced1f54fd45b2d3)


### 2. Python代码直接调用

#### 处理本地视频文件

```python
from integrated_video_analyzer import IntegratedVideoAnalyzer

# 创建分析器实例
analyzer = IntegratedVideoAnalyzer()

# 保存并处理视频
saved_video_path = analyzer.save_uploaded_video("path/to/your/video.mp4")
script_result = analyzer.extract_video_script(saved_video_path)
print(script_result)
```

#### 处理抖音视频链接

```python
from integrated_video_analyzer import IntegratedVideoAnalyzer

# 创建分析器实例
analyzer = IntegratedVideoAnalyzer()

# 抖音分享链接
share_url = "https://v.douyin.com/xxxxxx/"

# 获取无水印视频链接
video_url = analyzer.get_douyin_video_url(share_url)
print(f"无水印视频链接: {video_url}")

# 下载视频
saved_video_path = analyzer.download_douyin_video(video_url)

# 提取脚本
script_result = analyzer.extract_video_script(saved_video_path)
print(script_result)
```

### 3. API密钥配置

### 在文件ytong.py中修改配置
### 点击 （[模型广场](https://aistudio.baidu.com/playground)）

![](https://ai-studio-static-online.cdn.bcebos.com/5724f66da2a64a15bd02cfd77959db87fde6eb8e4b874354973e29b8592a7401)

#### 复制自己对应的api_key和base_url 在ytong.py中修改

### 4. 批量处理脚本示例

```python
import os
from integrated_video_analyzer import IntegratedVideoAnalyzer

# 创建分析器实例
analyzer = IntegratedVideoAnalyzer()

# 视频文件目录
video_dir = "./videos/"

# 遍历目录中的所有视频文件
for filename in os.listdir(video_dir):
    if filename.endswith((".mp4", ".avi", ".mov")):
        video_path = os.path.join(video_dir, filename)
        print(f"正在处理视频: {video_path}")
        
        try:
            # 保存并处理视频
            saved_video_path = analyzer.save_uploaded_video(video_path)
            script_result = analyzer.extract_video_script(saved_video_path)
            print(f"视频 {filename} 处理完成")
        except Exception as e:
            print(f"处理视频 {filename} 时出错: {e}")
```

## 七、效果展示

### 功能演示

1. **视频文件处理**
    * 本地视频文件读取和验证
    * 自动文件重命名和存储
    * 文件大小和格式检查
    * 抖音视频链接解析和下载

2. **脚本提取过程**
    * 实时控制台进度显示
    * 流式输出脚本内容
    * 处理状态监控

3. **结果展示**
    * 结构化脚本预览
    * JSON和TXT双格式导出
    * 历史记录管理

### 处理效果对比

**输入视频：** 3分钟教学视频
**处理时间：** 约2-3分钟
**输出质量：** 详细的结构化脚本，包含场景描述、对话内容、情感分析等

### 示例输出

![](https://ai-studio-static-online.cdn.bcebos.com/20ca2207478c4a3fbe66651e157499cd6f61eb0a9af3476c96070b43b7335fd4)


## 八、总结提高

### 项目成果

1. **技术创新：**
    * 成功集成ERNIE Bot 5.0大模型
    * 实现视频内容的智能理解和结构化提取
    * 开发完整的端到端解决方案
    * 支持抖音视频链接解析和处理

2. **实用价值：**
    * 为视频创作者提供高效工具
    * 降低视频内容分析成本
    * 提升内容创作效率
    * 支持多种视频来源

3. **开源贡献：**
    * 提供完整的开源代码
    * 详细的文档说明
    * 便于社区二次开发
    * 多种使用方式支持

### 后续计划

1. **功能扩展：**
    * 支持更多视频平台（快手、小红书等）
    * 增加批量处理功能
    * 开发Web界面
    * 支持更多输出格式（如SRT字幕文件）

2. **性能优化：**
    * 提升处理速度
    * 优化内存使用
    * 增加缓存机制
    * 支持断点续传

3. **应用场景拓展：**
    * 教育领域的视频内容分析
    * 媒体行业的自动化脚本生成
    * 内容审核和版权保护
    * 视频内容翻译和本地化

### 技术挑战与解决方案

**挑战1：大文件处理**

* 问题：大视频文件导致API调用失败
* 解决方案：实施文件大小限制和分块处理

**挑战2：API响应稳定性**

* 问题：流式响应可能中断
* 解决方案：增加重试机制和错误处理

**挑战3：结果格式化**

* 问题：AI输出格式不一致
* 解决方案：设计结构化提示词模板

**挑战4：抖音链接解析**

* 问题：抖音接口变化导致解析失败
* 解决方案：提供多种解析方式和错误处理机制
