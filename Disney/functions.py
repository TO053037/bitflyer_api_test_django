from bs4 import BeautifulSoup
import os
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time
from typing import List
import csv


def make_driver():
    # Firefox のオプションを設定する
    options = FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Selenium Server に接続する
    driver = webdriver.Firefox(
        executable_path='./Disney/geckodriver',
        # executable_path='./geckodriver',
        options=options,
    )
    return driver


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
            wait_times += driver.find_element(by='xpath', value=xpath_list[j] + '[' + str(i + 2) + ']').text.split()[1:]
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
    driver.get('https://disneyreal.asumirai.info/history/disneyland-crowd-calendar.html#current')
    source = driver.page_source
    driver.quit()

    with open('./Disney/wait_time/crowding.txt', 'w') as f:
        f.writelines(source)


if __name__ == '__main__':
    # scraping_wait_time_data()
    selenium_attractions_1001()
