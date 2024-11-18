#!/bin/bash

# 定义一个函数来处理每个文件
rename_files() {
    for file in "$1"/*; do
        if [ -f "$file" ]; then
            # 获取文件的基本信息
            base=$(basename "$file")
            dir=$(dirname "$file")
            parent_dir=$(basename "$dir")
            grand_parent_dir=$(basename "$(dirname "$dir")")

            # 只处理文件名以 'result' 开头的文件
            if [[ "$base" == result* ]]; then
                # 提取文件名中的数字部分
                result_number=$(echo "$base" | grep -oP '(?<=result_)\d+')

                # 构建新的文件名
                new_name="result_${result_number}_${parent_dir}_${grand_parent_dir}"

                # 如果文件名中包含 'try'，则保留这个部分
                if [[ "$base" =~ try ]]; then
                    try_part=$(echo "$base" | grep -oP '(?<=try_)\d+')
                    new_name="${new_name}_try_$try_part"
                fi

                # 添加原始文件扩展名
                ext="${file##*.}"
                new_file="$dir/$new_name.$ext"

                # 检查是否已经存在相同的新文件名
                count=1
                while [ -e "$new_file" ]; do
                    new_file="$dir/${new_name}_$count.$ext"
                    ((count++))
                done

                # 执行重命名
                mv "$file" "$new_file"
                echo "Renamed '$file' to '$new_file'"
            fi
        elif [ -d "$file" ]; then
            rename_files "$file"
        fi
    done
}

# 开始从根目录处理
rename_files .
# move
# find . -type f -name "result_*" | xargs -I {} mv {} ./result/old/