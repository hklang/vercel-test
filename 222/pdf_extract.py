#!/usr/bin/env python3
"""
PDF内容提取工具
用法: python3 pdf_extract.py <pdf文件路径>
"""

import sys
import os

# 使用虚拟环境路径
VENV_PIP = "/home/lang/.openclaw/workspace/venv/bin/pip"
VENV_PYTHON = "/home/lang/.openclaw/workspace/venv/bin/python"

def extract_pdf_text(pdf_path):
    """提取PDF文本内容"""
    try:
        import PyPDF2
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
    except ImportError:
        # 安装 PyPDF2
        print("正在安装 PyPDF2...")
        os.system(f"{VENV_PIP} install PyPDF2 -q")
        import PyPDF2
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 pdf_extract.py <pdf文件路径>")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    
    if not os.path.exists(pdf_file):
        print(f"文件不存在: {pdf_file}")
        sys.exit(1)
    
    print(f"正在提取: {pdf_file}")
    print("-" * 50)
    
    content = extract_pdf_text(pdf_file)
    print(content)
    
    # 同时保存到同名 .txt 文件
    txt_file = os.path.splitext(pdf_file)[0] + ".txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"\n内容已保存到: {txt_file}")
