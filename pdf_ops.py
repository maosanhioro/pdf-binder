import os
from typing import List

import PyPDF2


def unique_path(path: str) -> str:
    base, ext = os.path.splitext(path)
    candidate = path
    i = 2
    while os.path.exists(candidate):
        candidate = f"{base} ({i}){ext}"
        i += 1
    return candidate


def parse_page_spec(spec: str, total_pages: int) -> List[int]:
    if not spec:
        raise ValueError("空のページ指定")
    pages = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            raise ValueError("無効なページ指定")
        if "-" in part:
            a, b = part.split("-", 1)
            try:
                start = int(a)
                end = int(b)
            except Exception:
                raise ValueError("無効なページ指定（数値）")
            if start > end:
                raise ValueError("範囲が不正です")
            for p in range(start, end + 1):
                if p < 1 or p > total_pages:
                    raise ValueError(f"ページ番号 {p} が範囲外です")
                pages.append(p)
        else:
            try:
                pn = int(part)
            except Exception:
                raise ValueError("無効なページ指定（数値）")
            if pn < 1 or pn > total_pages:
                raise ValueError(f"ページ番号 {pn} が範囲外です")
            pages.append(pn)
    if not pages:
        raise ValueError("有効なページ指定がありません")
    return pages


def merge_pdfs(file_paths: List[str], output_dir: str, output_name: str) -> str:
    if len(file_paths) < 2:
        raise ValueError("2件以上のPDFが必要です")
    out_path = os.path.join(output_dir, output_name)
    merger = PyPDF2.PdfMerger()
    try:
        for p in file_paths:
            with open(p, "rb") as fh:
                reader = PyPDF2.PdfReader(fh)
                if getattr(reader, "is_encrypted", False):
                    raise RuntimeError(f"{os.path.basename(p)} は暗号化されています")
                merger.append(reader)
        out_path = unique_path(out_path)
        with open(out_path, "wb") as out_f:
            merger.write(out_f)
    finally:
        try:
            merger.close()
        except Exception:
            pass
    return out_path


def extract_pages(
    file_path: str, page_spec: str, password: str, output_dir: str, output_name: str
) -> str:
    out_path = os.path.join(output_dir, output_name)
    with open(file_path, "rb") as fh:
        reader = PyPDF2.PdfReader(fh)
        if getattr(reader, "is_encrypted", False):
            if not password:
                raise RuntimeError("パスワードが必要です")
            ok = reader.decrypt(password)
            if not ok:
                raise RuntimeError("パスワードが不正です")
        total = len(reader.pages)
        pages = parse_page_spec(page_spec, total)
        writer = PyPDF2.PdfWriter()
        for p in pages:
            writer.add_page(reader.pages[p - 1])
        out_path = unique_path(out_path)
        with open(out_path, "wb") as out_f:
            writer.write(out_f)
    return out_path
    return out_path
    return out_path
