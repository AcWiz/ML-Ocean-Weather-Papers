#!/usr/bin/env python3
"""
图像处理模块
基础图像处理功能
"""
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont
import numpy as np
import os

class ImageProcessor:
    """图像处理器"""
    
    def __init__(self):
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
    
    # ========== 基础操作 ==========
    
    def open(self, path):
        """打开图片"""
        return Image.open(path)
    
    def save(self, image, path):
        """保存图片"""
        image.save(path)
        return path
    
    def resize(self, image, size):
        """调整大小 (width, height)"""
        return image.resize(size, Image.Resampling.LANCZOS)
    
    def crop(self, image, box):
        """裁剪 (left, top, right, bottom)"""
        return image.crop(box)
    
    # ========== 滤镜效果 ==========
    
    def grayscale(self, image):
        """转为灰度图"""
        return image.convert('L')
    
    def blur(self, image, radius=2):
        """模糊"""
        return image.filter(ImageFilter.GaussianBlur(radius))
    
    def sharpen(self, image):
        """锐化"""
        return image.filter(ImageFilter.SHARPEN)
    
    def enhance_contrast(self, image, factor=2.0):
        """增强对比度"""
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)
    
    def enhance_brightness(self, image, factor=1.5):
        """增强亮度"""
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)
    
    def enhance_sharpness(self, image, factor=2.0):
        """增强清晰度"""
        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(factor)
    
    # ========== 绘制功能 ==========
    
    def add_text(self, image, text, position=(0, 0), color='black', size=20):
        """在图片上添加文字"""
        draw = ImageDraw.Draw(image)
        
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
        except:
            font = ImageFont.load_default()
        
        draw.text(position, text, fill=color, font=font)
        return image
    
    def draw_rectangle(self, image, box, outline='red', width=2):
        """绘制矩形"""
        draw = ImageDraw.Draw(image)
        draw.rectangle(box, outline=outline, width=width)
        return image
    
    # ========== 分析功能 ==========
    
    def get_size(self, image):
        """获取图片尺寸"""
        return image.size
    
    def get_mode(self, image):
        """获取颜色模式"""
        return image.mode
    
    def get_pixel(self, image, position):
        """获取像素值"""
        return image.getpixel(position)
    
    def to_array(self, image):
        """转为 numpy 数组"""
        return np.array(image)
    
    # ========== 批量处理 ==========
    
    def batch_resize(self, image_paths, output_dir, size=(800, 600)):
        """批量调整大小"""
        os.makedirs(output_dir, exist_ok=True)
        
        results = []
        for path in image_paths:
            try:
                img = Image.open(path)
                img_resized = self.resize(img, size)
                
                basename = os.path.basename(path)
                output_path = os.path.join(output_dir, basename)
                img_resized.save(output_path)
                
                results.append({"input": path, "output": output_path, "success": True})
            except Exception as e:
                results.append({"input": path, "error": str(e), "success": False})
        
        return results


class ImageAnalyzer:
    """图像分析器"""
    
    @staticmethod
    def get_dominant_colors(image, n=5):
        """获取主色调"""
        img = image.convert('RGB')
        img = img.resize((100, 100))
        
        pixels = np.array(img)
        pixels = pixels.reshape(-1, 3)
        
        # 简单统计
        from collections import Counter
        colors = Counter(map(tuple, pixels))
        
        return colors.most_common(n)
    
    @staticmethod
    def is_blank(image, threshold=250):
        """判断是否空白"""
        img = image.convert('L')
        arr = np.array(img)
        return np.mean(arr) > threshold
    
    @staticmethod
    def get_histogram(image):
        """获取直方图"""
        return image.histogram()


# 便捷函数
def quick_ocr_placeholder(image_path):
    """
    OCR 占位符函数
    注意: 需要安装 tesseract 才能使用 OCR
    """
    return "OCR 需要安装 tesseract: apt-get install tesseract-ocr"


if __name__ == "__main__":
    # 测试
    processor = ImageProcessor()
    
    print("🔧 图像处理测试...")
    
    # 创建测试图片
    img = Image.new('RGB', (200, 100), color='white')
    img = processor.add_text(img, "Hello!", (10, 30), 'black', 30)
    
    # 保存
    test_path = "/tmp/test_image.png"
    processor.save(img, test_path)
    
    print(f"✅ 测试图片已保存: {test_path}")
    
    # 测试处理
    img2 = processor.open(test_path)
    print(f"尺寸: {processor.get_size(img2)}")
    
    img_gray = processor.grayscale(img2)
    img_gray.save("/tmp/test_gray.png")
    print("✅ 灰度图已保存")
