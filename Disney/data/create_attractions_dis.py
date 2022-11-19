from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time
from typing import List
import csv

attraction_dic = {0: "", 1: "", 2: "スプラッシュマウンテン", 3: "プーさんのハニーハント", 4: "ビッグサンダーマウンテン", 5: "スペース・マウンテン",
                  6: "バス・ライトイヤーのアストロブラスター", 7: "モンスターズ・インクライド&ゴーシーク!", 8: "空飛ぶダンボ", 9: "ピータパン空の旅", 10: "ホーンテッドマンション",
                  11: "ピノキオの冒険旅行", 12: "白雪姫と七人のこびと", 13: "イッツ・ア・スモールワールド", 14: "", 15: "キャッスルカルーセル",
                  16: "ミッキーのフィルハーマジック", 17: "シンデレラのフェアリーテイル・ホール", 18: "スターツアーズ", 19: "スティッチ・エンカウンター", 20: "オムニバス",
                  21: "カリブの海賊", 22: "ジャングルクルーズ", 23: "ウエスタンリバー鉄道", 24: "", 25: "ウエスタンランド・シューティングギャラリー",
                  26: "カントリーベア・シアター", 27: "トムソーヤ島いかだ", 28: "ブーバーブラザーズのカヌー探検", 29: "スイスファミリー・ツリーハウス",
                  30: "ガジェットのゴーコースター", 31: "ロジャーラビットのカートゥーンスピン", 32: "グーフィーのペイント&プレイハウス", 33: "ミニーの家", 34: "ドナルドのボート",
                  35: "チップとデールのツリーハウス", }


def open_txt_file(file_path: str) -> str:
    f = open(file_path, 'r', encoding='UTF-8')
    data = f.read()
    f.close()
    return data


def make_driver():
    # Firefox のオプションを設定する
    options = FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Selenium Server に接続する
    driver = webdriver.Firefox(
        executable',
        # executable_path='./geckodriver',
        options=options,
    )
    return driver


def create_source_url_list(attractions_num: int) -> List[str]:
    driver = make_driver()
    driver.get('https://disney.hosuu.jp/syosai_information.php?code=ACC0101')
    url_list = ['' for _ in range(attractions_num)]
    
    print(driver.page_source)
    driver.quit()
    
    return url_list
    

if __name__ == '__main__':
    # attractions_num = 36
    # distance_list = [[-1 for _ in range(attractions_num)] for _ in range(attractions_num))]
    # for i in range(attractions_num):
    #     if attraction_dic[i] == "":
    #         continue
    create_source_url_list(36)