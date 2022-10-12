from selenium import webdriver
import chromedriver_binary



def scrape_caribbean():
    # Chrome のオプションを設定する
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    print("1"*100)

    # Selenium Server に接続する
    # driver = webdriver.Remote(
    #     command_executor='http://localhost:4442/wd/hub',
    #     desired_capabilities=options.to_capabilities(),
    #     options=options,
    # )
    # driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver',options=options)
    driver = webdriver.Chrome(options=options)
    print("2"*100)
    # Message: 'chromedriver' executable needs to be in PATH. Please see https://chromedriver.chromium.org/home
    # Message: Service chromedriver unexpectedly exited. Status code was: 127
    # Selenium 経由でブラウザを操作する
    driver.get('https://disney.hosuu.jp/syosai_information.php?code=AAL0101')
    print(driver.current_url)
    source = driver.page_source
    print(type(source))
    print(source)

    with open('./caribbean.txt', 'w') as f:
        f.write(source)

    # ブラウザを終了する
    driver.quit()
