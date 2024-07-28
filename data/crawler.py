from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime
import os
import re
import time
from time import sleep
import random
import urllib.request
import requests



def scroll_down():
    for i in range(3):
        # 또는 Keys.END를 사용하여 페이지 아래로 스크롤하기
        body = driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.END)
        time.sleep(1)


def convert_seconds(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return hours, minutes, seconds

# 이미지 다운로드 함수
def download_image(image_url, save_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        
    else:
        print(f"이미지 다운로드 실패: {image_url}")
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


# Setting
# 크롬 드라이버 다운로드 및 자동 설정
chrome_driver_path = ChromeDriverManager().install()

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 불필요한 에러 메시지 삭제
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# jente store 남성 상의 파트

genders = ['0001', '0002']
categories = ['000200010003', '000100010003']

url = 'https://jentestore.com/goods/list?gender=0001&category[]=000100010003&per=24&page=1&sort=sale&imageSize=medium&type[]=category&type[]=brand&type[]=color&type[]=size&type[]=logistics'

# Open Chrome driver
print("Open Driver")
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)
driver.maximize_window()

time.sleep(3)
print("Driver Opened\n\n")


# 크롤링 시작 시간 기록
start_time = time.time()


for gender, cateogry in zip(genders, categories):
    url=f'https://jentestore.com/goods/list?gender={gender}&category[]={cateogry}&per=24&page=1&sort=sale&imageSize=medium&type[]=category&type[]=brand&type[]=color&type[]=size&type[]=logistics'
    driver.get(url)

    start = 0
    scroll_down()
    time.sleep(1)
    goods_lists = driver.find_elements(By.CSS_SELECTOR, ".jt-goods-list-elem")

    for i, goods in enumerate(goods_lists[start:]):
        try:
            brand_name = goods.find_element(By.CSS_SELECTOR, ".goods-brand")
            goods_name = goods.find_element(By.CSS_SELECTOR, ".goods-name")
            brand_product_name = brand_name.text + "_" + goods_name.text
            # print(brand_product_name)
        except Exception as e:
            print(f"오류가 발생했습니다: {e}")

        try:
            image_element = goods.find_element(By.CSS_SELECTOR, "img")
            # 이미지 URL 가져오기
            image_url = image_element.get_attribute('src')
            time.sleep(1)

            # 이미지 저장 경로 설정
            save_folder = f"images/{gender}"
            os.makedirs(save_folder, exist_ok=True)
            
            image_name = os.path.basename(brand_product_name + '.jpg')
            save_path = os.path.join(save_folder, image_name)

            # 이미지 다운로드
            download_image(image_url, save_path)
        except Exception as e:
            print(f"오류가 발생했습니다: {e}")

        time.sleep(1)

    

print()
print("====================================================  Done  ============================================================")
print()
for _ in range(2):
    print("========================================================================================================================")
print()
print()

# 크롤링 종료 시간 기록
end_time = time.time()
# 크롤링 소요 시간 계산
elapsed_time = end_time - start_time
hours, minutes, seconds = convert_seconds(elapsed_time)
# 결과 출력
print("크롤링 소요 시간: {}시간 {}분 {}초\n".format(int(hours), int(minutes), int(seconds)))


# 마지막 탭 닫기
driver.close()