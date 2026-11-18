# -*- coding: utf-8 -*-
"""
1-Click Cloud Synchronizer cho Tờ Trình Hưng Thịnh
Đồng bộ dữ liệu từ Desktop lên Website 24/7 (GitHub Pages & Gist Vault)
"""

import datetime
import json
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

WEB_DIR = os.path.abspath(os.path.dirname(__file__))
DESKTOP_DIR = os.path.expanduser(r"~\Desktop")
EXCEL_INPUT = os.path.join(DESKTOP_DIR, "DỮ LIỆU ĐẦU VÀO LÀM TỜ TRÌNH.xlsx")
GIST_ID = "3892ec3b8648c7f622847c9dd29e7d2d"
REPO_FULL = "ninhhpvnu-coder/to-trinh-hung-thinh"
WEB_URL = "https://ninhhpvnu-coder.github.io/to-trinh-hung-thinh/"


def run_cmd(args, cwd=None):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="ignore")


def sync():
    print("=" * 65)
    print("   ĐỒNG BỘ TỜ TRÌNH HƯNG THỊNH LÊN CLOUD VĨNH VIỄN (24/7)")
    print("=" * 65)

    # 1. Chạy generator tạo word & bóc tách dữ liệu nếu có file excel
    gen_script = r"j:\Bộ AG Kit\.agents\skills\to-trinh-hung-thinh\scripts\generate_to_trinh.py"
    if os.path.isfile(EXCEL_INPUT) and os.path.isfile(gen_script):
        print("[1/3] Đang đọc file Excel trên Desktop và xuất Word...")
        subprocess.run([
            "python", gen_script,
            "--excel", EXCEL_INPUT,
            "--out", os.path.join(WEB_DIR, "files", "Tong_Hop_To_Trinh_Thang_08_2026.docx"),
            "--out-dir", os.path.join(WEB_DIR, "files")
        ])

    # 2. Cập nhật git
    print("[2/3] Đang đồng bộ mã nguồn & file Word lên GitHub Pages...")
    run_cmd(["git", "add", "-A"], cwd=WEB_DIR)
    status = run_cmd(["git", "status", "--porcelain"], cwd=WEB_DIR)
    if status.stdout.strip():
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        run_cmd(["git", "commit", "-m", f"Cap nhat to trinh cloud ({now_str})"], cwd=WEB_DIR)
        res = run_cmd(["git", "push", "origin", "main"], cwd=WEB_DIR)
        if res.returncode == 0:
            print("  ✓ Đã đẩy thành công lên GitHub Pages!")
        else:
            print("  [!] Lỗi push:", res.stderr.strip())
    else:
        print("  ✓ Dữ liệu trên web đã ở trạng thái mới nhất.")

    # 3. Cập nhật Gist
    vault_file = os.path.join(WEB_DIR, "data", "to_trinh_vault.json")
    if os.path.isfile(vault_file):
        print("[3/3] Đang cập nhật Gist Cloud Vault để điện thoại thấy ngay...")
        res_gist = run_cmd(["gh", "gist", "edit", GIST_ID, "-a", vault_file], cwd=WEB_DIR)
        if res_gist.returncode == 0:
            print("  ✓ Gist Cloud Vault đã được cập nhật!")
        else:
            print("  [!] Gist update notice:", res_gist.stderr.strip())

    print("\n" + "=" * 65)
    print("  ✅ HOÀN TẤT ĐỒNG BỘ 24/7! TRUY CẬP NGAY TẠI:")
    print(f"  👉 {WEB_URL}")
    print("  🔑 Mã PIN mặc định: 123456")
    print("=" * 65)


if __name__ == "__main__":
    sync()
