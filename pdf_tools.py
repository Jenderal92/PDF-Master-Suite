# pdf_tools.py
from PyPDF2 import PdfReader, PdfWriter
import os

def merge_pdfs(input_paths, output_path):
    writer = PdfWriter()
    for path in input_paths:
        reader = PdfReader(path)
        for page in reader.pages:
            writer.add_page(page)
    with open(output_path, "wb") as f:
        writer.write(f)

def split_pdf(input_path, output_folder):
    reader = PdfReader(input_path)
    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        outpath = os.path.join(output_folder, f"page_{i+1}.pdf")
        with open(outpath, "wb") as f:
            writer.write(f)

def compress_pdf(input_path, output_path):
    try:
        import pikepdf
        pdf = pikepdf.open(input_path)
        pdf.save(
            output_path,
            compress_streams=True,
            object_stream_mode=pikepdf.ObjectStreamMode.generate,
            recompress_flate=True
        )
        pdf.close()
        print(f"[OK] File dikompres dengan pikepdf: {output_path}")
    except ImportError:
        print("[!] pikepdf tidak terpasang, fallback ke PyPDF2 (hasil kompresi terbatas)")
        reader = PdfReader(input_path)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        with open(output_path, "wb") as f:
            writer.write(f)


def watermark_pdf(input_path, watermark_path, output_path):
    reader = PdfReader(input_path)
    watermark = PdfReader(watermark_path).pages[0]
    writer = PdfWriter()
    for page in reader.pages:
        page.merge_page(watermark)
        writer.add_page(page)
    with open(output_path, "wb") as f:
        writer.write(f)

def protect_pdf(input_path, output_path, password):
    reader = PdfReader(input_path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.encrypt(password)
    with open(output_path, "wb") as f:
        writer.write(f)

def unlock_pdf(input_path, output_path, password):
    reader = PdfReader(input_path)
    if reader.is_encrypted:
        reader.decrypt(password)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    with open(output_path, "wb") as f:
        writer.write(f)