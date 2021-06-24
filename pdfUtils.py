import os
import pdfplumber

IMG_BEGIN_SIGN = r'\includegraphics{'  # final.txt中判断img开始的标志
TXT_SUFFIX = '.txt'

def mkdir(path):
    """
    如果没有文件夹，则创建文件夹
    :param path: 地址
    :return: None
    """

    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径


def read_context(f_path):
    """
    给出指定pdf,读取文件内容
    :param f_path: 文件地址
    :return: 文件内容字符串
    """

    context = ""
    context_list = []
    print("Reading pdf context in: ", f_path)
    with pdfplumber.open(f_path) as pdf:
        for page in pdf.pages:
            # print(page.extract_text())
            try:
                context += page.extract_text()
                context_list.append(page.extract_text())
            except TypeError:
                print(page)
    return context


def search_context(keyword, context):
    """
    检查一段内容中是否有关键字keyword
    :param keyword: 关键字
    :param context: pdf字符串内容
    :return: 概括后的文本字符串
    """

    summary = ""
    for c in context:
        if(c.find(keyword)+1):
            summary += c

    return summary


def txt_save(file_name, output_dir, context):
    """
    给定文件名，文件路径，内容，保存文件
    :param file_name: 无后缀文件名
    :param file_path: 保存文件的地址文件夹
    :param context: 文件内容
    :return: None
    """

    mkdir(output_dir)
    f_path = os.path.join(output_dir, file_name+TXT_SUFFIX)

    f = open(f_path, "w", encoding='utf-8')
    f.write(context)
    f.close()


def content_wash(content):
    """
    清洗数据，清洗空格、斜杠、百分号等
    :param content: 未清洗的数据string
    :return: 清洗后的数据string
    """

    # 删除特殊字符
    clean_data = content.strip().replace("\r","").replace("\n","").replace("\t","")
    # 消除转义
    clean_data = clean_data.replace(r"\&", r"$\backslash$").replace("%", "\%")
    # print("CLEAN DATA: ", clean_data)
    return clean_data


def judge_title(data, i):
    """
    判断第i行文本是否未标题
    :param data: final.txt中的string list
    :param i: 当前行数
    :return: Boolean是否未标题
    """
    if(i == 0 or i==(len(data)-1)):
        return False
    if(data[i] != "" and data[i-1] == "" and data[i+1] == "" and (not data[i].startswith(IMG_BEGIN_SIGN))):
        return True
    return False


def judge_context_body(data, i):
    """
    判断第i行文本是否为context body
    :param data: final.txt中的string list
    :param i: 当前行数
    :return: Boolean是否为context body
    """
    if (i == 0 or i == (len(data) - 1)):
        return False
    if (data[i] != "" and (data[i+1] != "") and not data[i].startswith(IMG_BEGIN_SIGN)):
        return True
    return False


def judge_context_tail(data, i):
    """
    判断第i行文本是否为context 结尾
    :param data: final.txt中的string list
    :param i: 当前行数
    :return: Boolean是否为context 结尾
    """
    if (i == 0 or i >= (len(data))):
        return False
    if(i == (len(data)-1) and data[i] !=""):
        return True
    if (data[i] != "" and (data[i-1] != "")and (data[i+1]=="") and not data[i].startswith(IMG_BEGIN_SIGN)):
        return True
    return False

    return False


def judge_img(data, i):
    """
    判断第i行文本是否为图片
    :param data: final.txt中的string list
    :param i: 当前行数
    :return: Boolean是否为图片
    """
    if (i == 0 or i == (len(data) - 1)):
        return False
    if (data[i] != "" and data[i-1] == "" and data[i+1] == "" and (data[i].startswith(IMG_BEGIN_SIGN))):
        return True
    return False


def add_header(f, title, author, Institute, date):
    """
    为.tex增加文件头部
    :param f: 开着的.tex写指针
    :param title: 文章标题
    :param author: 作者
    :param Institute: 机构
    :param date: 日期
    :return: None
    """

    header_content = r'''\documentclass[t]{beamer}
\usepackage{CTEX}
\usetheme{Madrid}
\usepackage{graphicx}
\usepackage{graphbox}
\title{%(Title)s}
\date{%(date)s}

\begin{document}

\frame{\titlepage}

'''
    # Generate Latex Head
    head_info = dict()
    head_info["Title"] = title
    head_info["Author"] = author
    head_info["Institute"] = Institute
    head_info["date"] = date

    page = header_content % head_info
    f.write(page)


def add_page_title(f, title):
    """
    增加每页标题
    :param f: 开着的写指针
    :param title: 章节标题
    :return: None
    """

    body_content = r'''\begin{frame}
\frametitle{%(Title)s}
'''
    page_info = dict()
    page_info['Title'] = title
    page = body_content % page_info
    f.write(page)


def add_content_body(f, content):
    """
    增加文本内容
    :param f: 开着的写指针
    :param content: 正文内容string
    :return: None
    """

    body_content = r'''%(Content)s'''
    page_info = dict()
    page_info['Content'] = content
    page = body_content % page_info
    f.truncate()
    f.write(page)


def add_content_tail(f, content):
    """
    增加内容结尾
    :param f: 开着的写指针
    :param content: 正文尾部string
    :return: None
    """

    body_content = r'''%(Content)s
\end{frame}

'''
    page_info = dict()
    page_info['Content'] = content
    page = body_content % page_info
    f.truncate()
    f.write(page)

def add_img(f, img):
    """
    Add img with a new beamer page
    :param f: file pointer
    :return: none
    """

    img_content = r'''\begin{center}
\includegraphics[align=c, width=0.9\textwidth]{%(Image)s}
\end{center}
\end{frame}

'''
    page_info = dict()
    page_info['Image'] = img
    page = img_content % page_info
    f.write(page)


def add_ending(f):
    """
    Add the ending to latex template.
    :param f: the file pointer
    :type f: :class:`pylatex.document.Document` instance
    """

    ending_latex = r'''
\end{document}'''
    f.write(ending_latex)