import os
import json
import requests
from urllib.parse import urlparse

def download_file(url, folder_path):
    local_filename = url.split('/')[-1]
    file_path = os.path.join(folder_path, local_filename)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    return file_path

def process_json(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    if not isinstance(data, list):
        print("JSON数据不是列表格式")
        return

    for item in data:
        kairosoft_link = item.get('KairosoftLink')
        kairosoft_ico = item.get('Kairosoftico')

        if kairosoft_link and kairosoft_ico:
            # 提取xx部分作为子文件夹名
            parsed_url = urlparse(kairosoft_link)
            path_parts = parsed_url.path.strip('/').split('/')
            folder_name = path_parts[-1].replace('.html', '') if path_parts else None

            if folder_name:
                folder_path = os.path.join(os.path.dirname(json_file_path), folder_name)
                os.makedirs(folder_path, exist_ok=True)

                # 下载ICO文件
                ico_file_path = download_file(kairosoft_ico, folder_path)
                print(f"已下载 {kairosoft_ico} 到 {ico_file_path}")
        else:
            print("缺少必要的字段")

if __name__ == "__main__":
    json_file_path = os.path.join(os.getcwd(), '0.json')
    process_json(json_file_path)



