from django.shortcuts import render, redirect
from django.contrib import messages
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EC%98%A8%EB%9D%BC%EC%9D%B8+%EC%A0%84%EC%8B%9C%ED%9A%8C'


def reset_exhibitions(request):
    response = requests.get(url)
    if response.status_code == 200:

        driver = webdriver.Chrome(
            'C:\\Users\\realp\\PycharmProjects\\project-arta-django\\exhibition\\chromedriver.exe')
        driver.implicitly_wait(10)
        driver.get(url)
        driver.implicitly_wait(10)

        next_btn = driver.find_element_by_css_selector('#main_pack > div.sc_new.cs_common_module.case_list.color_1._kgs_art_exhibition > div.cm_content_wrap > div > div > div.cm_paging_area._page > div > a.pg_next.on');
        # next_btn = driver.find_element_by_xpath('//*[@id="main_pack"]/div[3]/div[2]/div/div/div[3]/div/a[2]')
        # driver.execute_script("arguments[0].click();", next_btn)
        page = driver.find_element_by_xpath('//*[@id="main_pack"]/div[3]/div[2]/div/div/div[3]/div/span/span[3]').text
        for i in range(int(page)):
            items = driver.find_element_by_xpath('//*[@id="mflick"]/div/div/div/div/div[1]')

            title = items.find_element_by_xpath(
                '//*[@id="mflick"]/div/div/div/div/div[1]/div[1]/div/div[1]/div/strong/a').text
            title2 = items.find_element_by_xpath(
                '//*[@id="mflick"]/div/div/div/div/div[2]/div[1]/div/div[1]/div/strong/a').text
            title3 = items.find_element_by_xpath(
                '//*[@id="mflick"]/div/div/div/div/div[3]/div[1]/div/div[1]/div/strong/a').text
            title4 = items.find_element_by_xpath(
                '//*[@id="mflick"]/div/div/div/div/div[4]/div[1]/div/div[1]/div/strong/a').text
            print(f'{title}:{title2}:{title3}:{title4}')
            time.sleep(1)
            next_btn.send_keys(Keys.ENTER)
            time.sleep(1)

        # driver.close()
        time.sleep(3)
        driver.quit()
        messages.add_message(request, messages.SUCCESS, "리셋 되었습니다.")
    else:
        messages.add_message(request, messages.WARNING, "리셋에 실패하였습니다.")

    return redirect('/info/')
