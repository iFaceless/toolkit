import os.path
import sys
from argparse import ArgumentParser
from os import walk

from PyPDF2 import PdfFileReader, PdfFileWriter


def main():
    parser = ArgumentParser()
    parser.add_argument('-d', '--directory', dest='directory', help='directory that save pdf files')
    parser.add_argument('-f', '--files', dest='files', help='multiple pdf files can be split by ,')
    parser.add_argument('-o', '--output', dest='output', help='output pdf filename', required=True)
    args = parser.parse_args()

    if not args.directory and not args.files:
        print('pdf files or directory not specified')
        sys.exit(1)

    pdf_filenames = args.files or list(list_pdf_files(args.directory))
    if not pdf_filenames:
        print('empty pdf files')
        sys.exit(1)

    pdf_writer = merge_pdf_pages(pdf_filenames)
    with open(args.output, 'wb') as f:
        pdf_writer.write(f)

    print('save merged pdf files to {}'.format(args.output))


def merge_pdf_pages(filenames, ):
    pdf_writer = PdfFileWriter()

    page_no = 0
    for filename in filenames:
        pdf_reader = PdfFileReader(open(filename, 'rb'))
        for idx, page in enumerate(pdf_reader.pages):
            page_no += 1
            pdf_writer.addPage(page)
            if idx == 0:
                pdf_writer.addBookmark(title=extract_as_bookmark_title(filename), pagenum=page_no-1, bold=True)

    return pdf_writer


def extract_as_bookmark_title(filename):
    *_, name = os.path.split(filename)
    realname, _ = os.path.splitext(name)
    return realname


def list_pdf_files(directory):
    for (pth, _, filenames) in walk(directory):
        for filename in filenames:
            yield os.path.join(pth, filename)


if __name__ == '__main__':
    main()
