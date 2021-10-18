import csv
import os

import xlrd

from Book import Book


def get_books():
    return list(map(lambda filename: os.path.splitext(filename)[0], os.listdir('./books')))


def get_book_size(book_name):
    counter = 0
    with open('books/%s.csv' % book_name, newline='') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            counter += 1
    return counter


def get_xlsx_sheets(path):
    workbook = xlrd.open_workbook(path)
    return workbook.sheet_names()


def update_book_by_xlsx_sheet(xlsx_path, sheet_name):
    _, file_name = os.path.split(xlsx_path)
    file_name, _ = os.path.splitext(file_name)
    csv_path = 'books/%s_%s.csv' % (file_name, sheet_name)

    workbook = xlrd.open_workbook(xlsx_path)
    sheet = workbook.sheet_by_name(sheet_name)
    book = Book('%s_%s' % (file_name, sheet_name))
    for row_id in range(sheet.nrows):
        book.add_tango(*sheet.row_values(row_id))
    book.sort_by_kana()

    if book.size < 4:
        return book.title, '单词量过少'

    mode = '更新' if os.path.exists(csv_path) else '创建'
    book.save_to_csv(path=csv_path)
    return book.title, mode
