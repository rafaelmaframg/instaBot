from selenium import webdriver
from time import sleep

class Bot():
    def __init__(self):
        self.login('user', 'password')

    def login(self, username, password):
        self.driver = webdriver.Chrome('chromedriver.exe')
        self.driver.get('https://www.instagram.com/accounts/login/?hl=en')
        sleep(2)
        cook = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/button[1]')
        cook.click()
        sleep(5)
        user_name_input = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
        user_name_input.send_keys(username)
        user_password = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
        user_password.send_keys(password)
        sleep(2)
        self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button').click()
        sleep(7)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
        sleep(5)
        self.driver.find_element_by_xpath('//button[contains(text(), "Agora não")]').click()
        sleep(1)
    def home(self):
        self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/span').click()
        sleep(1)
        self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div[2]/div[2]/a[1]').click()
        sleep(1)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/ul/li[2]').click()

def main():
    mybot = Bot()

if __name__ == '__main__':
    main()
