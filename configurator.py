import json
import os

import constants as const


class Configurator:
    __instance = None

    @staticmethod
    def get_instance():
        if Configurator.__instance is None:
            Configurator()
        return Configurator.__instance

    def __init__(self):

        if Configurator.__instance is not None:
            raise Exception('This class is a singleton!')
        else:
            Configurator.__instance = self

        self.analyze_non_follower = None
        self.comment_enabled = None
        self.disable_image = None
        self.follow_enabled = None
        self.hashtag_enabled = None
        self.headless = None
        self.likes_per_hashtag = None
        self.password = None
        self.unfollow_enabled = None
        self.username = None
        self.config = None

    def get_configurations(self):
        with open(const.CONFIG_FILE_PATH, mode=const.R) as self.config:
            self.config = json.load(self.config)
            self.analyze_non_follower = True if self.config[const.ANALYZE_NON_FOLLOWER].lower() == const.TRUE else False
            self.comment_enabled = True if self.config[const.COMMENT].lower() == const.TRUE else False
            self.disable_image = True if self.config[const.DISABLE_IMAGE].lower() == const.TRUE else False
            self.follow_enabled = True if self.config[const.FOLLOW].lower() == const.TRUE else False
            self.hashtag_enabled = True if self.config[const.HASHTAG].lower() == const.TRUE else False
            self.headless = True if self.config[const.HEADLESS].lower() == const.TRUE else False
            self.likes_per_hashtag = self.config[const.LIKES_PER_HASHTAG]
            self.password = self.config[const.PASSWORD]
            self.unfollow_enabled = True if self.config[const.UNFOLLOW].lower() == const.TRUE else False
            self.username = self.config[const.USERNAME]

    def update_configurations(self, config_name, updated_value):
        with open(const.CONFIG_FILE_PATH, mode=const.W) as updated_config:
            self.config[config_name] = updated_value
            json.dump(self.config, updated_config)

    def get_analyze_non_follower(self):
        self.get_configurations()
        if self.analyze_non_follower:

            try:
                if os.path.getsize(const.FOLLOWERS_FILE_PATH) == 0 or os.path.getsize(const.FOLLOWING_FILE_PATH) == 0:
                    print('Empty {} or {} found, setting "{}" config to "{}".'
                          .format(const.FOLLOWERS_FILE_PATH, const.FOLLOWING_FILE_PATH, const.ANALYZE_NON_FOLLOWER, const.FALSE))
                    self.update_configurations(const.ANALYZE_NON_FOLLOWER, const.FALSE)
                    return self.get_analyze_non_follower()

            except FileNotFoundError:
                print('"{}: {} or {}", setting "{}" config to "false".'
                      .format(const.NO_FILE_FOUND, const.FOLLOWERS_FILE_PATH,
                              const.FOLLOWING_FILE_PATH, const.ANALYZE_NON_FOLLOWER))
                self.update_configurations(const.ANALYZE_NON_FOLLOWER, const.FALSE)
                return self.get_analyze_non_follower()

        return self.analyze_non_follower

    def get_comment_enabled(self):
        self.get_configurations()
        if self.comment_enabled:

            try:
                if os.path.getsize(const.COMMENTS_FILE_PATH) == 0:
                    print('Empty {} found, setting "comment" config to "false".'.format(const.COMMENTS_FILE_PATH))
                    self.update_configurations(const.COMMENT, const.FALSE)
                    return self.get_comment_enabled()

            except FileNotFoundError:
                print('"{}: {}", setting "{}" config to "false".'
                      .format(const.NO_FILE_FOUND, const.COMMENTS_FILE_PATH, const.COMMENT))
                self.update_configurations(const.COMMENT, const.FALSE)
                return self.get_comment_enabled()

        return self.comment_enabled

    def get_disable_image(self):
        self.get_configurations()
        return self.disable_image

    def get_follow_enabled(self):
        self.get_configurations()
        return self.follow_enabled

    def get_hashtag_enabled(self):
        self.get_configurations()
        if self.hashtag_enabled:
            try:
                if os.path.getsize(const.HASHTAGS_FILE_PATH) == 0:
                    print('Empty {} found, setting "{}" config to "false".'
                          .format(const.HASHTAGS_FILE_PATH, const.HASHTAG))
                    self.update_configurations(const.HASHTAG, const.FALSE)
                    return self.get_hashtag_enabled()
            except FileNotFoundError:
                print('"{}: {}", setting "{}" config to "false".'
                      .format(const.NO_FILE_FOUND, const.HASHTAGS_FILE_PATH, const.HASHTAG))
                self.update_configurations(const.HASHTAG, const.FALSE)
                return self.get_hashtag_enabled()
        return self.hashtag_enabled

    def get_headless(self):
        self.get_configurations()
        return self.headless

    def get_likes_per_hashtag(self):
        self.get_configurations()
        try:
            int_likes_per_hashtag = int(self.likes_per_hashtag)
            if int_likes_per_hashtag < 1:
                print('Less tha 1 value found for {} config, setting "{}" config to "{}"'
                      .format(const.LIKES_PER_HASHTAG, const.LIKES_PER_HASHTAG, const.DEFAULT_LIKES_PER_HASHTAG))
                self.update_configurations(const.LIKES_PER_HASHTAG, const.DEFAULT_LIKES_PER_HASHTAG)
                return self.get_likes_per_hashtag()

        except ValueError:
            print('Invalid config for {} found, setting "{}" config to "{}"'
                  .format(const.LIKES_PER_HASHTAG, const.LIKES_PER_HASHTAG, const.DEFAULT_LIKES_PER_HASHTAG))
            self.update_configurations(const.LIKES_PER_HASHTAG, const.DEFAULT_LIKES_PER_HASHTAG)
            return self.get_likes_per_hashtag()
        return int_likes_per_hashtag

    def get_password(self):
        self.get_configurations()
        if self.password != const.EMPTY:
            return self.password
        else:
            raise ValueError(const.EMPTY_PASSWORD)

    def get_unfollow_enabled(self):
        self.get_configurations()
        if self.unfollow_enabled:
            try:
                if os.path.getsize(const.NOT_FOLLOWING_FILE_PATH) == 0:
                    print('Empty {} found, setting "{}" config to "false".'
                          .format(const.NOT_FOLLOWING_FILE_PATH, const.UNFOLLOW))
                    self.update_configurations(const.UNFOLLOW, const.FALSE)
                    return self.get_unfollow_enabled()
            except FileNotFoundError:
                print('"{}: {}", setting "{}" config to "false".'
                      .format(const.NO_FILE_FOUND, const.NOT_FOLLOWING_FILE_PATH, const.UNFOLLOW))
                self.update_configurations(const.UNFOLLOW, const.FALSE)
                return self.get_unfollow_enabled()
        return self.unfollow_enabled

    def get_username(self):
        self.get_configurations()
        if self.username != const.EMPTY:
            return self.username
        else:
            raise ValueError(const.EMPTY_USERNAME)
