# MirrorPost AI - 素材管理模块
# 用于管理 Logo、二维码、Slogan 等品牌资产

import os
import shutil
from typing import Dict, List, Optional
from PIL import Image


class AssetManager:
    """素材管理器：管理品牌素材的上传、存储和使用"""

    def __init__(self, assets_dir: str = "assets"):
        """
        初始化素材管理器

        参数:
            assets_dir (str): 素材存储目录
        """
        self.assets_dir = assets_dir
        self.logo_dir = os.path.join(assets_dir, "logos")
        self.qr_dir = os.path.join(assets_dir, "qrcodes")
        self._ensure_dirs()

    def _ensure_dirs(self):
        """确保所有素材目录存在"""
        for directory in [self.assets_dir, self.logo_dir, self.qr_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)

    def save_logo(self, image: Image.Image, name: str = "logo") -> bool:
        """
        保存 Logo

        参数:
            image (PIL.Image): Logo 图片
            name (str): Logo 名称

        返回:
            bool: 是否保存成功
        """
        try:
            file_path = os.path.join(self.logo_dir, f"{name}.png")
            image.save(file_path)
            print(f"Logo 已保存: {name}")
            return True
        except Exception as e:
            print(f"保存 Logo 失败: {str(e)}")
            return False

    def save_qrcode(self, image: Image.Image, name: str = "qrcode") -> bool:
        """
        保存二维码

        参数:
            image (PIL.Image): 二维码图片
            name (str): 二维码名称

        返回:
            bool: 是否保存成功
        """
        try:
            file_path = os.path.join(self.qr_dir, f"{name}.png")
            image.save(file_path)
            print(f"二维码已保存: {name}")
            return True
        except Exception as e:
            print(f"保存二维码失败: {str(e)}")
            return False

    def load_logo(self, name: str = "logo") -> Optional[Image.Image]:
        """
        加载 Logo

        参数:
            name (str): Logo 名称

        返回:
            PIL.Image: Logo 图片，如果不存在则返回 None
        """
        try:
            file_path = os.path.join(self.logo_dir, f"{name}.png")
            if os.path.exists(file_path):
                return Image.open(file_path)
            return None
        except Exception as e:
            print(f"加载 Logo 失败: {str(e)}")
            return None

    def load_qrcode(self, name: str = "qrcode") -> Optional[Image.Image]:
        """
        加载二维码

        参数:
            name (str): 二维码名称

        返回:
            PIL.Image: 二维码图片，如果不存在则返回 None
        """
        try:
            file_path = os.path.join(self.qr_dir, f"{name}.png")
            if os.path.exists(file_path):
                return Image.open(file_path)
            return None
        except Exception as e:
            print(f"加载二维码失败: {str(e)}")
            return None

    def list_logos(self) -> List[str]:
        """
        列出所有 Logo

        返回:
            List[str]: Logo 名称列表
        """
        try:
            files = os.listdir(self.logo_dir)
            return [f[:-4] for f in files if f.endswith(".png")]
        except Exception as e:
            print(f"列出 Logo 失败: {str(e)}")
            return []

    def list_qrcodes(self) -> List[str]:
        """
        列出所有二维码

        返回:
            List[str]: 二维码名称列表
        """
        try:
            files = os.listdir(self.qr_dir)
            return [f[:-4] for f in files if f.endswith(".png")]
        except Exception as e:
            print(f"列出二维码失败: {str(e)}")
            return []

    def delete_logo(self, name: str) -> bool:
        """
        删除 Logo

        参数:
            name (str): Logo 名称

        返回:
            bool: 是否删除成功
        """
        try:
            file_path = os.path.join(self.logo_dir, f"{name}.png")
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Logo 已删除: {name}")
                return True
            return False
        except Exception as e:
            print(f"删除 Logo 失败: {str(e)}")
            return False

    def delete_qrcode(self, name: str) -> bool:
        """
        删除二维码

        参数:
            name (str): 二维码名称

        返回:
            bool: 是否删除成功
        """
        try:
            file_path = os.path.join(self.qr_dir, f"{name}.png")
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"二维码已删除: {name}")
                return True
            return False
        except Exception as e:
            print(f"删除二维码失败: {str(e)}")
            return False

    def has_assets(self) -> Dict[str, bool]:
        """
        检查是否有可用的素材

        返回:
            Dict[str, bool]: {'logo': bool, 'qrcode': bool}
        """
        return {
            "logo": len(self.list_logos()) > 0,
            "qrcode": len(self.list_qrcodes()) > 0
        }
