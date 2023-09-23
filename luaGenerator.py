import os
import json

jsonFolderPath = './data/'

# フォルダ内のすべてのファイルを取得
all_files = os.listdir(jsonFolderPath)

# JSONファイルのみを抽出
json_files = [os.path.join(jsonFolderPath, file) for file in all_files if file.endswith(".json")]

for json_file in json_files:

    # 既存の JSON ファイルを読み込む
    with open(json_file, "r") as jf:
        existing_data = json.load(jf)

    for item in existing_data:
        vehicleName = item['name']
        vehicleBrand =


templateVehicle = '''
['blista'] = {
    ['name'] = 'Blista',
    ['brand'] = 'Dinka',
    ['model'] = 'blista',
    ['price'] = 1677000,
    ['category'] = 'compacts',
    ['categoryLabel'] = 'Compacts',
    ['hash'] = `blista`,
    ['shop'] = 'pdm',
},
'''