# PDF-Master-Suite

![PDF-Master-Suite](https://github.com/user-attachments/assets/08c8834f-a93a-41cd-891f-9f9ff885f3f5)


PDF Master Suite v1.0 is an all-in-one software designed to manage PDF files effortlessly. Key features include: Merge, Split, Compress, Watermark, and Protect/Unlock PDF with just a few clicks. Perfect for students, office workers, freelancers, and online businesses who frequently work with PDF documents.

**Features**
- Merge multiple PDF files into one (batch support)
- Split a PDF by page ranges or export single pages (batch support)
- Compress (rewrite) PDFs to reduce size (basic)
- Watermark PDFs with text (position, opacity, rotation)
- Protect (encrypt) and Unlock (decrypt) PDFs (owner/user password)

**Requirements**
- Python 3.8+
- Install dependencies:
```

pip install -r requirements.txt

```

**Usage (GUI)**
1. Run `python gui.py`
2. Use tabs to select Merge / Split / Compress / Watermark / Protect
3. Follow on-screen buttons to add files and run operations.

Command Help

```
python main.py -h merge
```

**Usage (CLI examples)**
- Merge:
`python main.py merge out.pdf a.pdf b.pdf c.pdf`
- Split (pages 1-3,5):
`python main.py split in.pdf --pages 1-3,5 --out-dir ./out`
- Watermark:
`python main.py watermark in.pdf --text "SAMPLE" out.pdf`

**Packaging**
To build Windows executable:

```

pip install pyinstaller
pyinstaller --onefile gui.py

```

**Notes**
- Compress is basic; for stronger compression use `pikepdf` or Ghostscript.
- Watermark placement may vary with page sizes; tune font/size in `pdf_tools.py` if needed.
