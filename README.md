# InstaBot
Instagram bot to get more traffic to your profile by hitting like and posting comments on the posts.
##### ver_01:
- Like photos.
- Post comment on random posts based on the logic.
- Added two .txt files with names comments, & hashtags in the instaRes folder.
- Add the comments in the comments.txt file separated by new line.
- Add the hashtags in the hashtags.txt file separated by new line.

##### ver_02:
- Added _config.json_, where you must specify the _username_ & _password_. 
- Also in config file you can mention the _hashtag_ & _comment_ setting as true or false **(NOTE: value other than true will be considered as false)**
- If **hashtag** is set to **true**, it will explore the post with the random hashtags from the text file.
- If **hashtag** is set to **false**, _it will fetch the posts from the explore page only_. **(NOTE: This feature is added as we are not able to open the hashtag pages in the web browser.)**