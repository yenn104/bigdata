from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json
import time

keyWord = 'TUF'

# Khởi tạo trình duyệt
driver = webdriver.Chrome('C:/Users/Admin/Downloads/chromedriver_win32/chromedriver.exe')

# Truy cập trang web cần thao tác
driver.get("https://cellphones.com.vn/")

# Tìm textbox bằng id hoặc class
searchCells = driver.find_element(By.ID ,"inp$earch")
# hoặc
# textbox = driver.find_element_by_class_name("textbox_class")
# Nhập dữ liệu vào textbox
searchCells.send_keys(keyWord)

time.sleep(2)

html = driver.page_source

# Sử dụng BeautifulSoup để parse HTML
soup = BeautifulSoup(html, 'html.parser')

quotes=[]  # a list to store quotes

tableCell = soup.find('div', attrs = {'id':'search_autocomplete'})
if tableCell:
    for row in tableCell.findAll('a',attrs = {'class', 'header-search-item px-1 is-flex is-align-items-center'}):
        quote = {}
        quote['ProductLink'] = row['href']
        quote['ProductName'] = row.find('p',attrs = {'class','header-search-name'}).text
        quote['ProductPrice'] = row.find('p',attrs = {'class','header-search-special mr-1'}).text.strip().replace('.','')
        quote['ProductPriceCurrent'] = row.find('p',attrs = {'class','header-search-price'}).text.strip().replace('.','')
        quote['ProductImg'] = row.find('img')['src']
        quote['URL'] = 'https://cellphones.com.vn/'
        quotes.append(quote)

# Truy cập trang web cần thao tác
driver.get("https://www.thegioididong.com/")
# Tìm textbox bằng id hoặc class
searchTheGioiDiDong = driver.find_element(By.NAME ,"key")
searchTheGioiDiDong.send_keys(keyWord)

time.sleep(2)

html = driver.page_source

# Sử dụng BeautifulSoup để parse HTML
soup = BeautifulSoup(html, 'html.parser')
tableTheGioiDiDong = soup.find('ul', attrs = {'class':'suggest_search'})
if tableTheGioiDiDong:
    for row in tableTheGioiDiDong.findAll('a'):
        quote = {}
        quote['ProductLink'] = 'https://www.thegioididong.com/' + row['href']
        quote['ProductName'] = row['data-name']
        quote['ProductPrice'] = row['data-price'].replace('.','')
        quote['ProductPriceCurrent'] = row.find('p',attrs = {'class','price-old black'}).text.replace('\u20ab','').replace('.','')
        quote['ProductImg'] = row.find('img')['src']
        quote['URL'] = 'https://www.thegioididong.com/'
        quotes.append(quote)


# Truy cập trang web cần thao tác
driver.get("https://gearvn.com/search?type=product&q=" + keyWord)
time.sleep(3)

html = driver.page_source

# Sử dụng BeautifulSoup để parse HTML
soup = BeautifulSoup(html, 'html.parser')
tableGearVN = soup.find('div', attrs = {'class':'results content-page content-product-list product-list'})
if tableGearVN:
    for row in tableGearVN.findAll('div', attrs = {'class','product-row'}):
        quote = {}
        quote['ProductLink'] = 'https://gearvn.com/' + row.a['href']
        quote['ProductName'] = row.h2.text
        quote['ProductPrice'] = row.find('span',attrs = {'class','product-row-sale'}).text.strip().replace('\u20ab','').replace(',','')
        if row.find('del'): 
            quote['ProductPriceCurrent'] = row.find('del').text.replace('\u20ab','').strip().replace(',','')
        else:
            quote['ProductPriceCurrent'] = ''
        quote['ProductImg'] = row.find('img')['src']
        quote['URL'] = 'https://gearvn.com/'
        quotes.append(quote)
# Truy cập trang web cần thao tác
driver.get("https://xgear.net/?s=" + keyWord)
time.sleep(2)

html = driver.page_source

# Sử dụng BeautifulSoup để parse HTML
soup = BeautifulSoup(html, 'html.parser')
tableXgear = soup.find('ul', attrs = {'class':'products elementor-grid columns-4'})
if tableXgear:
    for row in tableXgear.findAll('a',attrs = {'class', 'woocommerce-LoopProduct-link woocommerce-loop-product__link'}):
        quote = {}
        quote['ProductLink'] = row['href']
        quote['ProductName'] = row.h2.text.replace('\u2026','')
        quote['ProductPrice'] = row.find('ins').text.replace('\u00a0','').replace('\u20ab','').replace(',','')
        quote['ProductPriceCurrent'] = row.find('del').text.replace('\u00a0','').replace('\u20ab','').replace(',','')
        quote['ProductImg'] = row.find('img')['src']
        quotes.append(quote)
driver.close()

filename ='Data.json'
with open(filename, 'w') as f:
    json.dump(quotes, f)