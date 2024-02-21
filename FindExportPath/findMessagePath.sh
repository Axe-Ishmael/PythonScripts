#!/bin/bash

#在 message_name 输入你想查询的message的name ，输出为定义该message的路径
# 最顶层文件夹路径
top_level_folder="/Users/axeishmael/StudioProjects/api_proto/src/mobile_framework"
# 要搜索的消息名称
message_name="UserInfo"

# 要搜索的特定内容，这里使用正则表达式进行精确匹配
# ^ 表示行的开始，[[:space:]]+ 表示一个或多个空白字符
# search_content="^message[[:space:]]+${message_name}"
search_content="^message[[:space:]]+\b${message_name}\b"

# 使用find命令遍历文件夹下的所有.proto文件
find "$top_level_folder" -type f -name "*.proto" | while read -r file; do
    # 使用grep检查文件内容
    if grep -q -E "$search_content" "$file"; then
        # 输出文件的路径
        echo "$file"
    fi
done
