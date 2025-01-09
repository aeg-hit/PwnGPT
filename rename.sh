#!/bin/bash


rename_files() {
    for file in "$1"/*; do
        if [ -f "$file" ]; then

            base=$(basename "$file")
            dir=$(dirname "$file")
            parent_dir=$(basename "$dir")
            grand_parent_dir=$(basename "$(dirname "$dir")")


            if [[ "$base" == result* ]]; then

                result_number=$(echo "$base" | grep -oP '(?<=result_)\d+')

                new_name="result_${result_number}_${parent_dir}_${grand_parent_dir}"

                if [[ "$base" =~ try ]]; then
                    try_part=$(echo "$base" | grep -oP '(?<=try_)\d+')
                    new_name="${new_name}_try_$try_part"
                fi

                ext="${file##*.}"
                new_file="$dir/$new_name.$ext"

                count=1
                while [ -e "$new_file" ]; do
                    new_file="$dir/${new_name}_$count.$ext"
                    ((count++))
                done

                mv "$file" "$new_file"
                echo "Renamed '$file' to '$new_file'"
            fi
        elif [ -d "$file" ]; then
            rename_files "$file"
        fi
    done
}


rename_files .
# move
# find . -type f -name "result_*" | xargs -I {} mv {} ./result/old/