#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PdfBinder GUI版
PDFファイルの結合とページ抜き取りを直感的なGUIで操作できます
"""

# Windows-only: 日本語ロケール（CP932）を優先
import locale
import os
import platform
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import PyPDF2

try:
    locale.setlocale(locale.LC_ALL, "Japanese_Japan.932")
except:
    pass


class PDFManager:
    def __init__(self, root):
        self.root = root
        self.root.title("PdfBinder")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # Windows専用フォント設定
        self.default_font = ("Yu Gothic UI", 9)
        self.title_font = ("Yu Gothic UI", 18, "bold")
        self.header_font = ("Yu Gothic UI", 12, "bold")
        self.button_font = ("Yu Gothic UI", 10, "bold")

        # 現在のディレクトリ
        self.current_dir = os.getcwd()

        self.create_widgets()
        self.refresh_file_list()

    def create_widgets(self):
        """ウィジェットを作成"""
        # メインタイトル
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill="x", padx=10, pady=(10, 0))
        title_frame.pack_propagate(False)

        title_label = tk.Label(
            title_frame,
            text="PdfBinder",
            font=self.title_font,
            fg="white",
            bg="#2c3e50",
        )
        title_label.pack(expand=True)

        # ディレクトリ選択フレーム
        dir_frame = tk.Frame(self.root, bg="#f0f0f0")
        dir_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(
            dir_frame, text="作業フォルダ:", font=self.default_font, bg="#f0f0f0"
        ).pack(side="left")

        self.dir_var = tk.StringVar(value=self.current_dir)
        dir_entry = tk.Entry(
            dir_frame,
            textvariable=self.dir_var,
            font=self.default_font,
            state="readonly",
        )
        dir_entry.pack(side="left", fill="x", expand=True, padx=(10, 5))

        tk.Button(
            dir_frame,
            text="フォルダ選択",
            command=self.select_directory,
            bg="#3498db",
            fg="white",
            font=self.default_font,
            relief="flat",
            padx=20,
        ).pack(side="right")

        # メインコンテンツエリア
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # 左側：ファイルリスト
        left_frame = tk.Frame(main_frame, bg="#f0f0f0")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        tk.Label(
            left_frame, text="PDFファイル一覧", font=self.header_font, bg="#f0f0f0"
        ).pack(anchor="w", pady=(0, 5))

        # ファイルリストボックス
        list_frame = tk.Frame(left_frame)
        list_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.file_listbox = tk.Listbox(
            list_frame,
            selectmode="extended",
            font=self.default_font,
            yscrollcommand=scrollbar.set,
            bg="white",
            relief="flat",
            borderwidth=1,
            highlightthickness=1,
            highlightcolor="#3498db",
        )
        self.file_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.file_listbox.yview)

        # ファイルリスト更新ボタン
        tk.Button(
            left_frame,
            text="🔄 更新",
            command=self.refresh_file_list,
            bg="#27ae60",
            fg="white",
            font=("Arial", 9),
            relief="flat",
            pady=5,
        ).pack(fill="x", pady=(5, 0))

        # 右側：操作パネル
        right_frame = tk.Frame(main_frame, bg="#f0f0f0")
        right_frame.pack(side="right", fill="both", padx=(5, 0))

        # 操作選択
        tk.Label(
            right_frame, text="🔧 操作を選択", font=("Arial", 12, "bold"), bg="#f0f0f0"
        ).pack(anchor="w", pady=(0, 10))

        # PDF結合セクション
        merge_frame = tk.LabelFrame(
            right_frame,
            text="PDF結合",
            font=("Arial", 10, "bold"),
            bg="#f0f0f0",
            relief="flat",
            borderwidth=2,
        )
        merge_frame.pack(fill="x", pady=(0, 10))

        tk.Label(
            merge_frame,
            text="複数のPDFファイルを1つに結合",
            font=("Arial", 9),
            bg="#f0f0f0",
        ).pack(anchor="w", padx=10, pady=5)

        merge_button = tk.Button(
            merge_frame,
            text="📄➕ PDF結合を開始",
            command=self.open_merge_window,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            pady=8,
        )
        merge_button.pack(fill="x", padx=10, pady=(0, 10))

        # ページ抜き取りセクション
        extract_frame = tk.LabelFrame(
            right_frame,
            text="ページ抜き取り",
            font=("Arial", 10, "bold"),
            bg="#f0f0f0",
            relief="flat",
            borderwidth=2,
        )
        extract_frame.pack(fill="x", pady=(0, 10))

        tk.Label(
            extract_frame,
            text="PDFから指定ページを抜き取り",
            font=("Arial", 9),
            bg="#f0f0f0",
        ).pack(anchor="w", padx=10, pady=5)

        extract_button = tk.Button(
            extract_frame,
            text="📑✂️ ページ抜き取りを開始",
            command=self.open_extract_window,
            bg="#9b59b6",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            pady=8,
        )
        extract_button.pack(fill="x", padx=10, pady=(0, 10))

        # ヘルプセクション
        help_frame = tk.LabelFrame(
            right_frame,
            text="ヘルプ",
            font=("Arial", 10, "bold"),
            bg="#f0f0f0",
            relief="flat",
            borderwidth=2,
        )
        help_frame.pack(fill="x", pady=(0, 10))

        help_text = tk.Text(
            help_frame,
            height=6,
            wrap="word",
            font=("Arial", 8),
            bg="#ecf0f1",
            relief="flat",
        )
        help_text.pack(fill="x", padx=10, pady=5)
        help_text.insert(
            "1.0",
            "📖 使い方:\n\n"
            "1. 作業フォルダを選択\n"
            "2. PDFファイル一覧から操作対象を確認\n"
            "3. 実行したい操作を選択\n"
            "4. 画面の指示に従って操作\n\n"
            "💡 複数ファイル選択: Ctrlキーを押しながらクリック",
        )
        help_text.config(state="disabled")

    def select_directory(self):
        """ディレクトリを選択"""
        directory = filedialog.askdirectory(initialdir=self.current_dir)
        if directory:
            self.current_dir = directory
            self.dir_var.set(directory)
            os.chdir(directory)
            self.refresh_file_list()

    def refresh_file_list(self):
        """ファイルリストを更新"""
        self.file_listbox.delete(0, tk.END)

        try:
            pdf_files = [
                f for f in os.listdir(self.current_dir) if f.lower().endswith(".pdf")
            ]
            pdf_files.sort()

            for pdf_file in pdf_files:
                self.file_listbox.insert(tk.END, pdf_file)

            if not pdf_files:
                self.file_listbox.insert(tk.END, "PDFファイルが見つかりません")

        except Exception as e:
            messagebox.showerror("エラー", f"ファイルリストの取得に失敗しました:\n{e}")

    def open_merge_window(self):
        """PDF結合ウィンドウを開く"""
        MergeWindow(self.root, self.current_dir, self.refresh_file_list)

    def open_extract_window(self):
        """ページ抜き取りウィンドウを開く"""
        ExtractWindow(self.root, self.current_dir, self.refresh_file_list)


class MergeWindow:
    def __init__(self, parent, current_dir, refresh_callback):
        self.current_dir = current_dir
        self.refresh_callback = refresh_callback

        self.window = tk.Toplevel(parent)
        self.window.title("PdfBinder - PDF結合")
        self.window.geometry("600x500")
        self.window.configure(bg="#f0f0f0")
        self.window.grab_set()  # モーダルウィンドウ

        self.create_widgets()
        self.load_pdf_files()

    def create_widgets(self):
        """ウィジェットを作成"""
        # タイトル
        title_label = tk.Label(
            self.window,
            text="📄➕ PDF結合",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50",
        )
        title_label.pack(pady=10)

        # ファイル選択エリア
        file_frame = tk.LabelFrame(
            self.window,
            text="結合するファイルを選択",
            font=("Arial", 10, "bold"),
            bg="#f0f0f0",
        )
        file_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # ファイルリスト
        list_frame = tk.Frame(file_frame)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.file_listbox = tk.Listbox(
            list_frame,
            selectmode="extended",
            font=("Arial", 9),
            yscrollcommand=scrollbar.set,
        )
        self.file_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.file_listbox.yview)

        # 出力ファイル名
        output_frame = tk.Frame(self.window, bg="#f0f0f0")
        output_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(
            output_frame, text="出力ファイル名:", font=("Arial", 10), bg="#f0f0f0"
        ).pack(side="left")
        self.output_var = tk.StringVar(value="結合されたPDF")
        tk.Entry(output_frame, textvariable=self.output_var, font=("Arial", 10)).pack(
            side="left", fill="x", expand=True, padx=(10, 5)
        )
        tk.Label(output_frame, text=".pdf", font=("Arial", 10), bg="#f0f0f0").pack(
            side="right"
        )

        # ボタン
        button_frame = tk.Frame(self.window, bg="#f0f0f0")
        button_frame.pack(fill="x", padx=20, pady=20)

        tk.Button(
            button_frame,
            text="キャンセル",
            command=self.window.destroy,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 10),
            relief="flat",
            padx=20,
        ).pack(side="right", padx=(10, 0))

        tk.Button(
            button_frame,
            text="結合実行",
            command=self.merge_pdfs,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=20,
        ).pack(side="right")

    def load_pdf_files(self):
        """PDFファイルをロード"""
        try:
            pdf_files = [
                f for f in os.listdir(self.current_dir) if f.lower().endswith(".pdf")
            ]
            pdf_files.sort()

            for pdf_file in pdf_files:
                self.file_listbox.insert(tk.END, pdf_file)

        except Exception as e:
            messagebox.showerror("エラー", f"ファイルの読み込みに失敗しました:\n{e}")

    def merge_pdfs(self):
        """PDFを結合"""
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("警告", "結合するファイルを選択してください。")
            return

        output_name = self.output_var.get().strip()
        if not output_name:
            messagebox.showwarning("警告", "出力ファイル名を入力してください。")
            return

        if not output_name.endswith(".pdf"):
            output_name += ".pdf"

        selected_files = [self.file_listbox.get(i) for i in selected_indices]

        try:
            pdf_merger = PyPDF2.PdfMerger()

            for pdf_file in selected_files:
                file_path = os.path.join(self.current_dir, pdf_file)
                with open(file_path, "rb") as file:
                    pdf_merger.append(file)

            output_path = os.path.join(self.current_dir, output_name)
            with open(output_path, "wb") as output_file:
                pdf_merger.write(output_file)

            pdf_merger.close()

            messagebox.showinfo("完了", f"PDFの結合が完了しました:\n{output_name}")
            self.refresh_callback()
            self.window.destroy()

        except Exception as e:
            messagebox.showerror("エラー", f"PDFの結合に失敗しました:\n{e}")


class ExtractWindow:
    def __init__(self, parent, current_dir, refresh_callback):
        self.current_dir = current_dir
        self.refresh_callback = refresh_callback

        self.window = tk.Toplevel(parent)
        self.window.title("PdfBinder - ページ抜き取り")
        self.window.geometry("700x600")
        self.window.configure(bg="#f0f0f0")
        self.window.grab_set()  # モーダルウィンドウ

        self.create_widgets()
        self.load_pdf_files()

    def create_widgets(self):
        """ウィジェットを作成"""
        # タイトル
        title_label = tk.Label(
            self.window,
            text="📑✂️ ページ抜き取り",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50",
        )
        title_label.pack(pady=10)

        # ファイル選択
        file_frame = tk.Frame(self.window, bg="#f0f0f0")
        file_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(
            file_frame, text="PDFファイルを選択:", font=("Arial", 10), bg="#f0f0f0"
        ).pack(side="left")
        self.file_var = tk.StringVar()
        file_combo = ttk.Combobox(
            file_frame, textvariable=self.file_var, state="readonly", font=("Arial", 9)
        )
        file_combo.pack(side="left", fill="x", expand=True, padx=(10, 0))
        file_combo.bind("<<ComboboxSelected>>", self.on_file_selected)
        self.file_combo = file_combo

        # PDF情報表示
        info_frame = tk.LabelFrame(
            self.window,
            text="PDFファイル情報",
            font=("Arial", 10, "bold"),
            bg="#f0f0f0",
        )
        info_frame.pack(fill="x", padx=20, pady=10)

        self.info_text = tk.Text(
            info_frame,
            height=3,
            wrap="word",
            font=("Arial", 9),
            bg="#ecf0f1",
            relief="flat",
        )
        self.info_text.pack(fill="x", padx=10, pady=5)

        # ページ指定
        page_frame = tk.LabelFrame(
            self.window,
            text="抜き取るページを指定",
            font=("Arial", 10, "bold"),
            bg="#f0f0f0",
        )
        page_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # 指定方法の説明
        help_text = tk.Text(
            page_frame,
            height=4,
            wrap="word",
            font=("Arial", 8),
            bg="#fff3cd",
            relief="flat",
        )
        help_text.pack(fill="x", padx=10, pady=5)
        help_text.insert(
            "1.0",
            "📖 ページ指定方法:\n"
            "• 単一ページ: 1,3,5\n"
            "• 範囲指定: 1-5,8,10-12\n"
            "• 混合: 1,3-5,7,9-10",
        )
        help_text.config(state="disabled")

        tk.Label(page_frame, text="ページ番号:", font=("Arial", 10), bg="#f0f0f0").pack(
            anchor="w", padx=10, pady=(10, 5)
        )
        self.page_var = tk.StringVar()
        tk.Entry(page_frame, textvariable=self.page_var, font=("Arial", 10)).pack(
            fill="x", padx=10, pady=(0, 10)
        )

        # 出力ファイル名
        output_frame = tk.Frame(self.window, bg="#f0f0f0")
        output_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(
            output_frame, text="出力ファイル名:", font=("Arial", 10), bg="#f0f0f0"
        ).pack(side="left")
        self.output_var = tk.StringVar(value="抜き取ったページ")
        tk.Entry(output_frame, textvariable=self.output_var, font=("Arial", 10)).pack(
            side="left", fill="x", expand=True, padx=(10, 5)
        )
        tk.Label(output_frame, text=".pdf", font=("Arial", 10), bg="#f0f0f0").pack(
            side="right"
        )

        # ボタン
        button_frame = tk.Frame(self.window, bg="#f0f0f0")
        button_frame.pack(fill="x", padx=20, pady=20)

        tk.Button(
            button_frame,
            text="キャンセル",
            command=self.window.destroy,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 10),
            relief="flat",
            padx=20,
        ).pack(side="right", padx=(10, 0))

        tk.Button(
            button_frame,
            text="抜き取り実行",
            command=self.extract_pages,
            bg="#9b59b6",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=20,
        ).pack(side="right")

    def load_pdf_files(self):
        """PDFファイルをロード"""
        try:
            pdf_files = [
                f for f in os.listdir(self.current_dir) if f.lower().endswith(".pdf")
            ]
            pdf_files.sort()

            self.file_combo["values"] = pdf_files
            if pdf_files:
                self.file_combo.current(0)
                self.on_file_selected(None)

        except Exception as e:
            messagebox.showerror("エラー", f"ファイルの読み込みに失敗しました:\n{e}")

    def on_file_selected(self, event):
        """ファイルが選択されたときの処理"""
        selected_file = self.file_var.get()
        if not selected_file:
            return

        try:
            file_path = os.path.join(self.current_dir, selected_file)
            with open(file_path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)

                info_text = f"ファイル名: {selected_file}\n"
                info_text += f"総ページ数: {total_pages}\n"
                info_text += f"サイズ: {os.path.getsize(file_path) / 1024:.1f} KB"

                self.info_text.config(state="normal")
                self.info_text.delete("1.0", tk.END)
                self.info_text.insert("1.0", info_text)
                self.info_text.config(state="disabled")

        except Exception as e:
            self.info_text.config(state="normal")
            self.info_text.delete("1.0", tk.END)
            self.info_text.insert("1.0", f"エラー: {e}")
            self.info_text.config(state="disabled")

    def parse_page_range(self, page_input, total_pages):
        """ページ範囲を解析"""
        pages = []

        try:
            for part in page_input.split(","):
                part = part.strip()

                if "-" in part:
                    start, end = map(int, part.split("-"))
                    if start <= end:
                        pages.extend(range(start, end + 1))
                else:
                    pages.append(int(part))

            pages = sorted(list(set(pages)))
            valid_pages = [p for p in pages if 1 <= p <= total_pages]

            return valid_pages

        except ValueError:
            return []

    def extract_pages(self):
        """ページを抜き取り"""
        selected_file = self.file_var.get()
        if not selected_file:
            messagebox.showwarning("警告", "PDFファイルを選択してください。")
            return

        page_input = self.page_var.get().strip()
        if not page_input:
            messagebox.showwarning("警告", "ページ番号を入力してください。")
            return

        output_name = self.output_var.get().strip()
        if not output_name:
            messagebox.showwarning("警告", "出力ファイル名を入力してください。")
            return

        if not output_name.endswith(".pdf"):
            output_name += ".pdf"

        try:
            file_path = os.path.join(self.current_dir, selected_file)

            with open(file_path, "rb") as input_file:
                pdf_reader = PyPDF2.PdfReader(input_file)
                total_pages = len(pdf_reader.pages)

                page_numbers = self.parse_page_range(page_input, total_pages)

                if not page_numbers:
                    messagebox.showerror(
                        "エラー", "有効なページ番号を入力してください。"
                    )
                    return

                pdf_writer = PyPDF2.PdfWriter()

                for page_num in page_numbers:
                    pdf_writer.add_page(pdf_reader.pages[page_num - 1])

                output_path = os.path.join(self.current_dir, output_name)
                with open(output_path, "wb") as output_file:
                    pdf_writer.write(output_file)

                messagebox.showinfo(
                    "完了",
                    f"ページの抜き取りが完了しました:\n{output_name}\n抜き取ったページ: {page_numbers}",
                )
                self.refresh_callback()
                self.window.destroy()

        except Exception as e:
            messagebox.showerror("エラー", f"ページの抜き取りに失敗しました:\n{e}")


def main():
    """メイン関数"""
    root = tk.Tk()
    app = PDFManager(root)

    # ウィンドウを中央に配置
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")

    root.mainloop()


if __name__ == "__main__":
    main()
