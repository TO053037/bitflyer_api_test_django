from bs4 import BeautifulSoup
import os
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time
from typing import List
import csv


attraction_dic_time = {0: "", 1: "", 2: "スプラッシュマウンテン", 3: "プーさんのハニーハント", 4: "ビッグサンダーマウンテン", 5: "スペース・マウンテン",
                       6: "バス・ライトイヤーのアストロブラスター", 7: "モンスターズ・インクライド&ゴーシーク!", 8: "空飛ぶダンボ", 9: "ピータパン空の旅", 10: "ホーンテッドマンション",
                       11: "ピノキオの冒険旅行", 12: "白雪姫と七人のこびと", 13: "イッツ・ア・スモールワールド", 14: "", 15: "キャッスルカルーセル",
                       16: "ミッキーのフィルハーマジック", 17: "シンデレラのフェアリーテイル・ホール", 18: "スターツアーズ", 19: "スティッチ・エンカウンター", 20: "オムニバス",
                       21: "カリブの海賊", 22: "ジャングルクルーズ", 23: "ウエスタンリバー鉄道", 24: "", 25: "ウエスタンランド・シューティングギャラリー",
                       26: "カントリーベア・シアター", 27: "トムソーヤ島いかだ", 28: "ブーバーブラザーズのカヌー探検", 29: "スイスファミリー・ツリーハウス",
                       30: "ガジェットのゴーコースター", 31: "ロジャーラビットのカートゥーンスピン", 32: "グーフィーのペイント&プレイハウス", 33: "ミニーの家", 34: "ドナルドのボート",
                       35: "チップとデールのツリーハウス", }

attraction_dic = {0: "", 1: "", 2: "スプラッシュマウンテン", 3: "プーさんのハニーハント", 4: "ビッグサンダーマウンテン", 5: "スペース・マウンテン",
                  6: "バズ・ライトイヤーのアストロブラスター", 7: "モンスターズ・インク\"ライド&ゴーシーク!\"", 8: "空飛ぶダンボ", 9: "ピーターパン空の旅", 10: "ホーンテッドマンション",
                  11: "ピノキオの冒険旅行", 12: "白雪姫と七人のこびと", 13: "イッツ・ア・スモールワールド", 14: "", 15: "キャッスルカルーセル",
                  16: "ミッキーのフィルハーマジック", 17: "シンデレラのフェアリーテイル・ホール", 18: "スターツアーズ", 19: "スティッチ・エンカウンター", 20: "オムニバス",
                  21: "カリブの海賊", 22: "ジャングルクルーズ", 23: "ウエスタンリバー鉄道", 24: "", 25: "ウエスタンランド・シューティングギャラリー",
                  26: "カントリーベア・シアター", 27: "トムソーヤ島いかだ", 28: "ビーバーブラザーズのカヌー探検", 29: "スイスファミリー・ツリーハウス",
                  30: "ガジェットのゴーコースター", 31: "ロジャーラビットのカートゥーンスピン", 32: "グーフィーのペイント＆プレイハウス", 33: "ミニーの家", 34: "ドナルドのボート",
                  35: "チップとデールのツリーハウス", }

# ウエスタンランド・シューティングギャラリーとミニーの家とドナルドのボートとチップとデールのツリーハウスは-1にしてある
# カントリーベア・シアターは15分から17分、季節ごとのショーにより異なる
# トムソーヤ島いかだは1.5 ~ 3分
attraction_dic_riding = {0: 8, 1: 1.5, 2: 10, 3: 4.5, 4: 4, 5: 3, 
                         6: 4, 7: 4, 8: 1.5, 9: 2.5, 10: 15, 
                         11: 2, 12: 2.5, 13: 10, 14: 1.5, 15: 2, 
                         16: 16, 17: 8, 18: 4.5, 19: 12, 20: 6, 
                         21: 15, 22: 10, 23: 15, 24: 10, 25: -1,
                         26: 17, 27: 3, 28: 10, 29: 8.5, 
                         30: 1, 31: 3.5, 32: 1.5, 33: -1, 34: -1,
                         35: -1, }


def make_driver():
    # Firefox のオプションを設定する
    options = FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Selenium Server に接続する
    driver = webdriver.Firefox(
        # executable_path='./Disney/geckodriver',
        executable_path='./geckodriver',
        options=options,
    )
    return driver


def create_xpath_by_a(index: int) -> str:
    return '/html/body/div[3]/div[1]/article/table[2]/tbody/tr[' + str(index + 2) + ']/td[2]/a'

def create_xpath_by_td(index: int) -> str:
    return '/html/body/div[3]/div[1]/article/table[2]/tbody/tr[' + str(index + 2) + ']/td[1]'


def scraping_distance_source_urls(attractions_num: int) -> List[str]:
    urls = ['' for _ in range(attractions_num)]
    driver = make_driver()
    driver.get('https://disney.hosuu.jp/syosai_information.php?code=ACC0101')
    for i in range(47):
        attraction_name = driver.find_element(
            by='xpath', value=create_xpath_by_a(i)).text
        print(attraction_name)
        for j, v in attraction_dic.items():
            if v == attraction_name:
                urls[j] = driver.find_element(
                    by='xpath', value=create_xpath_by_a(i)).get_attribute('href')
                break

    urls[2] = 'https://disney.hosuu.jp/syosai_information.php?code=ACC0101'
    driver.quit()
    urls_file = open('source_distance.txt', 'w')
    for url in urls:
        urls_file.write(url)
        urls_file.write('\n')
    urls_file.close()
    return urls


def create_between_attractions_distance_csv_file() -> None:
    attraction_num = len(attraction_dic.keys())
    distance_list = [[-1 for _ in range(attraction_num)]
                     for _ in range(attraction_num)]
    source_urls = scraping_distance_source_urls(attraction_num)
    for i in range(attraction_num):
        if source_urls[i] == '':
            continue
        driver = make_driver()
        driver.get(source_urls[i])
        for j in range(47):
            try:
                to_attraction_name = driver.find_element(
                    by='xpath', value=create_xpath_by_a(j)).text
                for k, v in attraction_dic.items():
                    if v == to_attraction_name:
                        distance_str = driver.find_element(
                            by='xpath', value=create_xpath_by_td(j)).text
                        distance = int(distance_str[:-2])
                        distance_list[i][k] = distance
                        break
            except:
                print(i, j)
        driver.quit()
        print(distance_list[i])
        time.sleep(3)
    for i in range(attraction_num):
        distance_list[i][i] = 0
    print('------------------------------------------------')
    for distances in distance_list:
        print(distances)
    with open('attractions_distances.csv', 'w') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerows(distance_list)


if __name__ == '__main__':
    create_between_attractions_distance_csv_file()

def scraping_wait_time_data(year: int, month: int, day: int) -> List[List[int]]:
    driver = make_driver()
    m = str(month)
    d = str(day)
    if len(m) == 1:
        m = '0' + m
    if len(d) == 1:
        d = '0' + d
    date_str = str(year) + m + d

    driver.get('https://urtrip.jp/tdl-past-info/?rm=' + date_str + '#cal')
    print('access' + date_str)

    wait_time_list = []
    xpath_list = [
        '//*[@id="post-62757"]/article/div[2]/div/div[3]/table/tbody/tr',
        '//*[@id="post-62757"]/article/div[2]/div/div[4]/table/tbody/tr',
        '//*[@id="post-62757"]/article/div[2]/div/div[5]/table/tbody/tr',
        '//*[@id="post-62757"]/article/div[2]/div/div[6]/table/tbody/tr',
        '//*[@id="post-62757"]/article/div[2]/div/div[7]/table/tbody/tr',
    ]

    for i in range(48):
        wait_times = []
        for j in range(5):
            wait_times += driver.find_element(
                by='xpath', value=xpath_list[j] + '[' + str(i + 2) + ']').text.split()[1:]
        wait_time_list.append(wait_times)

    for i in range(len(wait_time_list)):
        for j in range(len(wait_time_list[i])):
            try:
                wait_time_list[i][j] = int(wait_time_list[i][j])
            except:
                wait_time_list[i][j] = -1

    with open('wait_time_data_' + date_str.csv, 'w') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerows(wait_time_list)
    print(len(wait_time_list))
    print(len(wait_time_list[0]))
    return wait_time_list

    # xpath_1 = '//*[@id="post-62757"]/article/div[2]/div/div[3]/table/tbody/tr'
    # for i in range(48):
    #     list = driver.find_element(by='xpath', value=xpath_1 + '[' + str(i + 1) + ']')
    #     print(list.text)

    # print('-------------------------------------------------------------------------')

    # xpath_2 = '/html/body/div[1]/div/div/div/div/div[1]/div/div/article/div[2]/div/div[4]/table/tbody/tr'
    # for i in range(10):
    #     list = driver.find_element(by='xpath', value=xpath_2 + '[' + str(i + 1) + ']')
    #     print(list.text)

    # print('-----------------------------------------------------------------------')

    # xpath_3 = '//*[@id="post-62757"]/article/div[2]/div/div[5]/table/tbody/tr'
    # for i in range(1):
    #     list = driver.find_element(by='xpath', value=xpath_3 + '[' + str(i + 1) + ']')
    #     print(list.text)
    # print('---------------------------------------------------------------------------')

    # xpath_4 = '//*[@id="post-62757"]/article/div[2]/div/div[6]/table/tbody/tr'
    # for i in range(1):
    #     list = driver.find_element(by='xpath', value=xpath_4 + '[' + str(i + 1) + ']')
    #     print(list.text)

    # print('---------------------------------------------------------------------------')

    # xpath_5 = '//*[@id="post-62757"]/article/div[2]/div/div[7]/table/tbody/tr'
    # for i in range(1):
    #     list = driver.find_element(by='xpath', value=xpath_5 + '[' + str(i + 1) + ']')
    #     print(list.text)

    driver.quit()


def scrape_caribbean():
    # Selenium 経由でブラウザを操作する
    driver = make_driver()
    driver.get('https://disney.hosuu.jp/syosai_information.php?code=AAL0101')
    source = driver.page_source

    with open('./Disney/data/caribbean.txt', 'w') as f:
        f.write(source)

    # ブラウザを終了する
    driver.quit()


def bs_caribbean():
    data = []
    with open('./Disney/data/caribbean.txt', 'r') as f:
        while True:
            data.append(f.readline())
            if data[-1] == "":
                break
    data = data[75]

    soup = BeautifulSoup(data, 'lxml')
    selector_1 = '.hosuu_col1'
    selector_2 = '.bold'
    meters = [x.get_text() for x in soup.select(selector_1)]
    names = [x.get_text() for x in soup.select(selector_2)]

    with open('./Disney/data/caribbean_meter.txt', 'w') as f:
        for t in meters:
            f.write(t + '\n')

    with open('./Disney/data/caribbean_names.txt', 'w') as f:
        for t in names:
            f.write(t + '\n')


def source_attractions():
    res = requests.get('https://disney.hosuu.jp/attractions.php')

    with open('./Disney/data/attractions.txt', 'w') as f:
        f.write(res.text)


def bs_attractions_urls():
    data = ''
    with open('./Disney/data/attractions.txt', 'r') as f:
        data = f.readlines()[48]

    soup = BeautifulSoup(data, 'lxml')
    selector = 'a[href]'
    # with open('./Disney/data/attractions_urls', 'w') as f:
    #     for x in soup.select(selector):
    #         f.write(x.get_text() + '\n')
    urls = [x.get('href') for x in soup.select(selector)]

    with open('./Disney/data/attractions_urls', 'w') as f:
        i = 0
        for t in urls:
            if i % 2 == 0:
                f.write(t + '\n')
            i += 1


def bs_attractions_names():
    data = ''
    with open('./Disney/data/attractions.txt', 'r') as f:
        data = f.readlines()[48]

    soup = BeautifulSoup(data, 'lxml')
    selector = 'a'
    print(soup.findAll("a"))
    with open('./Disney/data/attractions_names', 'w', newline='\n') as f:
        i = 0
        for x in soup.findAll("a"):
            if i % 2 == 0:
                f.write(x.get_text() + '\n')
            i += 1
        #     print(x.contents)
        # f.write(soup.string)


def selenium_attractions():
    driver = make_driver()

    names = []
    urls = []
    with open('./Disney/data/attractions_names', 'r') as f:
        names = [line[:-1] for line in f.readlines()]
    with open('./Disney/data/attractions_urls', 'r') as f:
        urls = [line[:-1] for line in f.readlines()]

    for i in range(40):
        driver.get('https://disney.hosuu.jp/' + urls[i])
        source = driver.page_source
        with open('./Disney/data/attractions_source/' + names[i] + '.txt', 'w') as f:
            f.write(source)

    driver.quit()


def test1():
    dirPath = "./Disney/data/attractions_source"
    files = [f for f in os.listdir(dirPath)]
    print(files)


def bs_attractions_meter_and_to():
    dirPath = "./Disney/data/attractions_source"
    file_names = [f for f in os.listdir(dirPath)]
    for fn in file_names:
        data = ''
        with open(dirPath + '/' + fn, 'r') as f:
            for i in range(82):
                f.readline()
            data = f.readline()

        soup = BeautifulSoup(data, 'lxml')
        selector_1 = '.hosuu_col1'
        selector_2 = '.bold'
        meter = [x.get_text() for x in soup.select(selector_1)]
        to = [x.get_text() for x in soup.select(selector_2)]

        with open('./Disney/data/attractions_meter/' + 'meter_' + fn, 'w') as f:
            for m in meter:
                f.write(m + '\n')
        with open('./Disney/data/attractions_to/' + 'to_' + fn, 'w') as f:
            for t in to:
                f.write(t + '\n')


def selenium_attractions_1001():
    driver = make_driver()
    # driver.get('https://disneyreal.asumirai.info/realtime/disneyland-wait-2022-10-1.html')
    driver.get('https://urtrip.jp/tdl-past-info/?rm=20220701')
    source = driver.page_source
    driver.quit()

    with open('./Disney/wait_time/attractions_1001.txt', 'w') as f:
        f.writelines(source)


def selenium_crowding():
    driver = make_driver()
    driver.get(
        'https://disneyreal.asumirai.info/history/disneyland-crowd-calendar.html#current')
    source = driver.page_source
    driver.quit()

    with open('./Disney/wait_time/crowding.txt', 'w') as f:
        f.writelines(source)
