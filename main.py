# This Python script extracts content from pdf.
import os.path

import pdfplumber
from shutil import copyfile

# root_dir = r'Z:\乘安共享盘\投资管理\网下打新\【打新标的】'
root_dir = r'\\192.168.10.3\chinan\乘安共享盘\投资管理\网下打新\【打新标的】'
# root_dir = r'C:\Users\Steven Wang\Documents\2021ChinShen\reference\因子投资相关报告\input'
file_path = r'C:\Users\Steven Wang\Documents\2021ChinShen\reference\因子投资相关报告\华创 - alpha检验与合成的新思路.pdf'
keyword = ""
# file_save_dir = r'C:\Projects\PycharmProjects\pdfExtractor\out'
file_save_dir = r'\\192.168.10.3\chinan\临时文件夹\tmp\dxbgtmp'
file_save_name = ""
first_date = '2021.06.07'


def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径


def read_context(f_path):

    context = ""
    context_list = []
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

    summary = ""
    for c in context:
        if(c.find(keyword)+1):
            summary += c

    return summary


def pdfSave(file_name, file_path, context):

    mkdir(file_path)
    f_path = os.path.join(file_path, file_name)
    print(f_path)
    f = open(f_path, "w", encoding='utf-8')
    f.write(context)
    f.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # context = read_context(file_path)
    # # print(context)
    # su = search_context(keyword, context)
    # pdfSave(file_save_name, file_save_path, su)

    # f = open(r'\\192.168.10.3\chinan\临时文件夹\tmp\dxtmp\emmm.txt', 'r')

    # 生成需要写txt的股票代码
    need_update_list = []

    for root, dirs, files in os.walk(root_dir, topdown=False):
        for name in dirs:
            # if(len(root.split(os.sep))>=8):
            #     dir_date = root.split(os.sep)[8].split(' ')[0]
            try:
                dir_date = root.split(os.sep)[8].split(' ')[0]
            except IndexError:
                print(root)
            name_spli = name.split(' ')
            root_spli = root.split(' ')

            '''
            探寻4文件夹，如果没有估值报告则加入
            '''
            if(len(name_spli) > 1 and name_spli[0] == '4' and dir_date > first_date):
                file_path = os.path.join(root, name)
                print(file_path, dir_date, " first date: ", first_date)
                has_report = 0

                for root, dirs, files in os.walk(file_path, topdown=False):
                    for file_name in files:
                        if(file_name.find("估值")+1):  # 如果已经有估值报告了，就不用重新生成
                            print(root, "找到估值报告 文件名: ", file_name,"  ", file_name.find("估值报告"))
                            has_report = 1
                            break

                if(has_report == 0):
                    need_update_list.append(root_spli[1])
    '''
    把那些无估价报告的去除
    '''
    for root, dirs, files in os.walk(root_dir, topdown=False):
        for name in dirs:
            try:
                dir_date = root.split(os.sep)[8].split(' ')[0]
            except IndexError:
                print(root)
            name_spli = name.split(' ')
            root_spli = root.split(' ')
            if (len(name_spli) > 1 and name_spli[0] == '2' and dir_date > first_date):
                file_path_2 = os.path.join(root, name)
                print(file_path_2, dir_date)
                need_remove = 0

                for root, dirs, files in os.walk(file_path_2, topdown=False):
                    for file_name in files:
                        if (file_name.find("无")+1):  # 如果已经有估值报告了，就不用重新生成
                            need_remove = 1
                            break

                if (need_remove == 1 and (root_spli[1] in need_update_list)):
                    print("Ready to remove...", root_spli)
                    need_update_list.remove(root_spli[1])

    print(need_update_list)

    for root, dirs, files in os.walk(root_dir, topdown=False):

        for name in dirs:
            name_spli = name.split(' ')
            root_spli = root.split(' ')

            if(len(name_spli)>1 and name_spli[0] == '2'): # 找到目标dir

                target_dir = os.path.join(root, name)  # 获得文件夹名
                for root, dirs, files in os.walk(target_dir, topdown=False):
                    for file in files:
                        if((file.find(".pdf")+1) and (root_spli[1] in need_update_list)):
                            print("Searching in file: ", file)
                            target_file = os.path.join(target_dir, file)
                            su = read_context(target_file)
                            save_dir = os.path.join(file_save_dir, (root_spli[1]+'_'+root_spli[2]))
                            print("SAVE_DIR:  ", save_dir)
                            save_file_name = os.path.splitext(file)[0] + '.txt'
                            copy_pdf_name = os.path.join(save_dir, os.path.splitext(file)[0] + '.pdf')
                            # save_file_name = root.split('\\')[8] + save_file_name
                            print("Saving file: ", save_file_name)
                            pdfSave(save_file_name, save_dir, su)
                            copyfile(target_file,copy_pdf_name)



