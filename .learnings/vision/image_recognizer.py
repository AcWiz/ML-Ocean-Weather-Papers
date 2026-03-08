#!/usr/bin/env python3
"""
图像识别模块
功能：OCR文字识别、图像处理、截图分析
"""
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import numpy as np
import os
from pathlib import Path

class ImageRecognizer:
    """图像识别器"""
    
    def __init__(self):
        self.tesseract_cmd = None  # 自动检测
    
    def recognize_text(self, image_path, lang='eng'):
        """
        从图片中识别文字 (OCR)
        
        Args:
            image_path: 图片路径
            lang: 语言 ('eng', 'chi_sim', 'eng+chi_sim')
        
        Returns:
            str: 识别的文字
        """
        try:
            image = Image.open(image_path)
            
            # 预处理
            image = self._preprocess(image)
            
            # OCR 识别
            text = pytesseract.image_to_string(image, lang=lang)
            
            return text.strip()
            
        except Exception as e:
            return f"识别失败: {e}"
    
    def recognize_chinese(self, image_path):
        """识别中文"""
        return self.recognize_text(image_path, lang='chi_sim')
    
    def _preprocess(self, image):
        """图像预处理"""
        # 转换为灰度
        if image.mode != 'L':
            image = image.convert('L')
        
        # 增加对比度
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2)
        
        # 去噪
        image = image.filter(ImageFilter.MedianFilter())
        
        return image
    
    def get_text_with_boxes(self, image_path):
        """获取带位置信息的文字"""
        try:
            image = Image.open(image_path)
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            
            results = []
            n_boxes = len(data['text'])
            
            for i in range(n_boxes):
                text = data['text'][i].strip()
                if text:
                    results.append({
                        'text': text,
                        'left': data['left'][i],
                        'top': data['top'][i],
                        'width': data['width'][i],
                        'height': data['height'][i],
                        'confidence': data['conf'][i]
                    })
            
            return results
            
        except Exception as e:
            return []
    
    def extract_info(self, image_path, pattern):
        """
        从图片中提取指定信息
        
        Args:
            image_path: 图片路径
            pattern: 正则表达式
        
        Returns:
            list: 匹配的结果
        """
        import re
        
        text = self.recognize_text(image_path)
        matches = re.findall(pattern, text)
        
        return matches


class ImageProcessor:
    """图像处理器"""
    
    @staticmethod
    def resize(image_path, output_path, size=(800, 600)):
        """调整图片大小"""
        img = Image.open(image_path)
        img = img.resize(size, Image.Resampling.LANCZOS)
        img.save(output_path)
        return output_path
    
    @staticmethod
    def crop(image_path, output_path, box):
        """裁剪图片"""
        img = Image.open(image_path)
        img = img.crop(box)
        img.save(output_path)
        return output_path
    
    @staticmethod
    def enhance(image_path, output_path, brightness=1.5, contrast=2.0):
        """增强图片"""
        img = Image.open(image_path)
        
        if brightness != 1.0:
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(brightness)
        
        if contrast != 1.0:
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(contrast)
        
        img.save(output_path)
        return output_path
    
    @staticmethod
    def to_grayscale(image_path, output_path):
        """转为灰度图"""
        img = Image.open(image_path)
        img = img.convert('L')
        img.save(output_path)
        return output_path


# 测试
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        
        recognizer = ImageRecognizer()
        
        print("🔍 图像识别测试...")
        print(f"图片: {image_path}\n")
        
        # 识别文字
        text = recognizer.recognize_text(image_path)
        
        print("识别结果:")
        print(text[:500])
    else:
        print("用法: python image_recognizer.py <图片路径>")
