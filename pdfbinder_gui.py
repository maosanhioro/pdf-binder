#!/usr/bin/env python3
# This file is deprecated. The Tkinter GUI implementation has been
# replaced by a PySide6-based GUI in `app.py`/`ui_*.py`.
#
# To avoid accidental usage, importing this module will raise an error.
raise RuntimeError("pdfbinder_gui.py (Tkinter) has been removed. Use app.py (PySide6) instead.")

        # Font preference: Meiryo if available
        try:
            available = tkfont.families()
            base_font = "Meiryo" if "Meiryo" in available else "Segoe UI"
        except Exception:
            base_font = "Segoe UI"

        self.default_font = (base_font, 11)
        self.title_font = (base_font, 18, "bold")
        self.header_font = (base_font, 14, "bold")
        self.button_font = (base_font, 11, "bold")

        # Colors (Calm / Windows-light inspired)
        self.bg_color = "#F4F6F8"
        self.card_color = "#FFFFFF"
        self.border_color = "#E2E6EA"
        self.primary = "#2B7CD3"
        self.accent = "#198754"

        # state: use executable/script directory
        if getattr(sys, "frozen", False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        self.current_dir = base_dir
        self.selected_files = []  # absolute paths (order source)
        self.password_var = tk.StringVar()
        self.page_var = tk.StringVar()

        # Header
        header = tk.Frame(self.root, bg=self.bg_color)
        header.grid(row=0, column=0, sticky="ew", padx=16, pady=(12, 6))
        header.grid_columnconfigure(0, weight=1)
        tk.Label(header, text="PdfBinder", font=self.title_font, bg=self.bg_color).pack(
            side="left"
        )
        tk.Label(
            header,
            text="シンプルに結合/抽出",
            font=(self.default_font[0], 12),
            bg=self.bg_color,
            fg="#6B7280",
        ).pack(side="right")

        # Main two-column layout
        main = tk.Frame(self.root, bg=self.bg_color)
        main.grid(row=1, column=0, sticky="nsew", padx=16, pady=8)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=1)

        # Left panel: file input
        left = tk.Frame(main, bg=self.bg_color)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        tk.Label(left, text="ファイル", font=self.header_font, bg=self.bg_color).pack(
            anchor="w"
        )
        btn_row = tk.Frame(left, bg=self.bg_color)
        btn_row.pack(anchor="w", pady=(6, 2))
        tk.Button(
            btn_row,
            text="PDFを追加",
            command=self.add_files_dialog,
            bg=self.primary,
            fg="white",
            font=self.button_font,
            relief="flat",
        ).pack(side="left")
        tk.Label(
            left,
            text="順番はドラッグで入れ替え",
            font=(self.default_font[0], 9),
            fg="#6B7280",
            bg=self.bg_color,
        ).pack(anchor="w", pady=(6, 0))

        list_frame = tk.Frame(left, bg=self.bg_color)
        list_frame.pack(fill="both", expand=True, pady=8)
        self.file_listbox = tk.Listbox(
            list_frame, height=12, font=self.default_font, selectmode=tk.EXTENDED
        )
        self.file_listbox.pack(side="left", fill="both", expand=True)
        scrollbar = tk.Scrollbar(list_frame, command=self.file_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.file_listbox.config(yscrollcommand=scrollbar.set)

        # move buttons row
        move_panel = tk.Frame(left, bg=self.bg_color)
        move_panel.pack(anchor="e", pady=(6, 0))
        tk.Button(
            move_panel,
            text="上へ",
            command=self.move_up,
            font=(self.default_font[0], 10),
        ).grid(row=0, column=0, padx=4)
        tk.Button(
            move_panel,
            text="下へ",
            command=self.move_down,
            font=(self.default_font[0], 10),
        ).grid(row=0, column=1, padx=4)
        tk.Button(
            move_panel,
            text="削除",
            command=self.remove_selected,
            font=(self.default_font[0], 10),
        ).grid(row=0, column=2, padx=4)

        # enable drag reorder on listbox
        self.file_listbox.bind("<Button-1>", self._on_list_press)
        self.file_listbox.bind("<B1-Motion>", self._on_list_drag)
        self.file_listbox.bind("<ButtonRelease-1>", self._on_list_release)

        # Right panel: operations
        right = tk.Frame(main, bg=self.bg_color)
        right.grid(row=0, column=1, sticky="nsew")
        tk.Label(right, text="操作", font=self.header_font, bg=self.bg_color).pack(
            anchor="w"
        )

        # mode toggle
        mode_row = tk.Frame(right, bg=self.bg_color)
        mode_row.pack(anchor="w", pady=(6, 8))
        self.mode_var = tk.StringVar(value="merge")
        tk.Radiobutton(
            mode_row,
            text="結合",
            value="merge",
            variable=self.mode_var,
            command=self.render_mode,
            bg=self.bg_color,
        ).pack(side="left", padx=(0, 8))
        tk.Radiobutton(
            mode_row,
            text="抜粋",
            value="extract",
            variable=self.mode_var,
            command=self.render_mode,
            bg=self.bg_color,
        ).pack(side="left")

        # mode container card
        self.mode_container = tk.Frame(right, bg=self.card_color, bd=1, relief="flat")
        self.mode_container.pack(fill="both", expand=True, pady=(0, 8))

        # merge view
        self.merge_view = tk.Frame(self.mode_container, bg=self.card_color)
        tk.Label(self.merge_view, text="出力先", bg=self.card_color).grid(
            row=0, column=0, sticky="w", padx=12, pady=(12, 4)
        )
        self.output_dir = tk.StringVar(value=self.current_dir)
        tk.Entry(self.merge_view, textvariable=self.output_dir, width=36).grid(
            row=0, column=1, padx=6, pady=(12, 4)
        )
        tk.Button(self.merge_view, text="参照", command=self.choose_dir).grid(
            row=0, column=2, padx=6, pady=(12, 4)
        )
        tk.Label(self.merge_view, text="出力名", bg=self.card_color).grid(
            row=1, column=0, sticky="w", padx=12, pady=(4, 8)
        )
        self.output_name = tk.StringVar(value="merged.pdf")
        tk.Entry(self.merge_view, textvariable=self.output_name, width=36).grid(
            row=1, column=1, padx=6, pady=(4, 8)
        )
        tk.Button(
            self.merge_view,
            text="結合を実行",
            command=self.merge_pdfs,
            bg=self.primary,
            fg="white",
        ).grid(row=2, column=0, columnspan=3, pady=(8, 12))

        # extract view
        self.extract_view = tk.Frame(self.mode_container, bg=self.card_color)
        tk.Label(
            self.extract_view, text="ページ指定 (例: 1,3-5)", bg=self.card_color
        ).grid(row=0, column=0, sticky="w", padx=12, pady=(12, 4))
        tk.Entry(self.extract_view, textvariable=self.page_var, width=36).grid(
            row=0, column=1, padx=6, pady=(12, 4)
        )
        tk.Label(
            self.extract_view, text="パスワード (必要時)", bg=self.card_color
        ).grid(row=1, column=0, sticky="w", padx=12, pady=(4, 4))
        tk.Entry(
            self.extract_view, textvariable=self.password_var, show="*", width=36
        ).grid(row=1, column=1, padx=6, pady=(4, 4))
        tk.Label(self.extract_view, text="出力先", bg=self.card_color).grid(
            row=2, column=0, sticky="w", padx=12, pady=(4, 4)
        )
        tk.Entry(self.extract_view, textvariable=self.output_dir, width=36).grid(
            row=2, column=1, padx=6, pady=(4, 4)
        )
        tk.Button(self.extract_view, text="参照", command=self.choose_dir).grid(
            row=2, column=2, padx=6, pady=(4, 4)
        )
        tk.Label(self.extract_view, text="出力名", bg=self.card_color).grid(
            row=3, column=0, sticky="w", padx=12, pady=(4, 8)
        )
        self.extract_name = tk.StringVar(value="extracted.pdf")
        tk.Entry(self.extract_view, textvariable=self.extract_name, width=36).grid(
            row=3, column=1, padx=6, pady=(4, 8)
        )
        tk.Button(
            self.extract_view,
            text="抜粋を実行",
            command=self.extract_pages,
            bg=self.accent,
            fg="white",
        ).grid(row=4, column=0, columnspan=3, pady=(8, 12))

        # initially render merge view
        self.render_mode()

        # Footer: progress + status
        footer = tk.Frame(self.root, bg=self.bg_color)
        footer.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 12))
        self.progress = ttk.Progressbar(footer, mode="indeterminate")
        self.progress.pack(side="left", fill="x", expand=True, padx=(0, 12))
        self.status_var = tk.StringVar(value="準備完了")
        tk.Label(
            footer, textvariable=self.status_var, bg=self.bg_color, fg="#6B7280"
        ).pack(side="right")

    def add_files_dialog(self):
        paths = filedialog.askopenfilenames(
            title="追加するPDFファイルを選択",
            initialdir=self.current_dir,
            filetypes=[("PDF files", "*.pdf")],
        )
        if not paths:
            return

        added = False
        for src in paths:
            if not src.lower().endswith(".pdf"):
                continue
            if src in self.selected_files:
                continue
            self.selected_files.append(src)
            added = True

        if added:
            self.update_files_display()

    def remove_selected(self):
        sel = list(self.file_listbox.curselection())
        if not sel:
            return
        # remove from selected_files in reverse order
        for i in sorted(sel, reverse=True):
            try:
                del self.selected_files[i]
            except Exception:
                pass
        self.update_files_display()

    def choose_dir(self):
        d = filedialog.askdirectory(initialdir=self.current_dir, title="出力先を選択")
        if d:
            self.output_dir.set(d)

    def render_mode(self):
        # clear container
        for w in self.mode_container.winfo_children():
            w.pack_forget() if hasattr(w, "pack_info") else None
            try:
                w.grid_forget()
            except Exception:
                pass
        mode = self.mode_var.get()
        if mode == "merge":
            self.merge_view.pack(fill="both", expand=True)
        else:
            self.extract_view.pack(fill="both", expand=True)

    # Drag & drop reordering for Listbox (reorders selected_files)
    def _on_list_press(self, event):
        try:
            idx = self.file_listbox.nearest(event.y)
            self._drag_index = idx
            self._drag_active = True
        except Exception:
            self._drag_index = None
            self._drag_active = False

    def _on_list_drag(self, event):
        if not getattr(self, "_drag_active", False):
            return
        try:
            target = self.file_listbox.nearest(event.y)
            if target != self._drag_index and 0 <= target < len(self.selected_files):
                # move element
                item = self.selected_files.pop(self._drag_index)
                self.selected_files.insert(target, item)
                self._drag_index = target
                self.update_files_display()
                # restore selection to moved item
                self.file_listbox.selection_clear(0, tk.END)
                self.file_listbox.selection_set(target)
        except Exception:
            pass

    def _on_list_release(self, event):
        self._drag_active = False
        self._drag_index = None

    # D&D support removed for compatibility across environments

    # Note: file-adding is done via `ファイルを選択` ボタン

    def _on_files_dropped(self, files):
        # removed
        return

    def update_files_display(self):
        self.file_listbox.delete(0, tk.END)
        for p in self.selected_files:
            self.file_listbox.insert(tk.END, os.path.basename(p))
        self.status_var.set(f"ファイル数: {len(self.selected_files)}")

    def move_up(self):
        sel = list(self.file_listbox.curselection())
        if not sel:
            return
        if min(sel) == 0:
            return
        # move selected items up preserving relative order
        for idx in sorted(sel):
            if idx - 1 in sel:
                continue
            self.selected_files[idx - 1], self.selected_files[idx] = (
                self.selected_files[idx],
                self.selected_files[idx - 1],
            )

        self.update_files_display()
        # restore selection
        new_sel = [i - 1 for i in sel]
        for i in new_sel:
            self.file_listbox.selection_set(i)

    def move_down(self):
        sel = list(self.file_listbox.curselection())
        if not sel:
            return
        if max(sel) >= len(self.selected_files) - 1:
            return
        # move selected items down preserving relative order
        for idx in sorted(sel, reverse=True):
            if idx + 1 in sel:
                continue
            self.selected_files[idx + 1], self.selected_files[idx] = (
                self.selected_files[idx],
                self.selected_files[idx + 1],
            )

        self.update_files_display()
        # restore selection
        new_sel = [i + 1 for i in sel]
        for i in new_sel:
            self.file_listbox.selection_set(i)

    def _start_progress(self, maximum=None):
        if maximum:
            self.progress.config(mode="determinate", maximum=maximum, value=0)
        else:
            self.progress.config(mode="indeterminate")
            self.progress.start(10)

    def _stop_progress(self):
        try:
            if self.progress["mode"] == "indeterminate":
                self.progress.stop()
        except Exception:
            pass
        try:
            self.progress.config(value=0)
        except Exception:
            pass

    def merge_pdfs(self):
        if len(self.selected_files) < 2:
            messagebox.showerror(
                "エラー", "結合するPDFファイルを2件以上追加してください。"
            )
            return

        out_dir = self.output_dir.get() or self.current_dir
        out_name = self.output_name.get() or "merged.pdf"
        out_path = os.path.join(out_dir, out_name)

        try:
            self.status_var.set("結合中...")
            self._start_progress()

            merger = PyPDF2.PdfMerger()
            for p in self.selected_files:
                with open(p, "rb") as fh:
                    reader = PyPDF2.PdfReader(fh)
                    if getattr(reader, "is_encrypted", False):
                        raise RuntimeError(
                            f"{os.path.basename(p)} は暗号化されています。結合はサポートされていません。"
                        )
                    merger.append(reader)

            out_path = unique_path(out_path)
            with open(out_path, "wb") as out_f:
                merger.write(out_f)
            merger.close()

            self.status_var.set(f"結合完了: {os.path.basename(out_path)}")
            self._stop_progress()
        except Exception as e:
            self._stop_progress()
            self.status_var.set("エラー")
            messagebox.showerror("エラー", f"PDFの結合に失敗しました:\n{e}")

    def extract_pages(self):
        if not self.selected_files:
            messagebox.showerror("エラー", "抽出対象のPDFファイルを追加してください。")
            return

        sel = self.file_listbox.curselection()
        if not sel:
            messagebox.showerror(
                "エラー", "抽出したいファイルをリストから選択してください。"
            )
            return
        if len(sel) > 1:
            messagebox.showerror(
                "エラー", "抜き取りは1つのファイルのみ選択してください。"
            )
            return
        selected_path = self.selected_files[sel[0]]

        page_input = self.page_var.get().strip()
        if not page_input:
            messagebox.showerror(
                "エラー", "抜き取りたいページをページ指定欄に入力してください。"
            )
            return

        out_dir = self.output_dir.get() or self.current_dir
        out_name = self.extract_name.get() or "extracted.pdf"
        out_path = os.path.join(out_dir, out_name)

        pw = self.password_var.get().strip() if self.password_var.get() else None

        try:
            self.status_var.set("抜き取り中...")
            self._start_progress()

            with open(selected_path, "rb") as fh:
                reader = PyPDF2.PdfReader(fh)
                if getattr(reader, "is_encrypted", False):
                    if not pw:
                        raise RuntimeError(
                            "このPDFはパスワードで保護されています。パスワードを入力してください。"
                        )
                    ok = reader.decrypt(pw)
                    if not ok:
                        raise RuntimeError("パスワードが不正です。")

                total_pages = len(reader.pages)
                pages = []
                for part in page_input.split(","):
                    part = part.strip()
                    if "-" in part:
                        vals = part.split("-", 1)
                        try:
                            start = int(vals[0])
                            end = int(vals[1])
                        except Exception:
                            raise RuntimeError("無効なページ指定です。")
                        if start > end:
                            raise RuntimeError("無効なページ範囲です。")
                        for pn in range(start, end + 1):
                            if pn < 1 or pn > total_pages:
                                raise RuntimeError(f"ページ番号 {pn} が範囲外です。")
                            pages.append(pn)
                    else:
                        try:
                            pn = int(part)
                        except Exception:
                            raise RuntimeError("無効なページ指定です。")
                        if pn < 1 or pn > total_pages:
                            raise RuntimeError(f"ページ番号 {pn} が範囲外です。")
                        pages.append(pn)

                if not pages:
                    raise RuntimeError("有効なページ指定がありません。")

                writer = PyPDF2.PdfWriter()
                for p in pages:
                    writer.add_page(reader.pages[p - 1])

                out_path = unique_path(out_path)
                with open(out_path, "wb") as out_f:
                    writer.write(out_f)

            self.status_var.set(f"抜き取り完了: {os.path.basename(out_path)}")
            self._stop_progress()

        except Exception as e:
            self._stop_progress()
            self.status_var.set("エラー")
            messagebox.showerror("エラー", f"ページの抜き取りに失敗しました:\n{e}")


def main():
    root = tk.Tk()
    app = PDFManager(root)

    # center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")

    root.mainloop()


if __name__ == "__main__":
    main()
