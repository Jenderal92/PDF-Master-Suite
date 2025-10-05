# gui.py
# GUI for PDF Master Suite (tkinter)
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from pdf_tools import merge_pdfs, split_pdf, compress_pdf, watermark_pdf, protect_pdf, unlock_pdf

APP_TITLE = "PDF Master Suite v1.0"

class App(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        root.title(APP_TITLE)
        root.geometry("820x540")
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        tabControl = ttk.Notebook(self)
        self.tab_merge = ttk.Frame(tabControl)
        self.tab_split = ttk.Frame(tabControl)
        self.tab_compress = ttk.Frame(tabControl)
        self.tab_watermark = ttk.Frame(tabControl)
        self.tab_protect = ttk.Frame(tabControl)

        tabControl.add(self.tab_merge, text='Merge')
        tabControl.add(self.tab_split, text='Split')
        tabControl.add(self.tab_compress, text='Compress')
        tabControl.add(self.tab_watermark, text='Watermark')
        tabControl.add(self.tab_protect, text='Protect/Unlock')
        tabControl.pack(expand=1, fill="both", padx=8, pady=8)

        # Merge tab
        self.merge_files = []
        mf_frame = ttk.Frame(self.tab_merge, padding=10)
        mf_frame.pack(fill='both', expand=True)
        btn_row = ttk.Frame(mf_frame)
        btn_row.pack(fill='x')
        ttk.Button(btn_row, text="Add PDFs", command=self.add_merge_files).pack(side='left')
        ttk.Button(btn_row, text="Remove Selected", command=self.remove_selected_merge).pack(side='left', padx=6)
        ttk.Button(btn_row, text="Clear List", command=self.clear_merge_list).pack(side='left', padx=6)
        self.merge_listbox = tk.Listbox(mf_frame, height=10)
        self.merge_listbox.pack(fill='both', expand=True, pady=8)
        ttk.Button(mf_frame, text="Merge to...", command=self.run_merge).pack(anchor='e')

        # Split tab
        sf_frame = ttk.Frame(self.tab_split, padding=10)
        sf_frame.pack(fill='both', expand=True)
        ttk.Button(sf_frame, text="Select PDF", command=self.select_split_file).pack(anchor='w')
        ttk.Label(sf_frame, text="Pages (e.g. 1-3,5)").pack(anchor='w', pady=(8,0))
        self.pages_entry = ttk.Entry(sf_frame)
        self.pages_entry.pack(fill='x', pady=4)
        ttk.Button(sf_frame, text="Split to...", command=self.run_split).pack(anchor='e')

        # Compress tab
        cf_frame = ttk.Frame(self.tab_compress, padding=10)
        cf_frame.pack(fill='both', expand=True)
        ttk.Button(cf_frame, text="Select PDFs (batch)", command=self.add_compress_files).pack(anchor='w')
        self.compress_listbox = tk.Listbox(cf_frame, height=8)
        self.compress_listbox.pack(fill='both', expand=True, pady=6)
        ttk.Button(cf_frame, text="Compress Selected", command=self.run_compress).pack(anchor='e')

        # Watermark tab
        wf_frame = ttk.Frame(self.tab_watermark, padding=10)
        wf_frame.pack(fill='both', expand=True)
        ttk.Button(wf_frame, text="Select PDFs (batch)", command=self.add_watermark_files).pack(anchor='w')
        self.watermark_listbox = tk.Listbox(wf_frame, height=6)
        self.watermark_listbox.pack(fill='both', expand=True, pady=6)
        ttk.Label(wf_frame, text="Watermark Text").pack(anchor='w')
        self.wm_text = ttk.Entry(wf_frame)
        self.wm_text.pack(fill='x', pady=4)
        ttk.Label(wf_frame, text="Opacity (0.0 - 1.0)").pack(anchor='w', pady=(6,0))
        self.wm_opacity = ttk.Entry(wf_frame)
        self.wm_opacity.insert(0, "0.15")
        self.wm_opacity.pack(fill='x', pady=4)
        ttk.Button(wf_frame, text="Apply Watermark", command=self.run_watermark).pack(anchor='e')

        # Protect tab
        pf_frame = ttk.Frame(self.tab_protect, padding=10)
        pf_frame.pack(fill='both', expand=True)
        ttk.Button(pf_frame, text="Select PDF to Protect", command=self.select_protect_file).pack(anchor='w')
        ttk.Label(pf_frame, text="Password").pack(anchor='w')
        self.pw_entry = ttk.Entry(pf_frame, show="*")
        self.pw_entry.pack(fill='x', pady=4)
        ttk.Button(pf_frame, text="Protect (Encrypt)", command=self.run_protect).pack(anchor='w', pady=6)
        ttk.Separator(pf_frame, orient='horizontal').pack(fill='x', pady=8)
        ttk.Button(pf_frame, text="Select PDF to Unlock", command=self.select_unlock_file).pack(anchor='w')
        ttk.Label(pf_frame, text="Current Password").pack(anchor='w')
        self.upw_entry = ttk.Entry(pf_frame, show="*")
        self.upw_entry.pack(fill='x', pady=4)
        ttk.Button(pf_frame, text="Unlock (Decrypt)", command=self.run_unlock).pack(anchor='w', pady=6)

        # Status bar
        self.status = ttk.Label(self, text="Ready", relief='sunken', anchor='w')
        self.status.pack(side='bottom', fill='x')

    # Merge handlers
    def add_merge_files(self):
        files = filedialog.askopenfilenames(title="Select PDF files", filetypes=[("PDF","*.pdf")])
        for f in files:
            if f not in self.merge_files:
                self.merge_files.append(f)
                self.merge_listbox.insert('end', f)

    def remove_selected_merge(self):
        sel = list(self.merge_listbox.curselection())
        for idx in reversed(sel):
            self.merge_listbox.delete(idx)
            del self.merge_files[idx]

    def clear_merge_list(self):
        self.merge_listbox.delete(0, 'end')
        self.merge_files = []

    def run_merge(self):
        if not self.merge_files:
            messagebox.showinfo("Info","No files selected")
            return
        out = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF","*.pdf")], title="Save merged PDF as")
        if not out:
            return
        self.status.config(text="Merging...")
        threading.Thread(target=self._merge_thread, args=(self.merge_files[:], out)).start()

    def _merge_thread(self, files, out):
        try:
            merge_pdfs(files, out)
            self.status.config(text=f"Merged {len(files)} files -> {out}")
            messagebox.showinfo("Success","Merge complete")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.config(text="Error during merge")

    # Split handlers
    def select_split_file(self):
        f = filedialog.askopenfilename(title="Select PDF", filetypes=[("PDF","*.pdf")])
        if f:
            self.split_file = f
            self.status.config(text=f"Selected {f}")

    def run_split(self):
        if not getattr(self, 'split_file', None):
            messagebox.showinfo("Info","No file selected")
            return
        pages = self.pages_entry.get().strip()
        outdir = filedialog.askdirectory(title="Select output folder")
        if not outdir:
            return
        threading.Thread(target=self._split_thread, args=(self.split_file, pages, outdir)).start()
        self.status.config(text="Splitting...")

    def _split_thread(self, pdf, pages, outdir):
        try:
            split_pdf(pdf, pages, outdir)
            self.status.config(text=f"Split saved to {outdir}")
            messagebox.showinfo("Success","Split complete")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.config(text="Error during split")

    # Compress handlers
    def add_compress_files(self):
        files = filedialog.askopenfilenames(title="Select PDF files", filetypes=[("PDF","*.pdf")])
        for f in files:
            if f not in getattr(self, 'compress_files', []):
                self.compress_files = getattr(self, 'compress_files', []) + [f]
                self.compress_listbox.insert('end', f)

    def run_compress(self):
        if not getattr(self, 'compress_files', None):
            messagebox.showinfo("Info","No files selected")
            return
        outdir = filedialog.askdirectory(title="Select output folder")
        if not outdir:
            return
        threading.Thread(target=self._compress_thread, args=(self.compress_files[:], outdir)).start()
        self.status.config(text="Compressing...")

    def _compress_thread(self, files, outdir):
        try:
            for f in files:
                basename = os.path.basename(f)
                out = os.path.join(outdir, basename)
                compress_pdf(f, out)
            self.status.config(text=f"Compressed {len(files)} files -> {outdir}")
            messagebox.showinfo("Success","Compression complete")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.config(text="Error during compression")

    # Watermark handlers
    def add_watermark_files(self):
        files = filedialog.askopenfilenames(title="Select PDF files", filetypes=[("PDF","*.pdf")])
        for f in files:
            if f not in getattr(self, 'watermark_files', []):
                self.watermark_files = getattr(self, 'watermark_files', []) + [f]
                self.watermark_listbox.insert('end', f)

    def run_watermark(self):
        if not getattr(self, 'watermark_files', None):
            messagebox.showinfo("Info","No files selected")
            return
        text = self.wm_text.get().strip()
        try:
            opacity = float(self.wm_opacity.get().strip())
        except:
            opacity = 0.15
        outdir = filedialog.askdirectory(title="Select output folder")
        if not outdir:
            return
        threading.Thread(target=self._watermark_thread, args=(self.watermark_files[:], text, opacity, outdir)).start()
        self.status.config(text="Applying watermark...")

    def _watermark_thread(self, files, text, opacity, outdir):
        try:
            for f in files:
                out = os.path.join(outdir, os.path.basename(f))
                watermark_pdf(f, out, text=text, opacity=opacity)
            self.status.config(text=f"Watermarked {len(files)} files -> {outdir}")
            messagebox.showinfo("Success","Watermark complete")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.config(text="Error during watermark")

    # Protect/Unlock handlers
    def select_protect_file(self):
        f = filedialog.askopenfilename(title="Select PDF", filetypes=[("PDF","*.pdf")])
        if f:
            self.protect_file = f
            self.status.config(text=f"Selected {f}")

    def run_protect(self):
        if not getattr(self, 'protect_file', None):
            messagebox.showinfo("Info","No file selected")
            return
        pw = self.pw_entry.get().strip()
        out = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF","*.pdf")])
        if not out:
            return
        threading.Thread(target=self._protect_thread, args=(self.protect_file, out, pw)).start()
        self.status.config(text="Protecting...")

    def _protect_thread(self, pdf, out, pw):
        try:
            protect_pdf(pdf, out, password=pw)
            self.status.config(text=f"Protected -> {out}")
            messagebox.showinfo("Success","Protect complete")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.config(text="Error during protect")

    def select_unlock_file(self):
        f = filedialog.askopenfilename(title="Select PDF", filetypes=[("PDF","*.pdf")])
        if f:
            self.unlock_file = f
            self.status.config(text=f"Selected {f}")

    def run_unlock(self):
        if not getattr(self, 'unlock_file', None):
            messagebox.showinfo("Info","No file selected")
            return
        pw = self.upw_entry.get().strip()
        out = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF","*.pdf")])
        if not out:
            return
        threading.Thread(target=self._unlock_thread, args=(self.unlock_file, out, pw)).start()
        self.status.config(text="Unlocking...")

    def _unlock_thread(self, pdf, out, pw):
        try:
            unlock_pdf(pdf, out, password=pw)
            self.status.config(text=f"Unlocked -> {out}")
            messagebox.showinfo("Success","Unlock complete")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.config(text="Error during unlock")

if __name__ == '__main__':
    root = tk.Tk()
    style = ttk.Style(root)
    try:
        style.theme_use('clam')
    except:
        pass
    app = App(root)
    root.mainloop()
