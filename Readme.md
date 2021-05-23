
# Instagram Bot

This is an automated Selenium based Web Scrapping Bot.

### Task done by Instagram Bot

    1. Login to Instagram
    2. Get the datetime of the recent post
    3. Open the Messages
    4. Validate the member is from OWASP
    5. Validate if the person has shared the post
    6. Logs the members name in the file


### Requirement

   1. Selenium `pip install selenium`
   2. Download the ![Chrome Web Browser](https://chromedriver.chromium.org/) according to Browser's Version
   3. Set the instagram credentials in `credentials.py`.

     user_name = ""  # INSTAGRAM USERNAME
     password = ""  # INSTAGRAM PASSWORD
   4. Add the members instagram handle in the list in `names.py`

### Debugging

   Increase the sleep time there. Mainly the error could arise due to slower internet speed.


### Important Note

   Do not attempt to **login** into same instagram account too frequently. Instagram may either IP ban you or temporarily ban you from logging in from any device.
   
Enjoy😜 !!!