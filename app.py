import os
import time
import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

class Application:

    def _GetVehicleDataFromWeb(self):

        # ドライバー生成
        self._driver_start()
        self._start_GettingDatas()


    def _driver_start(self):
        self.btnDriverStart['state'] = 'disabled'
        self.btnDriverStart['text'] = 'ログイン中…'
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
        option.add_argument('--headless')
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-gpu')
        option.add_argument('--log-level=3')
        option.add_argument('--user-agent=' + UA)
        option.add_argument('--disable-extensions')
        option.add_argument('--disable-dev-shm-usage')
        option.add_argument('--use-fake-ui-for-media-stream')
        option.add_argument('--use-fake-device-for-media-stream')
        option.add_argument('--blink-settings=imagesEnabled=false')
        option.add_experimental_option('useAutomationExtension', False)
        option.add_experimental_option("excludeSwitches", ["enable-logging"])
        option.page_load_strategy = 'eager'

        try:
            service = fs.Service(executable_path=ChromeDriverManager().install())
            service.creation_flags = CREATE_NO_WINDOW
        except Exception as e:

            tk.messagebox.showerror('Error', f'既存のChrome_Driverのバージョンが合っていない又はChrome_Driverがありません。\n {e}')
            self._kill_threads()

        else:

            self.driver = webdriver.Chrome(service=service,
                                           options=option)

        self.wait = WebDriverWait(driver=self.driver, timeout=120)

        # エラーがおきる可能性があるためTRY
        try:
            print(f'[LOG]{self.login_url}' + 'に接続...')
            self.driver.get(self.login_url)

        # エラーが起きた時の処理
        except Exception as e:
            print(e)
            print('[ERROR]Driverの起動に失敗しました。')
            self._kill_threads()

        else:
            stop = time.time()
            result = stop - start
            print(f'[LOG]アプリケーション起動までの時間：{result}s')

            start = time.time()
            self._login()
            stop = time.time()

            result = stop - start
            print(f'[LOG]ログインまでの時間：{result}s')

if __name__ == "__main__":
    Application()