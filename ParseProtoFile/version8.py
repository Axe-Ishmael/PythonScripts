import os
import re
import subprocess
from pathlib import Path

# 指定源目录和目标目录
source_dir = "/Users/kyrieliao/AndroidStudioProjects/api_proto/src/mobile_framework"
target_dir = "/Users/kyrieliao/python_script/protogeneratedproduclog12"

error_log_file = "/Users/kyrieliao/python_script/error_log12.txt"  # 指定错误日志文件的路径

error_count = 0
proto_file_count = 0



def getImportProtoAbsPath(currentAbsPath,import_file):

    base_path_string_list = currentAbsPath.split("/")

    filepathList = []

    import_file_string_list = import_file.split("/")
    target_path = base_path_string_list[:len(base_path_string_list) - len(import_file_string_list)+1] + import_file_string_list
    # 拼接 target_path 的元素，并返回绝对路径字符串
    absolute_path = "/".join(target_path)
    

    return absolute_path




def get_proto_files_recursively(proto_file_path, base_dir):
    visited_files = []

    def visit_proto_file(file_path):
        if file_path not in visited_files:
            visited_files.append(file_path)
            with open(file_path, 'r') as f:
                content = f.read()

            # 正则表达式用于匹配 import 语句（排除注释）
            import_pattern = re.compile(r'^import\s+"(.+\.proto)";', re.MULTILINE)

            # 查找并记录所有 import 文件
            for match in import_pattern.finditer(content):
                imported_file = match.group(1)
                imported_file_path = getImportProtoAbsPath(os.path.dirname(file_path),imported_file)

                if not os.path.isfile(imported_file_path):
                    imported_file_path = os.path.join(base_dir, imported_file)
                    if not os.path.isfile(imported_file_path):
                        raise FileNotFoundError(f"Imported file '{imported_file}' not found at '{imported_file_path}' current file path is '{file_path}'")

                visit_proto_file(imported_file_path)

    visit_proto_file(proto_file_path)
    return visited_files

# 创建目标目录
Path(target_dir).mkdir(parents=True, exist_ok=True)

# 遍历源目录中的所有 .proto 文件
for root, _, files in os.walk(source_dir):
    for file in files:
        if file.endswith(".proto"):
            # 获取 .proto 文件的绝对路径
            proto_file_abs_path = os.path.join(root, file)

            # 获取所有相关的 .proto 文件（包括当前文件和所有导入的文件）
            related_proto_files = get_proto_files_recursively(proto_file_abs_path, source_dir)
            print("\n\n")
            print(related_proto_files)
            print("///////////////////////////////")

            proto_file_count += 1 # 增加文件计数器

            # 创建目标目录结构
            proto_file_rel_path = os.path.relpath(proto_file_abs_path, source_dir)
            target_proto_file_abs_path = os.path.join(target_dir, proto_file_rel_path)
            target_proto_file_abs_dir = os.path.dirname(target_proto_file_abs_path)
            Path(target_proto_file_abs_dir).mkdir(parents=True, exist_ok=True)

            # 执行 pbjs 命令
            js_output_file = target_proto_file_abs_path.replace(".proto", ".js")
            pbjs_cmd = f'pbjs -t static-module -w es6 --no-delimited --no-create --no-verify --no-delimited --no-convert -o {js_output_file} {" ".join(related_proto_files)}'
            # subprocess.run(pbjs_cmd, shell=True, check=True)
            try:
                result = subprocess.run(pbjs_cmd, shell=True, check=True, capture_output=True, text=True)
            except subprocess.CalledProcessError as e:
                print("***********************")
                print(e.stderr)
                print("***********************")
                with open(error_log_file, 'a') as f:
                    f.write(f"Stderr: {proto_file_abs_path}\n related_files:{related_proto_files}\n{e.stderr}\n\n") 
                error_count += 1  # 增加错误计数器
                continue

            # 执行 pbts 命令
            ts_output_file = js_output_file.replace(".js", ".d.ts")
            pbts_cmd = f'pbts -o {ts_output_file} {js_output_file}'
            # subprocess.run(pbts_cmd, shell=True, check=True)
            try:
                result = subprocess.run(pbts_cmd, shell=True, check=True, capture_output=True, text=True)
            except subprocess.CalledProcessError as e:
                print("***********************")
                print(e.stderr)
                print("***********************")
                with open(error_log_file, 'a') as f:
                    f.write(f"Stderr: {proto_file_abs_path}\n related_files:{related_proto_files}\n{e.stderr}\n\n") 
                error_count += 1  # 增加错误计数器

# 在文件末尾写入最终的错误数量
with open(error_log_file, 'a') as f:
    f.write(f"Total errors: {error_count}\n Total file:{proto_file_count}")