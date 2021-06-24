import cmd

import pdfplumber
import os
import subprocess

from pylatex import Document, Section, Subsection, Command
from pylatex.utils import italic, NoEscape

from pdfUtils import *

# SOURCE_DIR = r"\\192.168.10.3\chinan\临时文件夹\tmp\dxbgtmp"
# OUTPUT_DIR = r"\\192.168.10.3\chinan\临时文件夹\投资管理\网下打新\【打新标的】"
SOURCE_DIR = "Z:\\临时文件夹\\tmp\\dxbgtmp"
OUTPUT_DIR = "Z:\\临时文件夹\\投资管理\\网下打新\\【打新标的】"

STOCK_BEGIN_CODE = ('68', '60')
STOCK_BEGIN_SIZE = 2
BEGIN_DATE = r'2021.06.07'


def delete_useless_log(filepath, filename):
    """
    将pdflatex生成的log等文件删除
    :param filepath: 输出目录【打新标的】
    :param filename: 文件名
    :return: None
    """
    f = os.path.join(filepath, filename)
    os.unlink(f + '.aux')
    os.unlink(f + '.log')
    os.unlink(f + '.nav')
    os.unlink(f + '.out')
    os.unlink(f + '.snm')
    os.unlink(f + '.toc')


def generate_pdf(data, filename, filepath, output_path):
    """
    根据清理后的数据、文件名、源路径和输出路径，将pdf生成在需要的位置

    :param data: 清洁数据，包含标题、正文、图片
    :param filename: 没有后缀的文件名
    :param filepath: tmp文件夹路径
    :param output_path: 输出文件夹路径 e.g. 【打新标的】/xxx/4 估值 询价/
    :return: pdflatex返回的状态码
    """

    '''
    单独截取出估值区间
    '''
    price_low = data[0]
    price_high = data[1]
    data = data[2:]

    '''
    生成tex路径，开写指针
    '''
    tex_name = filename + ".tex"
    tex_path = os.path.join(filepath, tex_name)
    f = open(tex_path, 'w', encoding='utf-8')

    '''
    生成文件头部参数
    '''
    title = filename.split(os.sep)[-1].replace('_', " ")
    author = None
    institute = None
    date = " "  # 日期留空
    add_header(f, title, author, institute, date)  # 生成latex头部、首页

    '''
    按行读取内容，写入.tex
    '''
    for i in range(len(data)):

        if (judge_title(data, i)):
            add_page_title(f, data[i])

        if (judge_context_body(data, i)):
            add_content_body(f, data[i])

        if (judge_context_tail(data, i)):
            add_content_tail(f, data[i])

        if (judge_img(data, i)):
            img_source = data[i].replace(IMG_BEGIN_SIGN, "")
            img_source = img_source.replace("}", "")
            add_img(f, img_source)

    '''
    生成文件末尾
    '''
    add_ending(f)
    f.close()

    '''
    用命令行由.tex 生成.pdf
    '''
    os.chdir(filepath)
    cmd = ['pdflatex', '-output-directory=' + output_path, tex_name]

    proc = subprocess.Popen(cmd)
    proc.communicate()

    '''
    返回proc的返回值
    '''
    retcode = proc.returncode
    return retcode


def read_file_and_save(file_path, output_path):
    """
    指定文件目录，读取其中的.txt并生成.pdf
    :param file_path: 文件路径
    :param output_path: 输出的文件夹路径，e.g. 【打新标的】/xxx/4 估值 询价/
    :return: None
    """
    try:

        '''
        初始化clean_data[]，同时计算目标final.txt位置
        '''
        txt_context = []
        clean_data = []
        target_txt = os.path.join(file_path, 'final.txt')

        '''
        计算存储文件的名字和地址
        '''
        save_file_name = file_path.split(os.sep)[-1] + "_估值报告"
        save_file_dir = file_path


        '''
        开指针读取目标txt，按行读取，清洗数据
        '''
        f = open(target_txt, 'r', encoding='utf-8')

        for line in f:  # 读文件
            txt_context.append(line)

        for e in txt_context:  # 去除data中的特殊字符与空格
            clean_data.append(content_wash(e))

        '''
        调用方法生成pdf，删去无用的文件
        '''
        generate_pdf(clean_data, save_file_name, save_file_dir, output_path)  # 生成pdf
        delete_useless_log(output_path, save_file_name)

    except (FileNotFoundError):
        print("Final.txt Not Found in :  ", save_file_dir)


'''
程序入口，首先获取OUTPUT_DIR下的文件
'''
out_dir = os.listdir(OUTPUT_DIR)

'''
拆分dir名字
'''
date_str = [e.split(" ")[0] for e in out_dir]
stock_code = [e.split(" ")[1] for e in out_dir]
stock_name = [e.split(" ")[2] for e in out_dir]

'''
添加需要更新的list
'''
need_update_list = []
source_dir_list = []
output_dir_list = []

'''
在打新标的中嵌套if判断是否要更新
得到生成tmp目录列表、输出目录列表
'''
for i in range(len(out_dir)):  # 遍历OUTPUT文件夹
    if (date_str[i] >= BEGIN_DATE):  # 如果日期在设定日期之后（包含设定日期）
        # 如果股票前两位在需求股票列表中
        if stock_code[i][:STOCK_BEGIN_SIZE] in STOCK_BEGIN_CODE:
            curr_dir = os.path.join(OUTPUT_DIR, out_dir[i], '4 估值 询价')
            need_update = 1
            # print(curr_dir)
            for file in os.listdir(curr_dir):  # 遍历询价文件夹下的文件
                if (file.find("估值报告") + 1):  # 如果找到估值报告，则不用更新
                    need_update = 0
                    break
            if (need_update):
                '''
                如果需要更新，生成tmp目录列表、输出目录列表
                '''
                need_update_list.append(i)
                source_dir_list.append(os.path.join(SOURCE_DIR, stock_code[i] + '_' + stock_name[i]))
                output_dir_list.append(curr_dir)

'''
统一更新
'''
for i in range(len(need_update_list)):
    read_file_and_save(source_dir_list[i], output_dir_list[i])