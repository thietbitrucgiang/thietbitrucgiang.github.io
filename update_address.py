#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import glob
from pathlib import Path

# Địa chỉ mới cần cập nhật
NEW_ADDRESS = "KM414 quốc lộ 21 Long Phú – Hòa Thạch – Quốc Oai – Hà Nội"

def update_html_files():
    """
    Tự động cập nhật địa chỉ cho tất cả file HTML trong website
    """
    # Tìm tất cả file HTML
    html_files = []
    for pattern in ['*.html', 'products/*.html']:
        html_files.extend(glob.glob(pattern, recursive=True))
    
    print(f"Tìm thấy {len(html_files)} file HTML cần cập nhật:")
    for file in html_files:
        print(f"  - {file}")
    
    updated_count = 0
    
    for html_file in html_files:
        try:
            # Đọc nội dung file
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Pattern 1: Cập nhật footer copyright
            # Tìm pattern "| Hotline/Zalo: 0382198383" và thêm địa chỉ trước đó
            footer_pattern = r'(\&copy; 2024 Thiết Bị Trúc Giang)(\s*\|\s*Hotline/Zalo: 0382198383)'
            if re.search(footer_pattern, content):
                # Kiểm tra xem địa chỉ đã có chưa
                if NEW_ADDRESS not in content:
                    content = re.sub(
                        footer_pattern, 
                        rf'\1 | {NEW_ADDRESS}\2', 
                        content
                    )
                    print(f"  ✓ Cập nhật footer trong {html_file}")
            
            # Pattern 2: Thêm địa chỉ vào danh sách liên hệ (nếu chưa có)
            # Tìm danh sách thông tin liên hệ và thêm địa chỉ
            contact_patterns = [
                # Pattern cho contact.html
                r'(<ul style="font-size:1\.1em;">)\s*(<li><b>Hotline/Zalo:</b>)',
                # Pattern cho about.html - thông tin liên hệ cuối trang
                r'(<h3>Thông tin liên hệ</h3>\s*<ul>)\s*(<li><b>Hotline/Zalo:</b>)',
                # Pattern chung cho các danh sách khác
                r'(<ul[^>]*>)\s*(<li><b>Hotline/Zalo:</b>)'
            ]
            
            for pattern in contact_patterns:
                if re.search(pattern, content) and NEW_ADDRESS not in content:
                    content = re.sub(
                        pattern,
                        rf'\1\n        <li><b>Địa chỉ:</b> {NEW_ADDRESS}</li>\n        \2',
                        content,
                        flags=re.MULTILINE
                    )
                    print(f"  ✓ Thêm địa chỉ vào danh sách liên hệ trong {html_file}")
                    break
            
            # Pattern 3: Cập nhật phần contact-info trong product pages
            contact_info_pattern = r'(<div class="contact-info">\s*<h2>Liên hệ tư vấn</h2>)\s*(<p><strong>Hotline/Zalo:</strong>)'
            if re.search(contact_info_pattern, content) and NEW_ADDRESS not in content:
                content = re.sub(
                    contact_info_pattern,
                    rf'\1\n                    <p><strong>Địa chỉ:</strong> {NEW_ADDRESS}</p>\n                    \2',
                    content,
                    flags=re.MULTILINE
                )
                print(f"  ✓ Cập nhật contact-info trong {html_file}")
            
            # Pattern 4: Cập nhật footer-section trong product pages
            footer_section_pattern = r'(<div class="footer-section">\s*<h3>Liên hệ</h3>)\s*(<p>Hotline/Zalo: 0382198383</p>)'
            if re.search(footer_section_pattern, content) and f'<p>Địa chỉ: {NEW_ADDRESS}</p>' not in content:
                content = re.sub(
                    footer_section_pattern,
                    rf'\1\n                <p>Địa chỉ: {NEW_ADDRESS}</p>\n                \2',
                    content,
                    flags=re.MULTILINE
                )
                print(f"  ✓ Cập nhật footer-section trong {html_file}")
            
            # Ghi lại file nếu có thay đổi
            if content != original_content:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated_count += 1
                print(f"  ✅ Đã cập nhật {html_file}")
            else:
                print(f"  ⏭️  Không cần cập nhật {html_file} (đã có địa chỉ)")
                
        except Exception as e:
            print(f"  ❌ Lỗi khi cập nhật {html_file}: {e}")
    
    print(f"\n🎉 Hoàn thành! Đã cập nhật {updated_count}/{len(html_files)} file HTML.")

if __name__ == "__main__":
    print("🚀 Bắt đầu cập nhật địa chỉ cho tất cả file HTML...")
    print(f"📍 Địa chỉ mới: {NEW_ADDRESS}")
    print("-" * 80)
    
    update_html_files() 