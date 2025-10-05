# main.py
# Simple CLI for PDF Master Suite
import argparse
from pdf_tools import merge_pdfs, split_pdf, compress_pdf, watermark_pdf, protect_pdf, unlock_pdf

def main():
    parser = argparse.ArgumentParser(prog='pdf-master', description='PDF Master Suite CLI')
    sub = parser.add_subparsers(dest='cmd')

    p1 = sub.add_parser('merge', help='Merge PDFs')
    p1.add_argument('out', help='Output PDF')
    p1.add_argument('inputs', nargs='+', help='Input PDFs')

    p2 = sub.add_parser('split', help='Split PDF pages')
    p2.add_argument('input', help='Input PDF')
    p2.add_argument('--pages', required=True, help='Pages spec e.g. 1-3,5')
    p2.add_argument('--out-dir', default='split_out')

    p3 = sub.add_parser('compress', help='Compress PDF (basic)')
    p3.add_argument('input', help='Input PDF')
    p3.add_argument('output', help='Output PDF')

    p4 = sub.add_parser('watermark', help='Apply text watermark')
    p4.add_argument('input', help='Input PDF')
    p4.add_argument('--text', default='SAMPLE')
    p4.add_argument('output', help='Output PDF')

    p5 = sub.add_parser('protect', help='Protect (encrypt) PDF')
    p5.add_argument('input', help='Input PDF')
    p5.add_argument('output', help='Output PDF')
    p5.add_argument('--password', default='')

    p6 = sub.add_parser('unlock', help='Unlock (decrypt) PDF')
    p6.add_argument('input', help='Input PDF')
    p6.add_argument('output', help='Output PDF')
    p6.add_argument('--password', default='')

    args = parser.parse_args()
    if args.cmd == 'merge':
        merge_pdfs(args.inputs, args.out)
    elif args.cmd == 'split':
        split_pdf(args.input, args.pages, args.out_dir)
    elif args.cmd == 'compress':
        compress_pdf(args.input, args.output)
    elif args.cmd == 'watermark':
        watermark_pdf(args.input, args.output, text=args.text)
    elif args.cmd == 'protect':
        protect_pdf(args.input, args.output, password=args.password)
    elif args.cmd == 'unlock':
        unlock_pdf(args.input, args.output, password=args.password)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
