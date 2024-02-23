import re

def extract_and_replace_methods_with_indentation(source_file_path, destination_file_path):
    # 正则表达式匹配 virtual 方法和它们上方的注释
    method_pattern = re.compile(r'(//.*\n)*\s*virtual\s+((?!~)[^\(]+)\((.*)\);')

    # 读取源文件中的 virtual 方法
    with open(source_file_path, 'r') as source_file:
        content = source_file.read()

    methods_with_comments = method_pattern.findall(content)
    methods_to_insert = []

    for comment, return_type, params in methods_with_comments:
        # 移除 virtual 关键字，添加 override 关键字
        method_definition = f"\t{return_type.strip()}({params.strip()}) override;\n"
        # 如果存在注释，则包含注释，并在每行前加制表符
        if comment:
            indented_comment = '\t' + comment.replace('\n', '\n\t')
            methods_to_insert.append(indented_comment)
        methods_to_insert.append(method_definition)

    # 读取目标文件内容
    with open(destination_file_path, 'r') as destination_file:
        destination_content = destination_file.read()

    # 正则表达式匹配 HmCoreServiceImpl 类定义
    class_pattern = re.compile(r'(class HmCoreServiceImpl final : public HmCoreService::HmCoreService::Service {)(.*?)(};)', re.DOTALL)

    # 替换 HmCoreServiceImpl 类定义中的内容
    new_destination_content = class_pattern.sub(r'\1\n' + ''.join(methods_to_insert) + r'\n\3', destination_content)

    # 写入新内容到目标文件
    with open(destination_file_path, 'w') as destination_file:
        destination_file.write(new_destination_content)

# 使用函数示例
source_file_path = '/Users/axeishmael/HMOS_iOSProject/wxwork_ios/src/mobile_framework/we_dart/wework_service/proto/hm_core_service.grpc.pb.h'
destination_file_path = '/Users/axeishmael/HMOS_iOSProject/wxwork_ios/src/mobile_framework/language_call/rpc_service/hm_core_service_impl.hpp'
extract_and_replace_methods_with_indentation(source_file_path, destination_file_path)