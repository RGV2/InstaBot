import commons
import random
import sys

from configurator import Configurator
from operations import InstagramBot
from time import sleep


def main():
    try:
        total_likes = 0
        config = Configurator.get_instance()
        ig = InstagramBot()

        if config.get_comment_enabled():
            commons.shuffle_comments()

        if config.get_hashtag_enabled():
            commons.shuffle_hashtags()

        if config.get_analyze_non_follower():
            commons.analyze_unfollower()

        username = config.get_username()
        password = config.get_password()
        ig.login(username, password)
        while True:
            try:
                hashtag = ig.get_hashtag_explore_page()
                hrefs_in_view = ig.get_href_in_views()
                photos_left = len(hrefs_in_view)
                for pic_href in hrefs_in_view:
                    if ig.load_post(pic_href):
                        if not ig.check_already_liked():
                            ig.scroll_up_down()
                            ig.hit_like()
                            total_likes += 1
                            photos_left -= 1
                            commons.hold_after_like(hashtag, total_likes, photos_left)

                            # Commenting on Photo
                            if (total_likes % 3 == 0 or total_likes % 4 == 0) and config.get_comment_enabled():
                                sleep(random.randint(4, 7))
                                ig.post_comment()

                            # Follow account
                            if (total_likes % 5 == 0 or total_likes % 6 == 0) and config.get_follow_enabled():
                                sleep(random.randint(4, 7))
                                ig.follow_account()

                            # Un-Follow account
                            if (total_likes % 7 == 0 or total_likes % 8 == 0) and config.get_unfollow_enabled():
                                sleep(random.randint(4, 7))
                                ig.unfollow_account()

            except Exception as ex_main:
                print(ex_main)
                ig.close_browser()
                sleep(60)
                main()
    except Exception as e:
        sys.exit('Error occurred in main: '+str(e))


if __name__ == "__main__":
    main()
