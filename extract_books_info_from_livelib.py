import os
import time
import pandas as pd
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By

load_dotenv()
livelib_username = os.getenv("LIVELIB_USERNAME")
livelib_password = os.getenv("LIVELIB_PASSWORD")
INPUT_LINKS = 'book-links.txt'
OUTPUT_CSV = 'books_info.csv'


def login_livelib(driver, username, password):
    driver.implicitly_wait(20) # in case of redirects on the main page
    driver.maximize_window()
    driver.get("https://www.livelib.ru")
    driver.find_element(By.CLASS_NAME, 'page-header__login').click()
    driver.find_element(By.ID, 'checkin-email').send_keys(username)
    time.sleep(3)  # wait for the button to become clickable
    driver.find_element(By.XPATH, '//button[@onclick="loginform_new_check_email()"]').click()
    driver.find_element(By.NAME, 'user[password]').send_keys(password)
    time.sleep(2) # wait for the next action to become available
    driver.find_element(By.NAME, 'user[submit]').click()
    driver.implicitly_wait(10) # set to the optimal value
    # time.sleep(80) # manual login
    return driver


def save_book_info(driver, book_url):
    print('book_url:', book_url)
    driver.get(book_url)
    book_data = []
    try:
        title = driver.find_element(By.XPATH, '//h1[@class="bc__book-title "]').text
        try:
            author = driver.find_element(By.XPATH, '//a[contains(@class, "bc-author__link")]').text # support multiple authors, returns first
        except:
            author = 'unknown/various'
        rating_string = driver.find_element(By.XPATH, '//a[@class="bc-rating-medium"]').get_attribute(
            'title')  # like "Рейтинг 4.393 (рейтинг ожидания 5.000)"
        global_rating = rating_string.split('(')[0].split(' ')[1]  # assume will keep first number only
        readers_count = driver.find_element(By.XPATH, '//a[@title="Прочитали эту книгу"]/b').text
        driver.find_element(By.XPATH, '//div[@class="bc-menu__wrap"]//a[@href="javascript:void(0);"]').click()
        time.sleep(2)  # wait for popup to load
        user_rating = driver.find_element(By.XPATH, '//span[@class="add-book__my-rating"]').text
        date_read = driver.find_element(By.XPATH, '//button[@name="already-read-date"]').text

        print('title: ', title)
        print('author: ', author)
        print('readers_count: ', readers_count)
        print('global_rating: ', global_rating)
        print('user_rating: ', user_rating)
        print('date_read: ', date_read)
        print('---')
        book_data.append([book_url, title, author, readers_count, global_rating, user_rating, date_read])
        pd.DataFrame(book_data, columns=['book_url', 'title', 'author', 'readers_count', 'global_rating', 'user_rating',
                                         'date_read']).to_csv(OUTPUT_CSV, sep='|', header=None, index=False, mode='a')
    except Exception as e:
        print(f'caught {type(e)}: e')
        print(str(e))
    return driver


if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver = login_livelib(driver, livelib_username, livelib_password)
    with open(INPUT_LINKS, 'r') as file:
        book_urls = file.read().splitlines()
    # write header to csv
    pd.DataFrame([], columns=['book_url', 'title', 'author', 'readers_count', 'global_rating', 'user_rating',
                                     'date_read']).to_csv(OUTPUT_CSV, sep='|', index=False, mode='a')
    for book_url in book_urls:
        driver = save_book_info(driver, book_url)
    driver.quit()
