from django.shortcuts import render, redirect
from django.contrib import messages
import requests
# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EC%98%A8%EB%9D%BC%EC%9D%B8+%EC%A0%84%EC%8B%9C%ED%9A%8C'


def reset_exhibitions(request):
    response = requests.get(url)
    if response.status_code == 200:

        driver = webdriver.Chrome(
            'C:\\Users\\realp\\PycharmProjects\\project-arta-django\\exhibition\\chromedriver.exe')
        driver.implicitly_wait(10)
        driver.get(url)
        driver.implicitly_wait(10)
        next_btn = driver.find_element_by_xpath('//*[@id="main_pack"]/div[3]/div[2]/div/div/div[3]/div/a[2]')
        # driver.execute_script("arguments[0].click();", next_btn)
        page = driver.find_element_by_xpath('//*[@id="main_pack"]/div[3]/div[2]/div/div/div[3]/div/span/span[3]').text
        driver.implicitly_wait(10)

        for i in range(int(page)):
            driver.implicitly_wait(10)
            # items = driver.find_elements_by_class_name('card_item')
            items = driver.find_element_by_xpath('//*[@id="mflick"]/div/div/div/div/div[1]')
            driver.implicitly_wait(10)
            title = items.find_element_by_xpath(
                '//*[@id="mflick"]/div/div/div/div/div[1]/div[1]/div/div[1]/div/strong/a').text
            driver.implicitly_wait(10)
            # for item in items:
                # title = item.find_element_by_class_name('title').text
                # title = item.find_element_by_xpath('//*[@id="mflick"]/div/div/div/div/div[1]/div[1]/div/div[1]/div/strong/a').text
                # driver.implicitly_wait(2)
                # date = item.find_element_by_tag_name('dd').text
                # driver.implicitly_wait(10)
                #     reserve = item.find_element_by_class_name('button_area').find_element_by_tag_name('a')[0].text
                # print(f'{title}')
            print(f'{title}')
            driver.implicitly_wait(10)
            next_btn.send_keys(Keys.ENTER)
            driver.implicitly_wait(10)





        # html = response.text
        # soup = BeautifulSoup(html, 'html.parser')
        # items = soup.find_all('div', attrs={'class': 'card_item'})
        # page = soup.select_one('.pgs > span.npgs > span._total').text
        # print(page)
        # for item in items:
        #     title = item.find('div', attrs={'class': 'title'}).find('a').text
        #     date = item.find('div', attrs={'class': 'info'}).find('dd', attrs={'class': 'no_ellip'}).text
        #     reserve = item.find('div', attrs={'class': 'button_area'}).find('a')['href']
        #     print(f'{title}:{date}:{reserve}')

        # items = driver.find_elements_by_class_name('card_item')
        # driver.implicitly_wait(10)
        # for item in items:
        #     title = item.find_element_by_class_name('title').text
        #     driver.implicitly_wait(10)
        #     date = item.find_element_by_tag_name('dd').text
        #     driver.implicitly_wait(10)
        #         reserve = item.find_element_by_class_name('button_area').find_element_by_tag_name('a')[0].text
            #
            # print(f'{title}:{date}')

        messages.add_message(request, messages.SUCCESS, "리셋 되었습니다.")
    else:
        messages.add_message(request, messages.WARNING, "리셋에 실패하였습니다.")

    return redirect('/info/')
