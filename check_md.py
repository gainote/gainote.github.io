import os
import yaml

def check_front_matter(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if len(lines) < 2 or not (lines[0].strip() == '---' and '---' in lines[1:]):
            return False
        try:
            # 嘗試解析 YAML Front Matter
            yaml.safe_load(''.join(lines[1:lines.index('---\n', 1)]))
            return True
        except yaml.YAMLError:
            return False

def find_invalid_md_files(directory):
    invalid_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                if not check_front_matter(file_path):
                    invalid_files.append(file_path)
    return invalid_files

if __name__ == "__main__":
    invalid_files = find_invalid_md_files('.')
    if invalid_files:
        with open('error_files.txt', 'w') as f:
            for file in invalid_files:
                f.write(f"{file}\n")
        print("以下 Markdown 檔案有問題：")
        for file in invalid_files:
            print(file)
        exit(1)  # 退出並標記為失敗狀態
    else:
        print("所有 Markdown 檔案都符合 Jekyll 規範！")
