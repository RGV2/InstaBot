# InstaBot
Instagram bot to get more traffic to your profile by hitting like and posting comments on the posts.
### ver_01:
- Like photos.
- Post comment on random posts based on the logic.
- Added two .txt files with names comments, & hashtags in the instaRes folder.
- Add the comments in the comments.txt file separated by new line.
- Add the hashtags in the hashtags.txt file separated by new line.

### ver_02:
- Added config.json, where you must specify the username & password.
- In addition config file have 4 more attributes, you can mention the hashtag, comment, & follow setting as true or false (NOTE: value other than true will be considered as false). And likes_per_hashtag as any integer > 0.
- If hashtag is set to true, it will explore the post with the random hashtags from the text file.
- If hashtag is set to false, it will fetch the posts from the explore page only. (NOTE: This feature is added as we are not able to open the hashtag pages in the web browser.)
- If follow is set to true in config, then it will follow the random pages based on the logic.

### If you find this repo useful, please hit the STAR & follow me.
