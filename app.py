import base64
import os
import re
import time
import json
import random
import requests
import tkinter as tk

from selenium import webdriver
from urllib.parse import urlparse
from subprocess import CREATE_NO_WINDOW

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Application:

    def __init__(self):
        self.WebUrl = "https://gtacars.net/gta5?q&page=2&filter_dlc=mpluxe2&filter_dlc=mpluxe&filter_dlc=mpheist&filter_dlc=mpchristmas2&filter_dlc=spupgrade&filter_dlc=mplts&filter_dlc=mppilot&filter_dlc=mpindependence&filter_dlc=mphipster&filter_dlc=mpbusiness2&filter_dlc=mpbusiness&filter_dlc=mpvalentines&filter_dlc=mpbeach&filter_dlc=TitleUpdate&sort=price_mp&filter_vehicle_type=car&filter_class=compacts&filter_class=coupe&filter_class=motorcycle&filter_class=sedan&filter_class=sport&filter_class=sport_classic&filter_class=super&filter_class=suv&perPage=60"
        self.saveFolder = "./images/"
        self.jsonFile = "./data/vehicles.json"
        self._driver_start()

    def _driver_start(self):
        start = time.time()

        # UA
        user_agent = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        ]

        UA = user_agent[random.randrange(0, len(user_agent), 1)]

        # ドライバーのオプション設定用
        option = Options()
        option.add_argument('--lang=ja')
        # option.add_argument('--headless')
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-gpu')
        option.add_argument('--log-level=3')
        option.add_argument('--user-agent=' + UA)
        option.add_argument('--disable-extensions')
        option.add_argument('--disable-dev-shm-usage')
        option.add_argument('--use-fake-ui-for-media-stream')
        option.add_argument('--use-fake-device-for-media-stream')
        # option.add_argument('--blink-settings=imagesEnabled=false')
        option.add_experimental_option('useAutomationExtension', False)
        option.add_experimental_option("excludeSwitches", ["enable-logging"])
        option.page_load_strategy = 'eager'

        try:
            service = fs.Service(executable_path=ChromeDriverManager().install())
            service.creation_flags = CREATE_NO_WINDOW
        except Exception as e:

            tk.messagebox.showerror('Error', f'既存のChrome_Driverのバージョンが合っていない又はChrome_Driverがありません。\n {e}')

        else:

            self.driver = webdriver.Chrome(
                service=service,
                options=option
            )

        self.wait = WebDriverWait(driver=self.driver, timeout=120)

        # エラーがおきる可能性があるためTRY
        try:
            print(f'[LOG]{self.WebUrl}' + 'に接続...')
            self.driver.get(self.WebUrl)

        # エラーが起きた時の処理
        except Exception as e:
            print(e)
            print('[ERROR]Driverの起動に失敗しました。')

        else:
            stop = time.time()
            result = stop - start
            print(f'[LOG] アプリケーション起動までの時間：{result}s')

            start = time.time()
            time.sleep(5)
            self._start_GettingDatas()
            stop = time.time()

            result = stop - start
            print(f'[LOG] 処理にかかった時間：{result}s')

    def _start_GettingDatas(self):

        json_data = []

        elements_data = self.driver.find_elements(By.XPATH,"//div[@class='grid gap-4 sm:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4']/div")
        print(len(elements_data))
        vehicleURLList = self._get_all_vehicle_Url(elements_data=elements_data)

        for i in range(len(vehicleURLList)):

            print(vehicleURLList[i])
            self.driver.get(vehicleURLList[i])
            time.sleep(5)

            element_tables = self.driver.find_elements(By.XPATH,'//div/table')

            # KEY INFO ( Class,Maker )
            element_keyinfo = element_tables[0]
            keyinfo_tr = element_keyinfo.find_elements(By.XPATH,'.//tr')
            vehicleClass = keyinfo_tr[2].find_element(By.XPATH,'.//a').text
            vehicleMaker = keyinfo_tr[3].find_element(By.XPATH,'.//a').text


            # PERFORMANCE ( Top Speed )
            # element_performance = element_tables[1]
            # performance_tbody = element_performance.find_elements(By.XPATH,'.//tbody')
            # element_TS_Tr = performance_tbody[1].find_elements(By.XPATH,'.//tr')
            #
            # element_TS_td = element_TS_Tr[1].find_elements(By.XPATH,'.//td')
            # vehicleTopSpeed = element_TS_td[1].find_element(By.XPATH,'.//span').text
            try:
                element_TS = self.driver.find_element(By.XPATH,'//span[contains(text(),"mph")]')

                if element_TS:  # element_TS_tdが空でない場合、要素が存在する
                    vehicleTopSpeed = element_TS.text
                    vehicleTopSpeed = vehicleTopSpeed.replace(' mph','')
                else:
                    vehicleTopSpeed = 0

            except NoSuchElementException:
                vehicleTopSpeed = 0


            # META ( Model ID,Hash )
            # element_meta = element_tables[3]
            # meta_tr = element_meta.find_elements(By.XPATH,'.//tr')
            # element_META_td = meta_tr[3].find_elements(By.XPATH,'.//td')
            # vehicleModelID = element_META_td[1].find_elements(By.XPATH,'.//code').text
            vehicleModelID = self.driver.find_elements(By.XPATH,'//td/code')[0].text

            # vehiclePrice = self.driver.find_elements(By.XPATH,"//span[contains(text(),'$')]")[0].text
            #
            # vehiclePrice = vehiclePrice.replace('$ ','')
            # vehiclePrice = vehiclePrice.replace(',','')

            try:
                vehiclePrice_elements = self.driver.find_elements(By.XPATH, "//span[contains(text(),'$')]")

                if vehiclePrice_elements:
                    vehiclePrice_element = vehiclePrice_elements[0]
                    vehiclePrice = vehiclePrice_element.text
                    vehiclePrice = vehiclePrice.replace('$ ', '')
                    vehiclePrice = vehiclePrice.replace('+ Full Coverage', '')
                    vehiclePrice = vehiclePrice.replace(',', '')
                else:
                    vehiclePrice = 0

            except NoSuchElementException:
                vehiclePrice = 0



            print(f"vehicleModelID: {vehicleModelID}")
            print(f"vehicleClass: {vehicleClass}")
            print(f"vehicleMaker: {vehicleMaker}")
            print(f"vehicleTopSpeed: {vehicleTopSpeed}")
            print(f"vehiclePrice: {vehiclePrice}")

            self._download_vehicle_image(modelId=vehicleModelID)

            # JSONデータを作成（例：ディクショナリ）
            new_data = {
                "model": vehicleModelID,
                "class": vehicleClass,
                "maker": vehicleMaker,
                "price": int(vehiclePrice),
                "topspeed": float(vehicleTopSpeed),
            }

            json_data.append(new_data)

        # JSONデータをJSON文字列に変換
        json_str = json.dumps(json_data, indent=4)  # インデントを追加して可読性を向上させる

        # JSONファイルに書き込む
        with open(self.jsonFile, "w") as json_file:
            json_file.write(json_str)

    print("JSONファイルが生成されました。")



    def _download_vehicle_image(self,modelId):

        element_img = self.driver.find_elements(By.XPATH,'//figure/img')
        if len(element_img) < 2 :
            element_img = self.driver.find_elements(By.XPATH,'//figure/img')[0]
        else:
            element_img = self.driver.find_elements(By.XPATH,'//figure/img')[1]

        img_url = element_img.get_attribute('src')
        response = requests.get(img_url)

        # 画像をフォルダに保存
        filename = os.path.join(self.saveFolder, f"{modelId}.jpg")
        with open(filename, "wb") as file:
            file.write(response.content)

    def _get_all_vehicle_Url(self,elements_data):

        list = []

        for i in range(len(elements_data)):

            # 画像要素
            element_a = elements_data[i].find_element(By.TAG_NAME, 'a')
            list.append(element_a.get_attribute('href'))

        return list


if __name__ == "__main__":
    Application()
