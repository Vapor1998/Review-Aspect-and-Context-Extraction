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


class Flipkart:
    def __init__(self, search, limit, page_visit):  # , count_product
        self.search = search
        self.limit = limit
        self.page_visit = page_visit
        # self.count_product = count_product
        self.result_queue = Queue()
        self.s = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.s)
        self.driver.get('https://www.flipkart.com/')

        try:
            x_button = WebDriverWait(self.driver, 17).until(
                EC.presence_of_element_located((By.CLASS_NAME, '_2KpZ6l._2doB4z')))
            x_button.click()

        except TimeoutException:
            pass
        self.un = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="container"]/div/div[1]/div[1]/div[2]/div[2]/form/div/div/input')))
        self.un.send_keys(self.search)
        time.sleep(2)
        self.un.send_keys(Keys.ENTER)

    def link_collection(self):

        self.driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
        time.sleep(2)

        try:
            review = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, '_1fQZEK')))
            title = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, '_4rR01T')))

        except TimeoutException:
            review = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, '_2rpwqI')))
            title = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 's1Q9rs')))

        titles = []
        d = {}
        reviews = []

        try:
            for i in review:
                if '(' in i.text or '(' not in i.text:
                    reviews.append(i)
        except StaleElementReferenceException:
            self.driver.refresh()
            time.sleep(2)
            self.link_collection()
        try:
            for i, j in zip(title, reviews):
                # x = search.lower()
                if '(Renewed)' not in i.text:
                    d[j] = i.text
                    titles.append(i.text)
        except StaleElementReferenceException:
            self.driver.refresh()
            time.sleep(2)
            self.link_collection()
        # print(d)
        if len(d) == 0:
            self.driver.refresh()
            time.sleep(2)
            self.link_collection()

        time.sleep(1)
        return d

    def scraping(self, d, limit):  # , count_product)
        j = 1
        no_of_product = 0
        prod_review = {}
        link = {}
        overall_rating = {}
        price = {}
        ratings = {}
        for i in d:
            # if no_of_product == self.count_product:
            #     break
            self.driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
            self.driver.switch_to.window(self.driver.window_handles[0])
            i.click()
            time.sleep(2)
            # driver.switch_to.window(driver.window_handles[j])
            c = self.driver.window_handles[1]
            self.driver.switch_to.window(c)

            y = d[i]

            # scraping link
            url = self.driver.current_url
            link[y] = url

            # scraping stars
            e = self.driver.page_source
            x = BeautifulSoup(e, 'html.parser')
            h = x.find_all('div', {'class': '_1uJVNT'})
            stars = {}
            count = 5
            for i in h:
                stars["{} Stars".format(count)] = i.text
                count -= 1

            ratings[y] = stars

            # scraping price   <div class="_30jeq3 _16Jk6d">₹69,999</div>
            e = self.driver.page_source
            x = BeautifulSoup(e, 'html.parser')
            h = x.find_all('div', {'class': '_30jeq3 _16Jk6d'})
            p = []
            for i in h:
                p.append(i.text)
            price[y] = p

            # average ratings
            e = self.driver.page_source
            x = BeautifulSoup(e, 'html.parser')
            h = x.find_all('div', {'class': '_2d4LTz'})
            r = []
            for i in h:
                r.append(i.text)
            overall_rating[y] = r

            # time.sleep(2)
            self.driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
            time.sleep(7)
            try:
                all_comments_link = WebDriverWait(self.driver, 6).until(
                    EC.presence_of_element_located((By.CLASS_NAME, '_3UAT2v._16PBlm')))
                self.driver.execute_script("arguments[0].click();", all_comments_link)

            except TimeoutException:
                pass

            # time.sleep(3)

            # scraping review
            e = self.driver.page_source
            x = BeautifulSoup(e, 'html.parser')

            h = x.find_all('div', {'class': 't-ZTKy'})
            reviews = set()
            # y = d[i]
            for k in h:
                reviews.add(k.text)
                if len(reviews) == limit:
                    break

            if len(reviews) != self.limit or len(reviews) < self.limit:
                try:
                    while len(reviews) != self.limit:
                        review1 = reviews
                        next_page = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_all_elements_located((By.CLASS_NAME, '_1LKTO3')))
                        if len(next_page) == 1:
                            next_page[0].click()
                        elif len(next_page) == 2:
                            next_page[1].click()
                        time.sleep(4)
                        self.driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
                        e = self.driver.page_source
                        x = BeautifulSoup(e, 'html.parser')
                        t = x.find_all('div', {'class': 't-ZTKy'})
                        for l in t:
                            reviews.add(l.text.strip())
                            if len(reviews) == limit:
                                break
                        prod_review[y] = reviews

                except TimeoutException:
                    pass
            else:
                prod_review[y] = reviews

            # prod_review[y] = reviews
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            no_of_product += 1

            print(j)
            j += 1

        return prod_review, link, overall_rating, price, ratings

    def run(self, page_visit):
        review = []
        avg_rating = []
        prices = []
        links = []
        all_r = []
        for i in range(self.page_visit):
            d = self.link_collection()
            print(len(d))
            x, y, z, a, b = self.scraping(d, self.limit)  # , self.count_product
            review.append(x)
            links.append(y)
            avg_rating.append(z)
            prices.append(a)
            all_r.append(b)

            # driver.switch_to.window(driver.window_handles[0])
            self.driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
            next_page = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, '_1LKTO3')))
            try:
                if len(next_page) == 1:
                    next_page[0].click()
                elif len(next_page) == 2:
                    next_page[1].click()
            except ElementClickInterceptedException:
                self.driver.refresh()
                time.sleep(4)
                self.driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')

                flag = False
                while flag != True:
                    try:
                        next_page = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_all_elements_located((By.CLASS_NAME, '_1LKTO3')))
                        if len(next_page) == 1:
                            next_page[0].click()
                        elif len(next_page) == 2:
                            next_page[1].click()
                        flag = True
                    except (ElementNotInteractableException, TimeoutException, ElementClickInterceptedException):
                        self.driver.refresh()
                        time.sleep(3)
                        pass

        self.result_queue.put((review, prices, avg_rating, all_r, links))

        # return review, avg_rating, prices, links, all_r