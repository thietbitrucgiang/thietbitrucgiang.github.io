#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import glob

# Địa chỉ mới
ADDRESS = "KM414 quốc lộ 21 Long Phú – Hòa Thạch – Quốc Oai – Hà Nội"

def find_html_files():
    """Tìm tất cả file HTML"""
    html_files = []
    
    # Tìm file HTML trong thư mục gốc
    for file in glob.glob("*.html"):
        html_files.append(file)
    
    # Tìm file HTML trong thư mục products
    for file in glob.glob("products/*.html"):
        html_files.append(file)
    
    return html_files

def update_file(filepath):
    """Cập nhật một file HTML"""
    try:
        print(f"Đang xử lý: {filepath}")
        
        # Đọc file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = False
        
        # 1. Cập nhật footer copyright (thêm địa chỉ nếu chưa có)
        if "©" in content and "Thiết Bị Trúc Giang" in content and "Hotline/Zalo: 0382198383" in content:
            if ADDRESS not in content:
                # Thay thế pattern footer
                old_footer = "© 2024 Thiết Bị Trúc Giang | Hotline/Zalo: 0382198383"
                new_footer = f"© 2024 Thiết Bị Trúc Giang | {ADDRESS} | Hotline/Zalo: 0382198383"
                
                if old_footer in content:
                    content = content.replace(old_footer, new_footer)
                    changes_made = True
                    print(f"  ✓ Cập nhật footer")
        
        # 2. Thêm địa chỉ vào contact info (nếu có phần liên hệ tư vấn)
        if "<h2>Liên hệ tư vấn</h2>" in content and ADDRESS not in content:
            # Tìm và thêm địa chỉ vào đầu phần contact info
            contact_section = '<h2>Liên hệ tư vấn</h2>'
            hotline_line = '<p><strong>Hotline/Zalo:</strong>'
            
            if contact_section in content and hotline_line in content:
                # Thêm dòng địa chỉ trước dòng hotline
                new_address_line = f'<p><strong>Địa chỉ:</strong> {ADDRESS}</p>\n                    '
                content = content.replace(
                    f'{contact_section}\n                    {hotline_line}',
                    f'{contact_section}\n                    {new_address_line}{hotline_line}'
                )
                changes_made = True
                print(f"  ✓ Thêm địa chỉ vào contact info")
        
        # 3. Thêm địa chỉ vào footer section (trong product pages)
        if '<h3>Liên hệ</h3>' in content and 'footer-section' in content and ADDRESS not in content:
            footer_contact = '<h3>Liên hệ</h3>'
            hotline_p = '<p>Hotline/Zalo: 0382198383</p>'
            
            if footer_contact in content and hotline_p in content:
                new_address_p = f'<p>Địa chỉ: {ADDRESS}</p>\n                '
                content = content.replace(
                    f'{footer_contact}\n                {hotline_p}',
                    f'{footer_contact}\n                {new_address_p}{hotline_p}'
                )
                changes_made = True
                print(f"  ✓ Cập nhật footer section")
        
        # 4. Thêm địa chỉ vào danh sách liên hệ (contact.html, about.html)
        if '<li><b>Hotline/Zalo:</b>' in content and ADDRESS not in content:
            hotline_li = '<li><b>Hotline/Zalo:</b>'
            new_address_li = f'<li><b>Địa chỉ:</b> {ADDRESS}</li>\n        '
            
            # Tìm vị trí để chèn địa chỉ (trước hotline)
            if '<ul style="font-size:1.1em;">' in content:
                # Contact.html pattern
                content = content.replace(
                    f'<ul style="font-size:1.1em;">\n        {hotline_li}',
                    f'<ul style="font-size:1.1em;">\n        {new_address_li}{hotline_li}'
                )
                changes_made = True
                print(f"  ✓ Thêm địa chỉ vào danh sách liên hệ")
            elif '<h3>Thông tin liên hệ</h3>' in content:
                # About.html pattern
                content = content.replace(
                    f'<h3>Thông tin liên hệ</h3>\n       <ul>\n         {hotline_li}',
                    f'<h3>Thông tin liên hệ</h3>\n       <ul>\n         {new_address_li}{hotline_li}'
                )
                changes_made = True
                print(f"  ✓ Thêm địa chỉ vào thông tin liên hệ")
        
        # Ghi file nếu có thay đổi
        if changes_made:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ Đã lưu {filepath}")
            return True
        else:
            print(f"  ⏭️ Không cần thay đổi {filepath}")
            return False
            
    except Exception as e:
        print(f"  ❌ Lỗi khi xử lý {filepath}: {e}")
        return False

def main():
    print("🚀 Bắt đầu cập nhật địa chỉ...")
    print(f"📍 Địa chỉ: {ADDRESS}")
    print("-" * 70)
    
    html_files = find_html_files()
    print(f"Tìm thấy {len(html_files)} file HTML:")
    
    updated_count = 0
    for filepath in html_files:
        if update_file(filepath):
            updated_count += 1
        print()
    
    print(f"🎉 Hoàn thành! Cập nhật {updated_count}/{len(html_files)} file.")

if __name__ == "__main__":
    main() 