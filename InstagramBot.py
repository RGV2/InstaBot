from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

import random
import sys
import json
import os


def print_same_line(text):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()


def type_phrase(comment, field):
    for letter in comment:
        field.send_keys(letter)
        sleep(0.2)


class InstagramBot:

    def __init__(self, u_name, pwd):
        self.username = u_name
        self.password = pwd
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.likes = 0
        self.i_hashtag = 0
        self.i_comment = 0

    def close_browser(self):
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/")
        sleep(5)
        username_element = driver.find_element_by_name('username')
        username_element.send_keys(self.username)
        password_element = driver.find_element_by_name('password')
        password_element.send_keys(self.password)
        password_element.send_keys(Keys.RETURN)
        sleep(5)
        return

    # Method for hitting like begins
    def hit_like(self):
        hrefs_in_view = ''
        driver = self.driver
        hashtag = None

        with open('./instaRes/config.json', mode='r') as hash_config:
            hash_config = json.load(hash_config)
            hashtag_status = hash_config['hashtag']

            if hashtag_status.lower() == 'true':
                hashtag_status = hashtag_status.lower()
            else:
                hashtag_status = 'false'

        if hashtag_status == 'true':
            with open('./instaRes/hashtags.txt', mode='r', encoding='utf8') as hashtags_f:
                hashtags = hashtags_f.read().splitlines()
                total_hashtags = len(hashtags)
            hashtag = hashtags[self.i_hashtag % total_hashtags]
            driver.get('https://www.instagram.com/explore/tags/' + hashtag + '/')
            self.i_hashtag += 1
        else:
            driver.get('https://www.instagram.com/explore/')

        try:
            sleep(random.randint(5, 7))
            hrefs_in_view = driver.find_elements_by_tag_name('a')
            hrefs_in_view = [elem.get_attribute('href')
                             for elem in hrefs_in_view
                             if '/p/' in elem.get_attribute('href')]

            with open('./instaRes/config.json', mode='r') as likes_per_hashtag_config:
                likes_per_hashtag_config = json.load(likes_per_hashtag_config)
                try:
                    likes_per_hashtag = int(likes_per_hashtag_config['likes_per_hashtag'])
                    if likes_per_hashtag < 1:
                        likes_per_hashtag = 1
                    hrefs_in_view = hrefs_in_view[:likes_per_hashtag]
                except ValueError:
                    sys.exit('Invalid config found for \'likes_per_hashtag\' in config.json. Please enter Integer only')

        except Exception as ex_fetch_url:
            print(ex_fetch_url)

        # Liking photos
        total_photos = len(hrefs_in_view)
        for pic_href in hrefs_in_view:
            driver.get(pic_href)
            sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)
            driver.execute_script("window.scrollTo(0, -document.body.scrollHeight);")
            try:

                sleep(random.randint(2, 4))
                check_like = driver.find_element_by_xpath("//button[normalize-space(@class)='wpO6b']/"
                                                          "div[normalize-space(@class)='QBdPU']/span/*[name()='svg']")
                if check_like.get_attribute('aria-label') == 'Like':
                    driver.find_element_by_xpath('//*[@id="react-root"]/section/main/'
                                                 'div/div[1]/article/div[3]/section[1]/span[1]/button').click()

                    self.likes += 1

                    # Commenting on Photo
                    if self.likes % 3 == 0 or self.likes % 4 == 0:
                        self.post_comment()

                    sleep(random.randint(1, 3))

                    # Follow account
                    if self.likes % 5 == 0 or self.likes % 6 == 0:
                        self.follow_account()

                else:
                    total_photos -= 1
                    continue

                total_photos -= 1
                for second in reversed(range(0, random.randint(20, 30))):
                    if hashtag is None:
                        hashtag = ' '
                    print_same_line("#" + hashtag + ': Photos left: ' + str(total_photos) + " | Total Likes: " +
                                    str(self.likes) + " | Sleeping " + str(second))
                    sleep(1)

            except Exception as ex_like:
                print(ex_like)
                sleep(2)
    # Method for hitting like end

    # Method for posting comments begin
    def post_comment(self):
        with open('./instaRes/config.json', mode='r') as comment_config:
            comment_config = json.load(comment_config)
            comment_status = comment_config['comment']
            if comment_status.lower() == 'true':
                comment_status = 'true'
            else:
                comment_status = 'false'

        if comment_status == 'true':
            with open('./instaRes/comments.txt', mode='r', encoding='utf8') as comments_f:
                comments = comments_f.read().splitlines()
                total_comments = len(comments)
            comment = comments[self.i_comment % total_comments]
            driver = self.driver
            driver.find_element_by_class_name('Ypffh').click()
            comment_element = driver.find_element_by_class_name('Ypffh')
            sleep(1)
            comment_element.clear()
            type_phrase(comment, comment_element)
            sleep(3)
            driver.find_element_by_xpath('//button[contains(text(), "Post")]').click()
            sleep(5)
            self.i_comment += 1

        return
    # Method for posting comments end

    # Method for account following begins
    def follow_account(self):
        with open('./instaRes/config.json', mode='r') as follow_config:
            follow_config = json.load(follow_config)
            follow_status = follow_config['follow']
            if follow_status.lower() == 'true':
                follow_status = 'true'
            else:
                follow_status = 'false'

        if follow_status == 'true':
            driver = self.driver
            follow_button = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/'
                                                         'article/header/div[2]/div[1]/div[2]/button')
            if follow_button.text == 'Follow':
                follow_button.click()

        return
    # Method for account following end


if __name__ == "__main__":

    with open('./instaRes/config.json', mode='r') as config:
        config = json.load(config)
        username = config['username']
        password = config['password']

        if os.path.getsize('./instaRes/hashtags.txt') == 0 or os.path.getsize('./instaRes/comments.txt') == 0:
            sys.exit('Empty comment.txt or hashtag.txt file. Please try again... :)')

        if username == '' or password == '':
            sys.exit('Invalid username or password entered. Please try again... :)')
        else:
            ig = InstagramBot(username, password)
            ig.login()

    while True:
        try:
            ig.hit_like()
        except Exception as ex_main:
            print(ex_main)
            ig.close_browser()
            sleep(60)
            ig = InstagramBot(username, password)
            ig.login()
