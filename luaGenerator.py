import os
import json
import tkinter as tk

############## -- config -- ##############

# Setting of Price
doFold = True
intFold = 56

templateVehicle = '''
['#vehicleHash'] = {
    ['name'] = '#vehicleName',
    ['brand'] = '#vehicleBrand',
    ['model'] = '#vehicleModel',
    ['price'] = #vehiclePrice,
    ['category'] = '#vehicleCategory',
    ['categoryLabel'] = '#vehicleCL',
    ['hash'] = `#vehicleHash`,
    ['shop'] = '#vehicleShop',
},\n
'''

# 売る場所のの設定
shopPDM = [ 'compacts', 'coupes', 'suvs', 'sedans', 'sportsclassics', 'muscle',]
shopLUXURY = ['sports', 'super', ]
shopHelicopters = [ 'heli' ]

##########################################

jsonFolderPath = './data/json/'
luaFolderPath = './data/lua/'

# フォルダ内のすべてのファイルを取得
all_files = os.listdir(jsonFolderPath)

# JSONファイルのみを抽出
json_files = [os.path.join(jsonFolderPath, file) for file in all_files if file.endswith(".json")]


for i in range(len(json_files)):

    newTemplateList = []
    
    json_file = json_files[i]
    file_name_without_extension = os.path.splitext(json_file)[1]

    # 既存の JSON ファイルを読み込む
    with open(json_file, "r",encoding='utf-8') as jf:
        existing_data = json.load(jf)

    for item in existing_data:

        # 修正なしでとりあえず取得
        vehicleName = item['name']
        vehicleBrand = item['brand']
        vehicleModel = item['model']
        vehiclePrice = item['price']
        vehicleCategory = item['class']
        vehicleCategoryLabel = item['class']
        vehicleHash = item['model']
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

            case "Muscle":
                vehicleCategory = "muscle"

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

            case "Supers":
                vehicleCategory = "super"
            
            # case "Helicopters"
            #     vehicleCategory = "heli"

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
                vehicleCategoryLabel = "Compacts"

            case "coupes":
                vehicleCategoryLabel = "Coupes"

            case "cycles":
                vehicleCategoryLabel = "Cycles"

            case "motorcycles":
                vehicleCategoryLabel = "Motorcycles"

            case "offroad":
                vehicleCategoryLabel = "Off Road"

            case "muscle":
                vehicleCategoryLabel = "Muscle"

            case "suvs":
                vehicleCategoryLabel = "SUVs"

            case "sedans":
                vehicleCategoryLabel = "Sedans"

            case "sportsclassics":
                vehicleCategoryLabel = "Sports Classics"

            case "sports":
                vehicleCategoryLabel = "Sports"

            case "super":
                vehicleCategoryLabel = "Super"

            case _:
                vehicleCategoryLabel = "NO-FOUND"

            # case "Emergency":
            #     vehicleCategoryLabel = "coupes"
            #
            # case "Coupes":
            #     vehicleCategoryLabel = "coupes"
            # case "Coupes":
            #     vehicleCategoryLabel = "coupes"

        if vehicleCategory in shopPDM:
            vehicleShop = 'pdm'
        elif vehicleCategory in shopLUXURY:
            vehicleShop = 'luxury'
        else:
            vehicleShop = '??'

        # 置き換え
        copyTemplate = templateVehicle

        newTemplate = copyTemplate.replace('#vehicleName',vehicleName)
        newTemplate = newTemplate.replace('#vehicleHash',vehicleHash)
        newTemplate = newTemplate.replace('#vehicleBrand',vehicleBrand)
        newTemplate = newTemplate.replace('#vehicleModel',vehicleModel)
        newTemplate = newTemplate.replace('#vehiclePrice',str(vehiclePrice))
        newTemplate = newTemplate.replace('#vehicleCategory',vehicleCategory)
        newTemplate = newTemplate.replace('#vehicleCL',vehicleCategoryLabel)
        newTemplate = newTemplate.replace('#vehicleShop',vehicleShop)
        newTemplate = newTemplate.replace('\xe4','')


        print(newTemplate)
        print("\n")

        newTemplateList.append(newTemplate)

    # 書き込み
    with open(f"{luaFolderPath}vehicles.lua","a") as luafile:
        for i in range(len(newTemplateList)):
            luafile.write(newTemplateList[i])