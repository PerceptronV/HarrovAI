import os
import json
import time
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from pdfloader import conv2text, merge_texts
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def checkpath(path):
    paths = path.split('\\')
    while '' in paths:
        paths.remove('')
    for i in range(1, len(paths)+1):
        p = '\\'.join(paths[:i])
        if not os.path.exists(p):
            os.mkdir(p)


def download_pdfs(path, driver, overwrite=False):
    checkpath(path)

    html = driver.find_element_by_id('gridTable').get_attribute('innerHTML')
    soup = BeautifulSoup(html, 'html.parser')
    results = list(soup.find('tbody', {'id': 'searchResults'}).children)
    url_2_fname = {}
    urls = []
    pages = []

    for e, i in enumerate(results):
        url_w_pg = 'https://theharrovian.org' + list(list(i.children)[1].children)[1]['href']
        page = int(url_w_pg.split('#')[-1][5:]) - 1
        url = url_w_pg.split('#')[0]

        if url not in urls:
            urls.append(url)
            url_2_fname[url] = f'src_{e}.pdf'

        pages.append([url_2_fname[url], page])

        json.dump({"Urls": urls, "Pages": pages}, open(path + 'log.json', 'w'))

    print('Downloading PDFs...')
    for i in tqdm(urls):
        fpath = path + url_2_fname[i]
        if overwrite or not os.path.exists(fpath):
            open(fpath, 'wb').write(requests.get(i).content)

    time.sleep(1)
    print('Converting PDFs to text...')
    conv2text(path, 'txt\\')
    merge_texts(path + 'txt\\')


def evoke(driver_path: str, save_path='Data\\', param_path='SearchConfig.json',
          login_url='https://theharrovian.org/Account/Login', base_url='https://theharrovian.org/Search'):

    params = json.load(open(param_path, 'r'))

    chrome_options = Options()
    for i in params['ChromeOptions']:
        chrome_options.add_argument(i)

    driver = webdriver.Chrome(driver_path, options=chrome_options)
    print('Driver started')

    driver.get(login_url)
    print('Driver landed at login page')

    usn = driver.find_element_by_id('UserName')
    usn.send_keys(input('Username: '))

    pswd = driver.find_element_by_id('Password')
    pswd.send_keys(input('Password: '))

    login_button = driver.find_elements(By.XPATH, '//input')[-1]
    login_button.click()
    print('Logged In')

    driver.get(base_url)
    print('Driver landed at base page\n')

    for search in params['SearchParams']:
        if not search['Done']:
            for i in search['Selections']:
                choice = driver.find_element_by_xpath(
                    "//select[@id='{}']/option[text()='{}']".format(i, search['Selections'][i])
                )
                choice.click()

            driver.find_element_by_id('SearchText').send_keys(search['SearchText'])
            driver.find_element_by_xpath("//input[@id='Radio{}']".format(search['SearchScope']))

            search_button = driver.find_element_by_id('btnSearch')
            search_button.click()
            time.sleep(1)

            driver.find_element_by_xpath("//select[@id='ddlPageSize']/option[text()='200']").click()
            time.sleep(2)

            pages = int(driver.find_element_by_id('lblNavigation').text.split(' of ')[-1])
            if (path := search['SavePath']) is None:
                path = save_path + search['Name'] + '\\'
            checkpath(path)

            for i in range(pages):
                print('Scraping page {}/{}'.format(i+1, pages))
                download_pdfs(path+'Page_{}\\'.format(i), driver)
                driver.find_element_by_id('next').click()
                time.sleep(2)

        print('Search \'{}\' completed\n'.format(search['Name']))

    driver.close()
    driver.quit()
    print("\nData scraping success")
