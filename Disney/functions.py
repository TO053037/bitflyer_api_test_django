from bs4 import BeautifulSoup
import chromedriver_binary
import os
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions



def scrape_caribbean():
    # Chrome のオプションを設定する
    # options = webdriver.ChromeOptions()
    options = FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Selenium Server に接続する
    # driver = webdriver.Remote(
        # command_executor='http://localhost:4442/wd/hub',
        # desired_capabilities=options.to_capabilities(),
        # options=options,
    # )
    # driver = webdriver.Chrome(options=options)
    driver = webdriver.Firefox(
        executable_path='./Disney/geckodriver',
        options=options,
    )

    # Selenium 経由でブラウザを操作する
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
    # options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    # driver = webdriver.Chrome(options=options)

    # driver.get('view-source:https://disney.hosuu.jp/attractions.php')
    # source = driver.page_source
    res = requests.get('https://disney.hosuu.jp/attractions.php')

    with open('./Disney/data/attractions.txt', 'w') as f:
        # f.write(source)
        f.write(res.text)

    # driver.quit()

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
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

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
