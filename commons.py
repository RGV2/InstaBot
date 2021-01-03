import constants as const
import pandas
import random
import sys

from time import sleep


def print_same_line(text):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()


def type_phrase(comment, field):
    for letter in comment:
        field.send_keys(letter)
        sleep(0.2)


def hold_after_like(h_tag, total_likes, photos_left):
    for second in reversed(range(0, random.randint(20, 30))):
        if h_tag is None:
            h_tag = ' '
        print_same_line('#{}: Photos left: {} | Total Likes: {} | Sleeping {}'
                        .format(h_tag, photos_left, total_likes, second))
        sleep(1)


def shuffle_comments():
    with open(const.COMMENTS_FILE_PATH) as comments:
        comments_lines = comments.readlines()
    random.shuffle(comments_lines)
    with open(const.COMMENTS_FILE_PATH, const.W) as comments:
        comments.writelines(comments_lines)


def shuffle_hashtags():
    with open(const.HASHTAGS_FILE_PATH) as hashtags:
        hashtags_lines = hashtags.readlines()
    random.shuffle(hashtags_lines)
    with open(const.HASHTAGS_FILE_PATH, const.W) as hashtags:
        hashtags.writelines(hashtags_lines)


def analyze_unfollower():
    following = pandas.read_csv(const.FOLLOWING_FILE_PATH, index_col=const.USERNAME)
    followers = pandas.read_csv(const.FOLLOWERS_FILE_PATH, index_col=const.USERNAME)
    mutual = following.index.intersection(followers.index, sort=False)
    not_following = following.drop(mutual)
    not_following.to_csv(const.NOT_FOLLOWING_FILE_PATH)
