import commons
import constants as const
import logging
import os
import pandas
import random
import sys

from configurator import Configurator
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager


class InstagramBot:

    def __init__(self):
        print(const.INITIALIZING)
        self.config = Configurator.get_instance()
        chrome_options = webdriver.ChromeOptions()
        os.environ[const.WDM_LOG_LEVEL] = str(logging.CRITICAL)
        if self.config.get_disable_image():
            prefs = {const.PROFILE_MANAGED_IMAGES: 2}
            chrome_options.add_experimental_option(const.PREFS, prefs)

        if self.config.get_headless():
            chrome_options.headless = True

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        self.i_hashtag = 0
        self.i_comment = 0

    def close_browser(self):
        self.driver.close()

    def login(self, username, password):
        try:
            driver = self.driver
            driver.get(const.INSTAGRAM_HOME_URL)
            sleep(5)
            username_element = driver.find_element_by_name(const.USERNAME)
            username_element.send_keys(username)
            password_element = driver.find_element_by_name(const.PASSWORD)
            password_element.send_keys(password)
            password_element.send_keys(Keys.RETURN)
            sleep(5)
            try:
                verifier = driver.find_element_by_xpath(const.LOGIN_ERROR_XPATH)
                if verifier.text == const.INVALID_CREDENTIALS:
                    self.close_browser()
                    sys.exit(const.INVALID_CREDENTIALS)
            except NoSuchElementException:
                print(const.LOGIN_SUCCESS)
                pass

        except (NoSuchElementException, Exception):
            self.close_browser()
            sys.exit('Error occurred while Logging in.')

    def get_hashtag_explore_page(self):
        try:
            driver = self.driver
            hashtag = None
            hashtag_enabled = self.config.get_hashtag_enabled()
            if hashtag_enabled:
                with open(const.HASHTAGS_FILE_PATH, mode=const.R, encoding=const.UTF8) as hashtags_f:
                    hashtags = hashtags_f.read().splitlines()
                    total_hashtags = len(hashtags)
                hashtag = hashtags[self.i_hashtag % total_hashtags]
                driver.get(const.TAGS_URL + hashtag)
                self.i_hashtag += 1
                return hashtag
            else:
                driver.get(const.EXPLORE_URL)
                return hashtag
        except Exception as e:
            self.close_browser()
            sys.exit('Error occurred while loading hashtag | explore page: '+str(e))

    def get_href_in_views(self):
        try:
            driver = self.driver
            sleep(random.randint(5, 7))
            hrefs_in_view = driver.find_elements_by_tag_name(const.A)
            hrefs_in_view = [elem.get_attribute(const.HREF)
                             for elem in hrefs_in_view
                             if const.SLASH_P in elem.get_attribute(const.HREF)]
            likes_per_hashtag = self.config.get_likes_per_hashtag()
            if likes_per_hashtag < len(hrefs_in_view) - 9:
                hrefs_in_view = hrefs_in_view[9:likes_per_hashtag + 9]

            return hrefs_in_view
        except Exception as e:
            self.close_browser()
            sys.exit('Error occurred while getting URLs of posts: '+str(e))

    def check_already_liked(self):
        try:
            driver = self.driver
            check_like = driver.find_element_by_xpath(const.CHECK_LIKE_XPATH)
            if check_like.get_attribute(const.ARIA_LABEL).lower() == const.LIKE:
                return False
            return True
        except (NoSuchElementException, Exception):
            self.close_browser()
            sys.exit('Error occurred while checking like status.')

    def load_post(self, pic_href):
        try:
            driver = self.driver
            driver.get(pic_href)
            sleep(2)
            if driver.title != const.PAGE_NOT_FOUND:
                return True
            return False
        except Exception as e:
            self.close_browser()
            sys.exit('Error occurred while loading post: '+str(e))

    def scroll_up_down(self):
        try:
            driver = self.driver
            driver.execute_script(const.SCROLL_UP)
            sleep(2)
            driver.execute_script(const.SCROLL_DOWN)
        except Exception as e:
            self.close_browser()
            sys.exit('Error occurred while scrolling: '+str(e))

    def hit_like(self):
        try:
            driver = self.driver
            driver.find_element_by_xpath(const.LIKE_BUTTON_XPATH).click()
        except (NoSuchElementException, Exception):
            self.close_browser()
            sys.exit('Error occurred while hitting like on the post.')

    def post_comment(self):
        try:
            with open(const.COMMENTS_FILE_PATH, mode=const.R, encoding=const.UTF8) as comments_f:
                comments = comments_f.read().splitlines()
                total_comments = len(comments)
            comment = comments[self.i_comment % total_comments]
            driver = self.driver
            driver.find_element_by_class_name(const.YPFFH).click()
            comment_element = driver.find_element_by_class_name(const.YPFFH)
            sleep(1)
            comment_element.clear()
            commons.type_phrase(comment, comment_element)
            sleep(3)
            driver.find_element_by_xpath(const.POST_COMMENT_BUTTON_XPATH).click()
            sleep(5)
            self.i_comment += 1
        except (NoSuchElementException, Exception):
            self.close_browser()
            sys.exit('Error occurred while posting comment on the post.')

    def follow_account(self):
        try:
            sleep(random.randint(5, 10))
            driver = self.driver
            follow_button = driver.find_element_by_xpath(const.FOLLOW_BUTTON_XPATH)
            if follow_button.text.lower() == const.FOLLOW:
                follow_button.click()
        except (NoSuchElementException, Exception):
            self.close_browser()
            sys.exit('Error occurred while following account from post.')

    def unfollow_account(self):
        try:
            sleep(random.randint(5, 10))
            driver = self.driver
            not_following = pandas.read_csv(const.NOT_FOLLOWING_FILE_PATH, index_col=const.USERNAME)
            counter = random.randint(1, 3)
            if not not_following.empty:
                for username_ in not_following.index[-counter:]:
                    driver.get(const.INSTAGRAM_HOME_URL + username_)
                    sleep(3)
                    driver.find_element_by_xpath(const.UNFOLLOW_BUTTON_OPENER_XPATH).click()
                    sleep(5)
                    driver.find_element_by_xpath(const.UNFOLLOW_BUTTON_XPATH).click()
                    sleep(2)
                    not_following = not_following.drop(username_)
                    not_following.to_csv(const.NOT_FOLLOWING_FILE_PATH)
        except (NoSuchElementException, Exception):
            self.close_browser()
            sys.exit('Error occurred while Unfollowing account.')
