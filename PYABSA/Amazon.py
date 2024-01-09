from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import threading
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from queue import Queue

class Amazon:
    def __init__(self, search, limit, page_visit): # , count_product
        self.search = search
        self.limit = limit
        # self.count_product = count_product
        self.result_queue = Queue()
        self.page_visit = page_visit
        self.s = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.s)
        self.driver.get('https://www.amazon.in/')
        self.un = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="twotabsearchtextbox"]')))
        self.un.send_keys(search)
        time.sleep(2)
        self.un.send_keys(Keys.ENTER)

    def link_collection(self):
        self.driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
        first_page_id = self.driver.current_window_handle
        review = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME,
                                                                                           'a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal')))  # a-size-base.s-underline-text
        reviews = []
        price = []

        for i in review:
            if '₹' not in i.text:
                reviews.append(i)

        for i in review:
            if '₹' in i.text:
                price.append(i.text)
        # price = []

        cnt = 0
        for i in price:
            if cnt % 2 != 0:
                price.append(i)
            cnt += 1

        try:
            title1 = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'a-size-base-plus.a-color-base.a-text-normal')))
        except TimeoutException:
            title1 = []

        try:
            title2 = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'a-size-medium.a-color-base.a-text-normal')))
        except TimeoutException:
            title2 = []

        main_title = title1 if len(title1) > len(title2) else title2

        titles = []
        d = {}
        prices = {}
        for i, j in zip(main_title, reviews):
            x = self.search.lower()
            if ('(Renewed)' not in i.text) or ('WeConnect' not in i.text) or (
                    'Protect+' not in i.text):  # or ('AppleCare' not in i.text)
                d[j] = i.text
                titles.append(i.text)

        for i, j in zip(main_title, price):
            prices[i.text] = j[1:]

        time.sleep(1)
        return d, titles, prices

    def scraping(self, d, limit):  # , count_product
        # j =
        no_of_product = 0
        prod_review = {}
        ratings = {}
        link_of_product = {}
        overall_rating = {}
        for i in d:
            # if no_of_product == self.count_product:
            #     break
            y = d[i]
            self.driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
            self.driver.switch_to.window(self.driver.window_handles[0])
            # driver.switch_to.window(first_page_id)
            i.click()
            time.sleep(2)
            c = self.driver.window_handles[1]
            self.driver.switch_to.window(c)

            link = self.driver.current_url
            link_of_product[y] = link

            time.sleep(6)
            self.driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')

            try:
                all_comments = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'a-link-emphasis.a-text-bold')))
                all_comments.click()
                time.sleep(2)
            except TimeoutException:
                pass

            self.driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
            try:
                box = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'a-dropdown-prompt')))
                for k in box:
                    if k.text == 'All formats':
                        k.click()
            except TimeoutException:
                pass

            try:
                click = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'format-type-dropdown_1')))
                click.click()
                time.sleep(3)
            except TimeoutException:
                pass

            # scrapping views
            e = self.driver.page_source
            x = BeautifulSoup(e, 'html.parser')

            # scraping rating
            h = x.find_all('span', {'class': 'a-size-medium a-color-base'})

            clean = ' '
            for g in h:
                cleaned = g.text.strip()
                if g.text.strip() != '':
                    clean += cleaned[:3]
            overall_rating[y] = cleaned.strip()

            ## scraping review

            t = x.find_all('span', {'class': 'a-size-base review-text review-text-content'})
            reviews = set()
            for l in t:
                reviews.add(l.text.strip())
                if len(reviews) == self.limit:
                    break

            # star ratings
            h = x.find_all('td', {'class': 'a-text-right a-nowrap'})
            rating = {}
            counter = 5
            for rat in h:
                rating['{} Stars'.format(counter)] = rat.text.strip()
                counter -= 1

            ratings[y] = rating

            if len(reviews) != self.limit or len(reviews) < self.limit:
                try:
                    n = 0
                    while len(reviews) != self.limit:
                        try:
                            last = WebDriverWait(self.driver, 5).until(
                                EC.presence_of_element_located((By.CLASS_NAME, 'a-disabled.a-last')))
                            x = last.text
                            if x == 'Next page':
                                break
                        except (TimeoutException, StaleElementReferenceException):
                            review1 = reviews
                            next_ = WebDriverWait(self.driver, 10).until(
                                EC.presence_of_element_located((By.CLASS_NAME, 'a-last')))
                            next_.click()
                            time.sleep(4)
                            self.driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
                            e = self.driver.page_source
                            x = BeautifulSoup(e, 'html.parser')
                            t = x.find_all('div', {'class': 'a-size-base review-text review-text-content'})
                            for l in t:
                                reviews.add(l.text.strip())
                                if len(reviews) == self.limit:
                                    break
                            prod_review[y] = reviews
                            if len(reviews) == len(review1):
                                break
                except TimeoutException:
                    pass
            else:
                prod_review[y] = reviews

            prod_review[y] = reviews
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            no_of_product += 1

        return prod_review, ratings, link_of_product, overall_rating

    def run(self, page_visit):
        review_of_product = []
        ratings_of_product = []
        link_product = []
        price_product = []
        overall_r = []

        for i in range(self.page_visit):
            d, titles, prices = self.link_collection()
            print(titles)
            prod, ratings, links, overall = self.scraping(d, self.limit) # , self.count_product

            review_of_product.append(prod)
            ratings_of_product.append(ratings)
            link_product.append(links)
            price_product.append(prices)
            overall_r.append(overall)

            self.driver.switch_to.window(self.driver.window_handles[0])
            self.driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
            time.sleep(2)
            flag = False
            while flag != True:
                try:
                    next_ = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME,
                                                                                                's-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator')))
                    next_.click()
                    flag = True
                except (TimeoutException, ElementNotInteractableException, ElementClickInterceptedException):
                    self.driver.refresh()
                    time.sleep(3)
                    pass

        self.result_queue.put((review_of_product, price_product, overall_r, ratings_of_product, link_product))
        # return review_of_product, ratings_of_product, link_product, price_product, overall_r

