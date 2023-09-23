import os
import json
import tkinter as tk

############## -- config -- ##############

# Setting of Price
doFold = True
intFold = 120

templateVehicle = '''
['#vehicleHash'] = {
    ['name'] = '#vehicleName',
    ['brand'] = '#vehicleBrand',
    ['model'] = '#vehicleModel',
    ['price'] = #vehiclePrice,
    ['category'] = '#vehicleCategory',
    ['categoryLabel'] = '#vehicleCategoryLabel',
    ['hash'] = `#vehicleHash`,
    ['shop'] = '#vehicleShop',
},
'''

##########################################

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

        # 修正なしでとりあえず取得
        vehicleName = item['name']
        vehicleBrand = item['brand']
        vehicleModel = item['model']
        vehiclePrice = item['price']
        vehicleCategory = item['class']
        vehicleCategoryLabel = item['class']
        vehicleHash = item['hash']
        vehicleShop = ""

        # luaファイル生成前の代入する値の前処理

        # 価格に倍率をかける場合 (True)
        if doFold:
            if intFold is not None:
                vehiclePrice = vehiclePrice * intFold

            else:
                tk.messagebox.showerror('Error', '倍率が指定する必要があります。')

        # Category 設定
        match vehicleCategoryLabel:
            case "Compacts":
                vehicleCategory = "compacts"

            case "Coupes":
                vehicleCategory = "coupes"

            case "Cycles":
                vehicleCategory = "cycles"

            case "Motorcycles":
                vehicleCategory = "motorcycles"

            case "Off-Road":
                vehicleCategory = "offroad"

            case "SUVs":
                vehicleCategory = "suvs"

            case "Sedans":
                vehicleCategory = "sedans"

            case "Sports Classics":
                vehicleCategory = "sportsclassics"

            case "Sports":
                vehicleCategory = "sports"

            case "Super":
                vehicleCategory = "super"

            # case "Emergency":
            #     vehicleCategory = "coupes"
            #
            # case "Coupes":
            #     vehicleCategory = "coupes"
            # case "Coupes":
            #     vehicleCategory = "coupes"

        # Category Label 設定
        match vehicleCategory:
            case "compacts":
                vehicleCategory = "Compacts"

            case "coupes":
                vehicleCategory = "Coupes"

            case "cycles":
                vehicleCategory = "Cycles"

            case "motorcycles":
                vehicleCategory = "Motorcycles"

            case "offroad":
                vehicleCategory = "Off Road"

            case "suvs":
                vehicleCategory = "SUVs"

            case "sedans":
                vehicleCategory = "Sedans"

            case "sportsclassics":
                vehicleCategory = "Sports Classics"

            case "sports":
                vehicleCategory = "Sports"

            case "super":
                vehicleCategory = "Super"

            # case "Emergency":
            #     vehicleCategory = "coupes"
            #
            # case "Coupes":
            #     vehicleCategory = "coupes"
            # case "Coupes":
            #     vehicleCategory = "coupes"


        # 売る場所のの設定
        shopPDM = [ 'compacts', 'coupes', 'suvs', 'sedans', 'sportsclassics', ]
        shopLuxury = ['sports', 'super', ]

        if vehicleCategory in shopPDM:
            vehicleShop = 'pdm'
        elif vehicleCategory in shopLuxury:
            vehicleShop = 'luxury'
        else:
            vehicleShop = '??'

        # 置き換え
        newTemplate = templateVehicle
        newTemplate.replace('#vehicleHash',vehicleHash)
        newTemplate.replace('#vehicleBrand',vehicleBrand)
        newTemplate.replace('#vehicleModel',vehicleModel)
        newTemplate.replace('#vehiclePrice',vehiclePrice)
        newTemplate.replace('#vehicleCategory',vehicleCategory)
        newTemplate.replace('#vehicleCategoryLabel',vehicleCategoryLabel)
        newTemplate.replace('#vehicleShop',vehicleShop)

        # 書き込み



# templateVehicle = '''
# ['#vehicleHash'] = {
#     ['name'] = '#vehicleName',
#     ['brand'] = '#vehicleBrand',
#     ['model'] = '#vehicleModel',
#     ['price'] = #vehiclePrice,
#     ['category'] = '#vehicleCategory',
#     ['categoryLabel'] = '#vehicleCategoryLabel',
#     ['hash'] = `#vehicleHash`,
#     ['shop'] = '#vehicleShop',
# },
# '''