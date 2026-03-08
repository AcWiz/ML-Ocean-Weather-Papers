#!/usr/bin/env python3
"""
图像识别模块
功能：OCR文字识别、图像处理、截图分析
"""
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import numpy as np
import os
import subprocess

class ImageRecognizer:
    """图像识别器"""
    
    def __init__(self):
        pass
    
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
            # 直接使用 tesseract，不做预处理
            text = pytesseract.image_to_string(Image.open(image_path), lang=lang)
            return text.strip()
        except Exception as e:
            return f"识别失败: {e}"
    
    def recognize_chinese(self, image_path):
        """识别中文"""
        return self.recognize_text(image_path, lang='chi_sim')
    
    def recognize_with_boxes(self, image_path, lang='eng'):
        """获取带位置信息的文字"""
        try:
            data = pytesseract.image_to_data(
                Image.open(image_path), 
                lang=lang,
                output_type=pytesseract.Output.DICT
            )
            
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
    
    def preprocess_for_better_ocr(self, input_path, output_path):
        """预处理图片以提高OCR准确率"""
        try:
            img = Image.open(input_path)
            
            # 转为灰度
            if img.mode != 'L':
                img = img.convert('L')
            
            # 增加对比度
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(2)
            
            # 二值化
            img = img.point(lambda x: 0 if x < 128 else 255, '1')
            img = img.convert('L')
            
            img.save(output_path)
            return output_path
        except Exception as e:
            return None


class ImageProcessor:
    """图像处理器"""
    
    @staticmethod
    def resize(image_path, output_path, size=(800, 600)):
        img = Image.open(image_path)
        img = img.resize(size, Image.Resampling.LANCZOS)
        img.save(output_path)
        return output_path
    
    @staticmethod
    def crop(image_path, output_path, box):
        img = Image.open(image_path)
        img = img.crop(box)
        img.save(output_path)
        return output_path
    
    @staticmethod
    def enhance(image_path, output_path, contrast=2.0, brightness=1.0):
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
    def grayscale(image_path, output_path):
        img = Image.open(image_path)
        img = img.convert('L')
        img.save(output_path)
        return output_path
    
    @staticmethod
    def to_grayscale(image_path):
        img = Image.open(image_path)
        return img.convert('L')


class ImageAnalyzer:
    """图像分析器"""
    
    @staticmethod
    def get_dominant_colors(image_path, n=5):
        img = Image.open(image_path).convert('RGB')
        img = img.resize((50, 50))
        
        import collections
        pixels = np.array(img).reshape(-1, 3)
        colors = collections.Counter(map(tuple, pixels))
        
        return colors.most_common(n)
    
    @staticmethod
    def get_size(image_path):
        img = Image.open(image_path)
        return img.size


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        recognizer = ImageRecognizer()
        
        print(f"识别: {sys.argv[1]}")
        text = recognizer.recognize_text(sys.argv[1])
        print(f"\n结果:\n{text}")
    else:
        print("用法: python image_recognizer.py <图片路径>")
