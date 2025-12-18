# MirrorPost AI - 风格管理模块
# 用于保存、加载和管理海报风格

import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class StyleManager:
    """风格管理器：管理海报风格的保存和加载"""

    def __init__(self, styles_dir: str = "styles"):
        """
        初始化风格管理器

        参数:
            styles_dir (str): 风格存储目录
        """
        self.styles_dir = styles_dir
        self._ensure_styles_dir()

    def _ensure_styles_dir(self):
        """确保风格目录存在"""
        if not os.path.exists(self.styles_dir):
            os.makedirs(self.styles_dir)

    def save_style(
        self,
        name: str,
        user_prompt: str,
        aspect_ratio: str,
        thinking_mode: bool,
        description: str = ""
    ) -> bool:
        """
        保存风格配置

        参数:
            name (str): 风格名称
            user_prompt (str): 原始提示词
            aspect_ratio (str): 纵横比
            thinking_mode (bool): 是否使用 Thinking 模式
            description (str): 风格描述

        返回:
            bool: 是否保存成功
        """
        try:
            style_data = {
                "name": name,
                "user_prompt": user_prompt,
                "aspect_ratio": aspect_ratio,
                "thinking_mode": thinking_mode,
                "description": description,
                "created_at": datetime.now().isoformat(),
            }

            file_path = os.path.join(self.styles_dir, f"{name}.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(style_data, f, ensure_ascii=False, indent=2)

            print(f"风格已保存: {name}")
            return True

        except Exception as e:
            print(f"保存风格失败: {str(e)}")
            return False

    def load_style(self, name: str) -> Optional[Dict]:
        """
        加载风格配置

        参数:
            name (str): 风格名称

        返回:
            Dict: 风格数据，如果不存在则返回 None
        """
        try:
            file_path = os.path.join(self.styles_dir, f"{name}.json")
            if not os.path.exists(file_path):
                return None

            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)

        except Exception as e:
            print(f"加载风格失败: {str(e)}")
            return None

    def list_styles(self) -> List[Dict]:
        """
        列出所有保存的风格

        返回:
            List[Dict]: 风格列表
        """
        styles = []
        try:
            for filename in os.listdir(self.styles_dir):
                if filename.endswith(".json"):
                    name = filename[:-5]  # 移除 .json 扩展名
                    style_data = self.load_style(name)
                    if style_data:
                        styles.append(style_data)

            # 按创建时间倒序排列
            styles.sort(key=lambda x: x.get("created_at", ""), reverse=True)

        except Exception as e:
            print(f"列出风格失败: {str(e)}")

        return styles

    def delete_style(self, name: str) -> bool:
        """
        删除风格

        参数:
            name (str): 风格名称

        返回:
            bool: 是否删除成功
        """
        try:
            file_path = os.path.join(self.styles_dir, f"{name}.json")
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"风格已删除: {name}")
                return True
            return False

        except Exception as e:
            print(f"删除风格失败: {str(e)}")
            return False

    def style_exists(self, name: str) -> bool:
        """
        检查风格是否存在

        参数:
            name (str): 风格名称

        返回:
            bool: 是否存在
        """
        file_path = os.path.join(self.styles_dir, f"{name}.json")
        return os.path.exists(file_path)
