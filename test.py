import os.path

file_path = r'Z:\临时文件夹\tmp\dxbgtmp\001209_洪兴股份'
file = os.path.join(file_path,"final.txt")
print(file)
f = open(file, "r")
f.close()
