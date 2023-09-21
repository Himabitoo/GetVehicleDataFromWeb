import os
import time
import json
import random
import requests
import tkinter as tk

from selenium import webdriver
from urllib.parse import urlparse
from subprocess import CREATE_NO_WINDOW
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Application:

    def __init__(self):
        self.WebUrl = "https://gtacars.net/gta5?q&page=1&filter_dlc=mpluxe2&filter_dlc=mpluxe&filter_dlc=mpheist&filter_dlc=mpchristmas2&filter_dlc=spupgrade&filter_dlc=mplts&filter_dlc=mppilot&filter_dlc=mpindependence&filter_dlc=mphipster&filter_dlc=mpbusiness2&filter_dlc=mpbusiness&filter_dlc=mpvalentines&filter_dlc=mpbeach&filter_dlc=TitleUpdate&sort=price_mp&filter_vehicle_type=car&filter_class=compacts&filter_class=coupe&filter_class=motorcycle&filter_class=sedan&filter_class=sport&filter_class=sport_classic&filter_class=super&filter_class=suv&perPage=60"
        self.saveFolder = "./images/"
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
            self._click_pulldown_button()
            self._start_GettingDatas()
            stop = time.time()

            result = stop - start
            print(f'[LOG] 処理にかかった時間：{result}s')

    def _start_GettingDatas(self):
        self._get_element_container_of_vehicle_data()

    def _get_element_container_of_vehicle_data(self):

        elements_data = self.driver.find_elements(By.XPATH,"//div[@class='grid gap-4 sm:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4']/div")

        for i in range(len(elements_data)):

            # 画像要素
            element_a = elements_data[i].find_element(By.TAG_NAME, 'a')
            element_a_img = element_a.find_element(By.TAG_NAME, 'img')
            element_a_span = element_a.find_element(By.TAG_NAME, 'span')

            img_url = element_a_img.get_attribute('src')

            # isDataUrI = self._is_data_uri(img_url)

            # ファイル名を生成（通常は画像のURLから取得します）
            filename = os.path.join(self.saveFolder, f"{element_a_span.text}.jpg")

            # 画像データをダウンロード
            response = requests.get(img_url)

            # 画像をフォルダに保存
            with open(filename, "wb") as file:
                file.write(response.content)




            # # データ要素
            # element_div = elements_data[i].find_element(By.TAG_NAME, 'div')
            # element_div_s = element_div.find_elements(By.TAG_NAME,'div')

            # クラス、ブランド、
            # element_div_info_1 = element_div_s[0]



            # element_div_info_2 = element_div_s[1]
            # element_div_info_3 = element_div_s[2]









    # def _get_element_children_tag_a(self):
    #      element_a = self.driver.
    #     return

    # def _get_element_

    
    def _click_pulldown_button(self):
        element_button = self.driver.find_elements(By.XPATH, '//button[@class="relative flex items-center justify-center gap-2 duration-75 h-6 w-6 rounded-full border border-neutral-200 bg-white hover:bg-neutral-50 active:bg-neutral-200 dark:border-neutral-600 dark:bg-neutral-750 dark:hover:border-neutral-500 dark:active:bg-neutral-800 has-tooltip"]')
        element_button[0].click()
        time.sleep(3)

    def _is_data_uri(url):
        # URLを解析
        parsed_url = urlparse(url)

        # スキームが"data"で始まるかどうかをチェック
        return parsed_url.scheme == "data"

if __name__ == "__main__":
    Application()
