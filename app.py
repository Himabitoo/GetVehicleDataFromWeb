import os
import time
import json
import random
import tkinter as tk

from selenium import webdriver
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
        self._get_element_container_of_vehicle_data()

    def _get_element_container_of_vehicle_data(self):

        elements_data = self.driver.find_elements(By.XPATH,"//div[@class='grid gap-4 sm:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4']/div")
        # print(f"{len(elements_data)}")



    # def _get_element_

if __name__ == "__main__":
    Application()
