import random

from django.shortcuts import render, redirect
from django.contrib import messages
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from .models import Exhibition, ExternalExhibition, ExhibitionMode, Category
from django.shortcuts import get_object_or_404
from random import *


def reset_exhibitions(request):
    online_url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EC%98%A8%EB%9D%BC%EC%9D%B8+%EC%A0%84%EC%8B%9C%ED%9A%8C'
    response = requests.get(online_url)
    categories = Category.objects.all()
    count = Category.objects.count()

    if response.status_code == 200:
        # 드라이버 다운 받아서, 절대 경로로 지정하세요.
        driver = webdriver.Chrome(
            'C:\\Users\\realp\\PycharmProjects\\test\\project-arta-django\\chromedriver.exe')
        driver.implicitly_wait(10)
        driver.get(online_url)
        driver.implicitly_wait(10)

        next_btn = driver.find_element_by_css_selector(
            '#main_pack > div.sc_new.cs_common_module.case_list.color_1._kgs_art_exhibition > div.cm_content_wrap > div > div > div.cm_paging_area._page > div > a.pg_next.on');
        page = driver.find_element_by_xpath('//*[@id="main_pack"]/div[3]/div[2]/div/div/div[3]/div/span/span[3]').text

        for i in range(int(page)):
            items = driver.find_element_by_xpath('//*[@id="mflick"]/div/div/div/div/div[1]')
            title_str = '//*[@id="mflick"]/div/div/div/div/div[{}]/div[1]/div/div[1]/div/strong/a'
            date_str = '//*[@id="mflick"]/div/div/div/div/div[{}]/div[1]/div/div[2]/dl[1]/dd'
            image_str = '//*[@id="mflick"]/div/div/div/div/div[{}]/div[1]/a/img'
            goto_str = '//*[@id="mflick"]/div/div/div/div/div[{}]/div[2]/a'

            for i in range(1, 5, 1):
                try:
                    title = items.find_element_by_xpath(title_str.format(i)).text
                except:
                    break
                date = items.find_element_by_xpath(date_str.format(i)).text
                start_at = date.split('~')[0].rstrip('.')
                start_at = start_at.replace('.', '-')
                end_at = date.split('~')[-1].rstrip('.')
                end_at = end_at.replace('.', '-')
                image_url = items.find_element_by_xpath(image_str.format(i)).get_attribute('src')
                goto_url = items.find_element_by_xpath(goto_str.format(i)).get_attribute('href')

                mode = get_object_or_404(ExhibitionMode, name='온라인')

                categories = list(categories)
                temp = randint(0, count - 1)
                category = categories[temp]

                try:
                    # test = ExternalExhibition.objects.filter(web_url=goto_url)
                    test = get_object_or_404(ExternalExhibition, web_url=goto_url)
                    if test:
                        print(f'{title} >> already exist')
                        pass
                except:
                    explain = '외부 전시회 입니다.'
                    if end_at == '오픈런':
                        temp_exhibition = Exhibition(name=title, start_at=start_at, mode_id=mode.id, explain=explain,
                                                     category=category)
                    else:
                        temp_exhibition = Exhibition(name=title, start_at=start_at, end_at=end_at, mode_id=mode.id,
                                                     category=category, explain=explain)

                    temp_exhibition.save()
                    temp_exhibition_id = get_object_or_404(Exhibition, name=title)
                    temp_external = ExternalExhibition(exhibition_id=temp_exhibition_id.id, web_url=goto_url,
                                                       poster_url=image_url)
                    temp_external.save()

            time.sleep(1)
            next_btn.send_keys(Keys.ENTER)
            time.sleep(1)

        # driver.close()
        driver.quit()
        messages.add_message(request, messages.SUCCESS, "리셋 되었습니다.")
    else:
        messages.add_message(request, messages.WARNING, "리셋에 실패하였습니다.")

    return redirect('/info/')


def get_offline_exhibition():
    offline_url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%A0%84%EC%8B%9C%ED%9A%8C'
    response = requests.get(offline_url)

    if response.status_code == 200:
        # 드라이버 다운 받아서, 절대 경로로 지정하세요.
        driver = webdriver.Chrome(
            'C:\\Users\\realp\\PycharmProjects\\test\\project-arta-django\\chromedriver.exe')
        driver.implicitly_wait(10)
        driver.get(online_url)
        driver.implicitly_wait(10)

        next_btn = driver.find_element_by_xpath('//*[@id="main_pack"]/div[3]/div[2]/div/div/div[3]/div/a[2]').text
        page = driver.find_element_by_xpath('//*[@id="main_pack"]/div[3]/div[2]/div/div/div[3]/div/span/span[3]').text

        for i in range(int(page)):
            items = driver.find_element_by_xpath('//*[@id="mflick"]/div/div/div/div/div[1]')
            title_str = '//*[@id="mflick"]/div/div/div/div/div[{}]/div[1]/div/div[1]/div/strong/a'
            date_str = '//*[@id="mflick"]/div/div/div/div/div[{}]/div[1]/div/div[2]/dl[1]/dd'
            image_str = '//*[@id="mflick"]/div/div/div/div/div[{}]/div[1]/a/img'
            goto_str = '//*[@id="mflick"]/div/div/div/div/div[{}]/div[2]/a'

            for i in range(1, 5, 1):
                date = items.find_element_by_xpath(date_str.format(i)).text
                start_at = date.split('~')[0].rstrip('.')
                start_at = start_at.replace('.', '-')
                end_at = date.split('~')[-1].rstrip('.')
                end_at = end_at.replace('.', '-')
                image_url = items.find_element_by_xpath(image_str.format(i)).get_attribute('src')
                goto_url = items.find_element_by_xpath(goto_str.format(i)).get_attribute('href')

                mode = get_object_or_404(ExhibitionMode, name='오프라인')

                try:
                    test = get_object_or_404(ExternalExhibition, web_url=goto_url)
                    if test:
                        print(f'{title} >> already exist')
                        pass
                except:
                    explain = '설명이 없습니다.'
                    temp_exhibition = Exhibition(name=title, start_at=start_at, end_at=end_at, mode_id=mode.id,
                                                 explain=explain)

                    temp_exhibition.save()
                    temp_exhibition_id = get_object_or_404(Exhibition, name=title)
                    temp_external = ExternalExhibition(exhibition_id=temp_exhibition_id.id, web_url=goto_url,
                                                       poster_url=image_url)
                    temp_external.save()

            time.sleep(1)
            next_btn.send_keys(Keys.ENTER)
            time.sleep(1)

        # driver.close()
        driver.quit()
        messages.add_message(request, messages.SUCCESS, "리셋 되었습니다.")

    else:
        messages.add_message(request, messages.WARNING, "리셋에 실패하였습니다.")

    return redirect('/info/')
