

import time
import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from credentials import user_name,password
from names import members

filename = 'owasp1.txt'

# initializing selenium
def init():
    path = "C:\\webdrivers\\chromedriver.exe"
    driver_var = webdriver.Chrome(path)
    driver_var.maximize_window()
    return driver_var

# instagram login
def login(driver):
    driver.get("https://www.instagram.com/")

    time.sleep(2)
    # credentials
    try:
        login_username = driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input")
        login_username.send_keys(user_name)
        login_password = driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input")
        login_password.send_keys(password)
        login_button = driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button")
        login_button.click()
    except :
        print("Either password is wrong or Instagram has IP banned you")


    time.sleep(5)
    # don't save password
    try:
        not_now = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div/div/button")
        not_now.click()
    except:
        print("The page has not loaded yet increase the sleep above")


    time.sleep(2)
    # disable notification
    try:
        disable_noti = driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]")
        disable_noti.click()
    except:
        print("Clicked button already")


    print("logged in")
    time.sleep(2)

#open the messaging tab
def open_messages(driver):
   driver.get("https://www.instagram.com/direct/inbox/")
   print("Messages Opened")
   time.sleep(5)

# _utility: check if the xpath exists
def check_xpath(driver,path):
    try:
        driver.find_element_by_xpath(path)
    except NoSuchElementException:
        return False
    return True

# sends the confirmation message
def send_confirmation(driver,base_path):
    dm_page = driver.find_element_by_xpath(base_path+"/a/div").click()
    time.sleep(1)
    # textarea = driver.find_element_by_xpath("/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea")
    # textarea.send_keys("[OWASP BOT]: Thank you for sharing our Story.\n")
    driver.back()

# validates the users
def validation(driver,username,base_path):
    unread_msg = check_xpath(driver, base_path + "/a/div/div[3]/div")
    visible_msg = driver.find_element_by_xpath(base_path + "/a/div/div[2]/div[2]/div/div/span[1]/span").text
    if unread_msg and visible_msg == "Mentioned you in their story":
        send_confirmation(driver,base_path)
        print(username)
        file = open(filename,'a')
        file.writelines(username+"\n")
        file.close()

# gets the time of the recent post
def time_of_recent_post(driver,url):
    driver.get(url)
    time.sleep(2)
    post_time = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[1]/article/div[3]/div[2]/a/time")
    recent_post = post_time.get_attribute("datetime")
    recent_post_mod = datetime.datetime.strptime(recent_post, '%Y-%m-%dT%H:%M:%S.%fZ')
    print(recent_post_mod)
    return recent_post_mod

#finds parent
def parentlist(driver,parent_base_path):
    parent = driver.find_elements_by_xpath(parent_base_path)
    # print(len(parent))
    names = []
    for child in range(len(parent) - 1):
        name = (driver.find_element_by_xpath(
            parent_base_path + "[" + str(child + 1) + "]/a/div/div[2]/div[1]/div/div/div/div").text)
        if (name != ''):
            names.append(name)
    print(names)
    return names

# brain: scroll n verifies the users
# scroll AKA brain 2.0: *STRESSED VOICES ALL OVER*
def brain(driver,post_time):
    open_messages(driver)

    file = open(filename,'a')
    file.writelines(str(datetime.datetime.now())+"\n")
    file.close()
    print("WAITING....")
    prev_person = None
    index = 0
    while(True):
        time.sleep(1)
        # print("HELLO!!! I'm Scroller I scroll instagram for you")

        parent_base_path     ="/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[3]/div/div/div/div/div"
        # business_base_path ="/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[3]/div/div/div/div/div"
        # normal_base_path   ="/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[2]/div/div/div/div/div"

        names = parentlist(driver,parent_base_path)

        if prev_person != None and prev_person not in names:
            print(prev_person)
            while True:
                names = parentlist(driver,parent_base_path)
                i = driver.find_element_by_xpath(parent_base_path + "[" + str(index + 7) + "]")
                a = ActionChains(driver)
                a.move_to_element(i).perform()
                print("PANIC FUNCTION ACTIVATED")
                time.sleep(0.5)
                if prev_person in names and names[-1]!=prev_person:
                    break

        if (prev_person != None):
            index = names.index(prev_person)+1

        # base_path of the user
        base_path = parent_base_path+"["+str(index+1)+"]"

        # time of story uploading
        msg_time = driver.find_element_by_xpath(base_path + "/a/div/div[2]/div[2]/div/div/time")
        story_time = msg_time.get_attribute("datetime")
        story_time_mod = datetime.datetime.strptime(story_time, '%Y-%m-%dT%H:%M:%S.%fZ')
        if (story_time_mod < post_time):
            print("SAFELY QUITTING...")
            exit(1)
            break

        # username extraction
        members_name = driver.find_element_by_xpath(base_path + "/a/div/div[2]/div[1]/div/div/div/div")
        members_username = members_name.text
        print("MEMBERS:", members_username)

        # username validation and verification
        if (members_username in members):
            print("OWASP MEMBERS:",members_username)
            validation(driver, members_name.text,base_path)

        i = driver.find_element_by_xpath(parent_base_path+"["+str(index+5)+"]")
        a = ActionChains(driver)
        a.move_to_element(i).perform()
        prev_person = names[index]
        print()
    # block()

# this is a blocker to stop the browser from closing
def block():
    num = 0
    while(True):
        num+=1

# driver
def main():
    url = "" #change the url to our latest post
    driver = init()
    login(driver)
    post_time = time_of_recent_post(driver,url)
    brain(driver,post_time)

if __name__ == '__main__':
    main()

