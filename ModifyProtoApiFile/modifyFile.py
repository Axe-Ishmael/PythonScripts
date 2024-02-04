import os
import re

def process_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        # 把文件中的所有“////”改为“//”
        line = line.replace('////', '//')

        # 如果同一行中包含“-”，并且后面跟了一个数字，如果“-”和数字之间有空格，则去掉他们之间的空格
        line = re.sub(r'-(\s+)(\d+)', r'-\2', line)

        # 如果某行以“message”或“enum”开头，并且这行的末尾有注释，则删掉这行的注释，并且把注释移到这一行的上一行
        match = re.match(r'(message|enum)(.*)(//.*)', line)
        if match:
            comment = match.group(3).strip()
            line = match.group(1) + match.group(2) + '\n'
            new_lines.append(comment + '\n')


        line = re.sub(r"import\s+\'([^\']+)\'\s*;", r'import "\1";', line)

        new_lines.append(line)

    with open(file_path, 'w') as f:
        f.writelines(new_lines)

def traverse_files(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.proto'):
                process_file(os.path.join(root, file))

# 使用方法
traverse_files('/Users/kyrieliao/AndroidStudioProjects/api_proto/src/mobile_framework')