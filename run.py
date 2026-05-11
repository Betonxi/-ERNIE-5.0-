# -*- coding: utf-8 -*-
"""
整合视频分析系统
功能：支持本地视频文件和抖音视频链接的脚本解析
"""

import requests
import re
import json
import os
import base64
from openai import OpenAI
from datetime import datetime
import shutil

class IntegratedVideoAnalyzer:
    """
    整合视频分析器
    支持本地视频文件和抖音视频链接的脚本解析
    """
    
    def __init__(self, api_key=None, base_url=None):
        """
        初始化整合视频分析器
        :param api_key: ERNIE Bot API密钥
        :param base_url: API基础URL
        """
        # 默认API配置
        default_api_key = "7b97b5e65d1248169aab2d56f67d2b0fbcb146a2"
        default_base_url = "https://aistudio.baidu.com/llm/lmapi/v3"
        
        self.api_key = api_key or default_api_key
        self.base_url = base_url or default_base_url
        
        # 初始化OpenAI客户端
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )
        
        # 创建必要的目录
        self.uploads_dir = "uploads"
        self.results_dir = "results"
        self.scripts_dir = "scripts"
        self.ensure_directories_exist()
    
    def ensure_directories_exist(self):
        """
        确保必要的目录存在
        """
        for directory in [self.uploads_dir, self.results_dir, self.scripts_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
    
    # 抖音相关功能
    def extract_url_from_text(self, text):
        """从分享文本中提取抖音链接"""
        # 匹配抖音链接的正则表达式
        url_pattern = r'https://v\.douyin\.com/[a-zA-Z0-9]+/?'
        match = re.search(url_pattern, text)
        if match:
            return match.group(0)
        else:
            raise ValueError("未找到有效的抖音链接")
    
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
    
    def _get_douyin_video_url_internal(self, share_url):
        """内部实现：获取抖音无水印视频链接"""
        # 如果输入的是完整分享文本，先提取URL
        if not share_url.startswith('http'):
            share_url = self.extract_url_from_text(share_url)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/121.0.2277.107 Version/17.0 Mobile/15E148 Safari/604.1'
        }
        # 发送请求获取视频页面
        response = requests.get(share_url, headers=headers)
        video_id = response.url.split("?")[0].strip("/").split("/")[-1]
        share_url = f'https://www.iesdouyin.com/share/video/{video_id}'
        response = requests.get(share_url, headers=headers)
        response.raise_for_status()
        # 使用正则表达式提取视频信息
        pattern = re.compile(
            pattern=r"window\._ROUTER_DATA\s*=\s*(.*?)</script>",
            flags=re.DOTALL
        )
        find_res = pattern.search(response.text)
        if not find_res or not find_res.group(1):
            raise ValueError("parse video json info from html fail")
        
        try:
            json_data = json.loads(find_res.group(1).strip())
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON解析失败: {e}")
        
        # 添加调试信息和错误处理
        try:
            loader_data = json_data.get("loaderData", {})
            video_page_data = loader_data.get("video_(id)/page", {})
            video_info_res = video_page_data.get("videoInfoRes", {})
            item_list = video_info_res.get("item_list", [])
            
            if not item_list:
                raise ValueError("视频信息为空，可能是视频已删除或不可访问")
            
            data = item_list[0]
            video_info = data.get("video", {})
            play_addr = video_info.get("play_addr", {})
            url_list = play_addr.get("url_list", [])
            
            if not url_list:
                raise ValueError("未找到视频播放地址")
            
            # 获取无水印视频链接
            video_url = url_list[0].replace("playwm", "play")
            return video_url
            
        except (KeyError, IndexError) as e:
            raise ValueError(f"解析视频信息失败: {e}")
    
    def download_douyin_video(self, video_url, filename=None):
        """
        下载抖音视频到本地
        :param video_url: 视频链接
        :param filename: 保存的文件名
        :return: 保存后的文件路径
        """
        try:
            print(f"正在下载抖音视频: {video_url}")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(video_url, headers=headers, stream=True)
            response.raise_for_status()
            
            # 生成文件名
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"douyin_video_{timestamp}.mp4"
            
            save_path = os.path.join(self.uploads_dir, filename)
            
            # 保存视频文件
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"抖音视频已保存到: {save_path}")
            return save_path
            
        except Exception as e:
            raise Exception(f"下载抖音视频失败: {str(e)}")
    
    # 视频处理相关功能
    def save_uploaded_video(self, source_path):
        """
        保存上传的视频文件
        :param source_path: 源文件路径
        :return: 保存后的文件路径
        """
        try:
            if not os.path.exists(source_path):
                raise FileNotFoundError(f"视频文件不存在: {source_path}")
            
            # 生成唯一文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.basename(source_path)
            name, ext = os.path.splitext(filename)
            new_filename = f"{name}_{timestamp}{ext}"
            
            # 保存文件
            save_path = os.path.join(self.uploads_dir, new_filename)
            shutil.copy2(source_path, save_path)
            
            print(f"视频文件已保存到: {save_path}")
            return save_path
            
        except Exception as e:
            print(f"保存视频文件时出错: {str(e)}")
            raise
    
    def encode_video_to_base64(self, video_path):
        """
        将视频文件编码为base64字符串
        :param video_path: 视频文件路径
        :return: base64编码的视频数据
        """
        try:
            # 检查文件是否存在
            if not os.path.exists(video_path):
                raise FileNotFoundError(f"视频文件不存在: {video_path}")
            
            # 读取视频文件并编码为base64
            with open(video_path, "rb") as video_file:
                video_data = video_file.read()
                video_base64 = base64.b64encode(video_data).decode('utf-8')
                return video_base64
        except Exception as e:
            raise Exception(f"视频文件编码失败: {str(e)}")
    
    def extract_video_script(self, video_path, save_result=True):
        """
        提取视频脚本
        :param video_path: 视频文件路径
        :param save_result: 是否保存结果
        :return: 提取的脚本内容
        """
        script_content = ""
        try:
            print(f"正在处理视频文件: {video_path}")
            
            # 检查文件大小（避免过大文件导致API调用失败）
            file_size = os.path.getsize(video_path)
            print(f"视频文件大小: {file_size / (1024*1024):.2f} MB")
            
            if file_size > 100 * 1024 * 1024:  # 100MB限制
                print("警告: 视频文件过大，可能无法正常处理")
            
            # 将视频编码为base64
            print("正在编码视频文件...")
            video_base64 = self.encode_video_to_base64(video_path)
            print("视频编码完成")
            
            # 构造data URL
            video_data_url = f"data:video/mp4;base64,{video_base64}"
            
            # 调用ERNIE Bot API进行视频内容识别和脚本提取
            print("正在调用ERNIE 5.0 API提取视频脚本...")
            
            # 使用特殊提示词引导模型生成结构化的视频脚本
            prompt = """
请详细分析这个视频的内容，并按照以下格式提取出完整的视频脚本：

【视频基本信息】
- 标题：[视频的主要标题或概括]
- 类型：[视频类型，如：vlog、教程、娱乐等]
- 时长估计：[根据内容复杂度估计的合理时长]

【分镜脚本】
按照时间顺序，为每个主要场景提供：
1. 画面描述：[详细描述画面中出现的元素、场景、动作等]
2. 文案/台词：[视频中出现的文字、旁白或对话]
3. 音乐/音效：[视频中可能使用的背景音乐或音效]

【核心主题】
- 主要信息点：[列出视频传达的3-5个核心信息]
- 情感基调：[视频的主要情感色彩]
- 目标受众：[视频的主要观看群体]

【亮点分析】
- 吸引人的元素：[视频中的亮点和吸引人的部分]
- 可能的改进点：[如果有，提供一些建设性的改进建议]

请确保脚本详细、结构化，便于用于拍摄参考。
            """
            
            chat_completion = self.client.chat.completions.create(
                model="ernie-5.0-thinking-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "video_url",
                                "video_url": {
                                    "url": video_data_url
                                }
                            }
                        ]
                    }
                ],
                stream=True,
                max_tokens=8192,  # 增加token数以获取更完整的脚本
                extra_body={
                    "web_search": {
                        "enable": True
                    }
                }
            )
            
            # 处理流式响应
            print("视频脚本提取结果:")
            print("=" * 50)
            for chunk in chat_completion:
                if not chunk.choices or len(chunk.choices) == 0:
                    continue
                if hasattr(chunk.choices[0].delta, "reasoning_content") and chunk.choices[0].delta.reasoning_content:
                    content = chunk.choices[0].delta.reasoning_content
                    print(content, end="", flush=True)
                    script_content += content
                elif hasattr(chunk.choices[0].delta, "content") and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    script_content += content
            
            # 保存结果
            if save_result:
                self.save_script_result(video_path, script_content)
                
            return script_content
            
        except Exception as e:
            error_msg = f"视频脚本提取过程中出现错误: {str(e)}"
            print(error_msg)
            return error_msg
    
    def save_script_result(self, video_path, script_content):
        """
        保存脚本提取结果
        :param video_path: 视频文件路径
        :param script_content: 提取的脚本内容
        :return: 保存的文件路径
        """
        try:
            # 生成结果文件名
            video_name = os.path.splitext(os.path.basename(video_path))[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            script_file = os.path.join(self.scripts_dir, f"{video_name}_script_{timestamp}.txt")
            
            # 保存脚本
            with open(script_file, "w", encoding="utf-8") as f:
                f.write(f"视频文件: {video_path}\n")
                f.write(f"提取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n")
                f.write(script_content)
            
            print(f"\n脚本提取结果已保存到: {script_file}")
            
            # 保存JSON格式的结果
            json_result_file = os.path.join(self.scripts_dir, f"{video_name}_script_{timestamp}.json")
            result_data = {
                "video_path": video_path,
                "extraction_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "script": script_content
            }
            with open(json_result_file, "w", encoding="utf-8") as f:
                json.dump(result_data, f, ensure_ascii=False, indent=2)
            
            print(f"JSON格式结果已保存到: {json_result_file}")
            
            return script_file
            
        except Exception as e:
            print(f"保存脚本结果时出现错误: {str(e)}")
            raise

def main():
    """
    主函数 - 用户交互界面
    """
    print("=" * 60)
    print("欢迎使用整合视频分析系统")
    print("支持本地视频文件和抖音视频链接的脚本解析")
    print("=" * 60)
    
    # 创建分析器实例
    analyzer = IntegratedVideoAnalyzer()
    
    while True:
        print("\n请选择视频来源:")
        print("1. 本地视频文件")
        print("2. 抖音视频链接")
        print("3. 退出程序")
        
        try:
            choice = input("\n请输入选项 (1/2/3): ").strip()
        except KeyboardInterrupt:
            print("\n\n程序已被用户中断")
            return
        except EOFError:
            print("\n\n输入结束，退出程序")
            return
        
        if choice == "1":
            # 处理本地视频文件
            try:
                video_path = input("请输入本地视频文件路径: ").strip()
            except KeyboardInterrupt:
                print("\n\n操作已被用户中断")
                continue
            except EOFError:
                print("\n\n输入结束，返回主菜单")
                continue
            
            if not video_path:
                print("错误: 视频文件路径不能为空")
                continue
            
            try:
                # 检查视频文件是否存在
                if not os.path.exists(video_path):
                    print(f"错误: 视频文件不存在: {video_path}")
                    continue
                
                # 保存上传的视频（这里模拟上传过程）
                saved_video_path = analyzer.save_uploaded_video(video_path)
                
                # 提取视频脚本
                analyzer.extract_video_script(saved_video_path)
                
            except Exception as e:
                print(f"处理本地视频时发生错误: {str(e)}")
        
        elif choice == "2":
            # 处理抖音视频链接
            try:
                share_url = input("请输入抖音视频的分享链接或完整分享文本: ").strip()
            except KeyboardInterrupt:
                print("\n\n操作已被用户中断")
                continue
            except EOFError:
                print("\n\n输入结束，返回主菜单")
                continue
            
            if not share_url:
                print("错误: 抖音分享链接不能为空")
                continue
            
            try:
                # 获取无水印视频链接
                print("正在解析抖音视频链接...")
                video_url = analyzer.get_douyin_video_url(share_url)
                print(f"无水印视频链接: {video_url}")
                
                # 下载视频到本地
                saved_video_path = analyzer.download_douyin_video(video_url)
                
                # 提取视频脚本
                analyzer.extract_video_script(saved_video_path)
                
            except Exception as e:
                print(f"处理抖音视频时发生错误: {str(e)}")
        
        elif choice == "3":
            print("感谢使用整合视频分析系统，再见！")
            break
        
        else:
            print("无效选项，请重新输入")

if __name__ == "__main__":
    main()
