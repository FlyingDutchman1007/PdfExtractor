# This Python script extracts content from pdf.
import os.path

import pdfplumber

file_path = r'C:\Users\Steven Wang\Documents\2021ChinShen\reference\因子投资相关报告\华创 - alpha检验与合成的新思路.pdf'
keyword = "最大"
file_save_path = r'C:\Users\Steven Wang\Documents\2021ChinShen\reference\因子投资相关报告'
file_save_name = "pdfSaveTest.txt"

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def read_context(f_path):

    context = ""
    context_list = []
    with pdfplumber.open(f_path) as pdf:
        for page in pdf.pages:
            # print(page.extract_text())
            context += page.extract_text()
            context_list.append(page.extract_text())

    return context_list

def search_context(keyword, context):

    summary = ""
    for c in context:
        if(c.find(keyword)+1):
            summary += c

    return summary


def pdfSave(file_name, file_path, context):
    f_path = os.path.join(file_path, file_name)
    print(f_path)
    f = open(f_path, "w", encoding='utf-8')
    f.write(context)
    f.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    context = read_context(file_path)
    # print(context)
    su = search_context(keyword, context)
    pdfSave(file_save_name, file_save_path, su)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
