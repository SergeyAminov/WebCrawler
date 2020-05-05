from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import os


class WebCrawler:

    def __init__(self):
        """Initialize new web crawler with empty attributes"""

        self.driver_path = "C:\\chromedriver\\chromedriver.exe"
        self.screenshots_path = None
        self.urls_need_to_go = list()
        self.all_checked_urls = list()
        self.is_crawler_started = False
        self.is_fullpage = False
        self.opened_pages_number = 0
        self.current_main_url = None
        self.driver = None
        self.depth_of_walk = None

    def set_up(self):
        """Turn on the webdriver, activate proxy"""

        if not self.is_crawler_started:
            self.driver = webdriver.Chrome(self.driver_path)
            self.driver.maximize_window()
            self.is_crawler_started = True

    def tear_down(self):
        """Turn off the webdriver"""

        if self.is_crawler_started:
            self.driver.quit()
            self.is_crawler_started = False

    def get_valid_url(self, url):
        """Return the URL that may program recognize and go further"""

        if url.startswith("http"):
            return url
        else:
            return self.current_main_url + url

    def screenshot(self, url):
        """Taking and saving screenshot or several screenshots of given URL"""

        self.driver.get(url)

        # Delay for fully loading page
        time.sleep(1.5)

        self.opened_pages_number += 1
        if not self.is_fullpage:
            self.driver.save_screenshot(self.screenshots_path + "{}.png".format(self.opened_pages_number))
        else:
            full_webpage_height = self.driver.execute_script("return document.body.parentNode.scrollHeight")
            driver_window_height = self.driver.execute_script("return window.innerHeight")
            current_screenshot_height = 0
            part_number = 0
            while current_screenshot_height < full_webpage_height:
                part_number += 1
                current_screenshot_height = current_screenshot_height + driver_window_height
                self.driver.execute_script("window.scrollTo(0,{})".format(current_screenshot_height))
                self.driver.save_screenshot(self.screenshots_path + "{}_{}.png"
                                            .format(self.opened_pages_number, part_number))

    def read_from_file(self, source):
        """Open the file and write the list of URLs into the variable"""

        with open(source) as file:
            for url in file:
                if url.endswith('\n'):
                    url = url[:-1]
                self.urls_need_to_go.append(url)
        self.walk_control()

    def walk_control(self):
        """Activate and turn off web driver, create folder for each website from the list, call walk() function"""

        self.set_up()

        screenshot_path = "C:\\Screenshots\\"
        website_number = 0

        for url in self.urls_need_to_go:

            # To get the correct URL in get_valid_url() function for each website from the list
            self.current_main_url = url

            website_number += 1
            self.screenshots_path = screenshot_path + str(website_number) + "\\"
            os.makedirs(self.screenshots_path)
            self.walk(url, self.depth_of_walk)

        self.tear_down()

    def walk(self, url, depth):
        """Get the response from webpage, take screenshot, find all link to other pages, go through"""

        response = requests.get(url)
        if response.status_code == 200:
            self.screenshot(url)
            self.all_checked_urls.append(url)
        else:
            print(response.text)
        if not depth == 0:
            soup = BeautifulSoup(response.content, features="html.parser")
            links = soup.findAll('a')
            for link in links:
                valid_url = self.get_valid_url(link.get('href'))
                if valid_url not in self.all_checked_urls:
                    self.walk(valid_url, depth - 1)
                else:
                    continue
        else:
            return
