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


class Croma:
    def __init__(self, search, limit, page_visit):  # , count_product
        self.search = search
        self.limit = limit
        self.page_visit = page_visit
        # self.count_product = count_product
        self.result_queue = Queue()
        self.s = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.s)
        self.driver.get('https://www.croma.com/')
        self.flag = False

        while self.flag != True:
            try:
                # self.un = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'MuiAutocomplete-input.MuiAutocomplete-inputFocused.search-field')))
                self.un = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="searchV2"]')))

                self.un.send_keys(self.search)
                self.flag = True
            except (ElementNotInteractableException, TimeoutException):
                self.driver.refresh()
                time.sleep(3)
                pass
        #                 self.un = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'MuiAutocomplete-input.MuiAutocomplete-inputFocused.search-field')))
        #                 self.un.send_keys(self.search)
        #                 self.flag = True

        time.sleep(2)
        self.un.send_keys(Keys.ENTER)

    #         try:
    #             self.un = WebDriverWait(self.driver, 12).until(EC.presence_of_element_located((By.CLASS_NAME,'MuiAutocomplete-input.MuiAutocomplete-inputFocused.search-field')))
    #             #time.sleep(2)
    #             self.un.send_keys(search)
    #             time.sleep(2)
    #             self.un.send_keys(Keys.ENTER)
    #         except ElementNotInteractableException:
    #             self.driver.refresh()
    #             self.un = WebDriverWait(self.driver, 12).until(EC.presence_of_element_located((By.CLASS_NAME,'MuiAutocomplete-input.MuiAutocomplete-inputFocused.search-field')))
    #             #time.sleep(2)
    #             self.un.send_keys(search)
    #             time.sleep(2)
    #             self.un.send_keys(Keys.ENTER)

    def link_collection(self):

        self.driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
        time.sleep(2)

        link_texts = []

        te = self.search.split(' ')
        # y = []
        # print(x)
        for j in te:
            k = 0
            for i in range(len(j)):
                modified_string = f"{j[:i]}{j[i].upper()}{j[i + 1:]}"
                link_texts.append(modified_string)
                k += 1
                if k == 2:
                    break

        link = []
        for i in link_texts:
            try:
                review_link = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, i)))
                if len(review_link) != 0:
                    for i in review_link:
                        link.append(i)
            except TimeoutException:
                pass
        # print(link)

        #         review_link = WebDriverWait(self.driver, 10).until(
        #             EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, self.search)))
        # name = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'_4rR01T')))

        d = {}
        name = []
        for i in link:
            name.append(i.text)
            # print(i.text)
        # print(name)
        for i, j in zip(link, name):
            # x = self.search.lower()
            # if x in j.lower() and '(Renewed)' not in j:
            d[i] = j

        time.sleep(1)
        # print(d)
        return d

    def scrapings(self, d, limit):  # , count_product
        j = 1
        prod_review = {}
        no_of_product = 0
        link = {}
        price = {}
        ratings = {}
        avg_rating = {}

        for i in d:
            # if no_of_product == self.count_product:
            #     break
            self.driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
            self.driver.switch_to.window(self.driver.window_handles[0])
            # i.click()
            webdriver.ActionChains(self.driver).move_to_element(i).click(i).perform()
            while len(self.driver.window_handles) != 2:
                time.sleep(3)
                webdriver.ActionChains(self.driver).move_to_element(i).click(i).perform()

            # driver.execute_script("arguments[0].click();", i)
            time.sleep(2)
            # driver.switch_to.window(driver.window_handles[j])
            c = self.driver.window_handles[1]
            self.driver.switch_to.window(c)

            y = d[i]
            # scraping link
            l = self.driver.current_url
            link[y] = l

            # scraping price
            e = self.driver.page_source
            x = BeautifulSoup(e, 'html.parser')
            p = []
            h = x.find_all('span', {'class': 'amount'})

            if len(h) <= 0:
                price[y] = p
            else:
                p.append(h[0].text)
                price[y] = p

            # time.sleep(2)
            self.driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
            time.sleep(7)
            # try:
            #    all_comments = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'btn-wrap.view-all-review-btn')))
            # all_comments[0].click()
            #   webdriver.ActionChains(driver).move_to_element(all_comments).click(all_comments).perform
            # except TimeoutException:
            #    pass

            # scrapping ratings
            e = self.driver.page_source
            x = BeautifulSoup(e, 'html.parser')

            r = []
            rating = {'5 Stars': 0, '4 Stars': 0, '3 Stars': 0, '2 Stars': 0, '1 Stars': 0}
            l = h = x.find_all('div', {'class': 'barAndStar'})
            # h = x.find_all('p', {'class' : 'right-text'})
            # rating['4 Stars'] = l[0].text
            if len(l) <= 0:
                ratings[y] = rating
            else:
                count = 5
                for i in l:
                    rating['{} Stars'.format(count)] = i.text[6:]
                    count -= 1

                ratings[y] = rating

            # scraping  avg ratings
            e = self.driver.page_source
            x = BeautifulSoup(e, 'html.parser')
            t = []
            h = x.find_all('div', {'class': 'totalRating'})

            if len(h) <= 0:
                avg_rating[y] = t
            else:
                t.append(h[0].text)
                avg_rating[y] = t

            # time.sleep(3)

            # scraping review
            e = self.driver.page_source
            x = BeautifulSoup(e, 'html.parser')

            h = x.find_all('div', {'class': 'desc'})
            reviews = set()
            # y = d[i]
            for k in h:
                reviews.add(k.text)
                print(k.text)
                if len(reviews) == self.limit:
                    break
            # driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
            # curr_height = driver.execute_script('return document.body.scrollHeight;')
            flag = 0
            reviews1 = reviews
            while len(reviews) != self.limit:
                try:
                    # driver.execute_script('window.scrollBy(0, 2000);')
                    # time.sleep(2)
                    flag += 1
                    more = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'View All Reviews')))
                    webdriver.ActionChains(self.driver).move_to_element(more).click(more).perform()
                    e = self.driver.page_source
                    x = BeautifulSoup(e, 'html.parser')
                    t = x.find_all('div', {'class': 'desc'})
                    # print(curr_height)
                    # curr_height += 100
                    for l in t:
                        reviews.add(l.text.strip())
                        if len(reviews) == self.limit:
                            break

                    self.driver.execute_script('window.scrollBy(5350, 100);')
                    time.sleep(3)
                    print(flag)
                    if flag == 11:
                        if len(reviews1) == len(reviews):
                            break

                    # driver.execute_script('window.scrollBy(0, 2000);')
                except TimeoutException:
                    flag += 3
                    if flag >= 11:
                        break
                    else:
                        pass

            prod_review[y] = reviews
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            no_of_product += 1
            print(j)
            j += 1

        return prod_review, ratings, link, avg_rating, price

    def run(self, page_visit):
        links = []
        reviews = []
        all_ratings = []
        prices = []
        avg_r = []

        main_d = {}
        now = time.time()
        for i in range(self.page_visit):
            d = self.link_collection()
            print(len(d))
            new_d = {}
            for i, j in d.items():
                if i in main_d:
                    continue
                else:
                    new_d[i] = j
            for i, j in d.items():
                main_d[i] = j
            x, y, z, a, b = self.scrapings(new_d, self.limit)  # , self.count_product
            reviews.append(x)
            all_ratings.append(y)
            links.append(z)
            avg_r.append(a)
            prices.append(b)

            self.driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
            time.sleep(3)
            next_page = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'btn.btn-secondary.btn-viewmore')))
            webdriver.ActionChains(self.driver).move_to_element(next_page).click(next_page).perform()

        self.result_queue.put((reviews, prices, avg_r, all_ratings, links))

        # return reviews, all_ratings, links, avg_r, prices
# x = Croma('iPhone 14', 10)


