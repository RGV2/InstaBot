from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

import random
import sys


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
    likes = 0

    def __init__(self, u_name, pwd):
        self.username = u_name
        self.password = pwd
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

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

    def like_comment(self, hashtag):

        hrefs_in_view = None
        with open('./instaRes/comments.txt', mode='r', encoding='utf8') as comments_f:
            comments = comments_f.read().splitlines()
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")

        try:
            sleep(random.randint(5, 7))
            hrefs_in_view = driver.find_elements_by_tag_name('a')
            hrefs_in_view = [elem.get_attribute('href')
                             for elem in hrefs_in_view
                             if '/p/' in elem.get_attribute('href')]

            # Removing the top 9 posts.
            hrefs_in_view = hrefs_in_view[9:]

        except Exception as e:
            print(e)

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
                                                 'div/div[1]/article/div/div[3]/section[1]/span[1]/button').click()
                    InstagramBot.likes += 1

                    # Commenting on Photo
                    if InstagramBot.likes % 3 == 0 or InstagramBot.likes % 4 == 0:
                        driver.find_element_by_class_name('Ypffh').click()
                        comment_element = driver.find_element_by_class_name('Ypffh')
                        sleep(1)
                        comment_element.clear()
                        type_phrase(random.choice(comments), comment_element)
                        sleep(3)
                        driver.find_element_by_xpath('//button[contains(text(), "Post")]').click()
                        sleep(5)

                total_photos -= 1
                for second in reversed(range(0, random.randint(20, 30))):
                    print_same_line("#" + hashtag + ': Photos left: ' + str(total_photos) + " | Total Likes: " + str(
                        InstagramBot.likes) + " | Sleeping " + str(second))
                    sleep(1)

            except Exception:
                sleep(2)


if __name__ == "__main__":

    username = "mushtaq.ashhar"
    password = "**************"

    ig = InstagramBot(username, password)
    ig.login()

    while True:
        with open('./instaRes/hashtags.txt', mode='r', encoding='utf8') as hashtag_f:
            hashtags = hashtag_f.read().splitlines()

        try:
            tag = random.choice(hashtags)
            ig.like_comment(tag)

        except Exception:
            ig.close_browser()
            sleep(60)
            ig = InstagramBot(username, password)
            ig.login()
