import os.path
from shutil import copyfile

from pdfUtils import *

'''
SOURCE_DIR 是打新股票【打新标的】目录
OUTPUT_DIR 是dxbgtmp目录
'''
SOURCE_DIR = r'\\192.168.10.3\chinan\乘安共享盘\投资管理\网下打新\【打新标的】'
OUTPUT_DIR = r'\\192.168.10.3\chinan\临时文件夹\tmp\dxbgtmp'

'''
BEGIN_DATE 只会考虑BEGIN_DATE之后的股票（含当天）
STOCK_BEGIN_CODE 元组，只会考虑开头在其中的股票
STOCK_BEGIN_SIZE STOCK_BEGIN_CODE元组中每个元素的长度，对应判断股票前几位
'''
BEGIN_DATE = r'2021.06.07'
STOCK_BEGIN_CODE = ('68', '60')
STOCK_BEGIN_SIZE = 2


def pdf_save_as_txt(source_dir, filename, output_dir):
    """
    给定源路径、文件名、输出文件夹，在指定位置生成.txt
    :param source_dir: 源文件夹 ...\2 投价报告
    :param filename: 不含后缀的文件名
    :param output_dir: tmp文件夹输出地址
    :return: None
    """

    '''
    获取详细文件地址，读取pdf内容
    '''
    f_path = os.path.join(source_dir, filename)
    context = read_context(f_path)

    '''
    保存到指定的位置
    '''
    filename_without_suffix = os.path.splitext(filename)[0]
    txt_save(filename_without_suffix, output_dir, context)


'''
程序入口，首先获取OUTPUT_DIR下的文件
'''
src_dir = os.listdir(SOURCE_DIR)


date_str = [e.split(" ")[0] for e in src_dir]
stock_code = [e.split(" ")[1] for e in src_dir]
stock_name = [e.split(" ")[2] for e in src_dir]

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
for i in range(len(src_dir)):  # 遍历src_dir
    if (date_str[i] >= BEGIN_DATE):  # 如果日期在设定日期之后（包含设定日期）
        # 如果股票前两位在需求股票列表中
        if stock_code[i][:STOCK_BEGIN_SIZE] in STOCK_BEGIN_CODE:
            '''
            分别获取2、4文件夹位置，初始化has_report、
            '''
            curr_dir_2 = os.path.join(SOURCE_DIR, src_dir[i], '2 投价报告')
            curr_dir_4 = os.path.join(SOURCE_DIR, src_dir[i], '4 估值 询价')
            curr_output_dir = os.path.join(OUTPUT_DIR, stock_code[i]+'_'+stock_name[i])
            has_report = 0
            has_research = 0
            '''
            根据2、4目录内的文件决定要不要去tmp生成.txt
            '''
            for file in os.listdir(curr_dir_4):  # 遍历询价文件夹下的文件
                if (file.find("估值报告") + 1):  # 如果找到估值报告，则不用更新
                    has_report = 1
                    break
            for file in os.listdir(curr_dir_2):  # 遍历2目录下的所有文件
                if (file.find("投价")+1):  # 如果找到投价报告
                    has_research = 1
                if(file.find("无投价报告")+1):  # 如果发现无投价报告.txt
                    has_research = 0
            '''
            如果有研究报告，但是没有估值报告
            则需要在tmp里生成txt并且复制一份研究报告pdf
            '''
            if has_research and not has_report:

                '''
                遍历符合条件的股票dir下的2号目录
                对其中每个文件进行txt生成、复制pdf
                '''
                for file in os.listdir(curr_dir_2):
                    pdf_save_as_txt(curr_dir_2, file, curr_output_dir)
                    '''
                    复制一份pdf到tmp
                    '''
                    source_pdf = os.path.join(curr_dir_2, file)
                    target_pdf = os.path.join(curr_output_dir, file)
                    copyfile(source_pdf, target_pdf)