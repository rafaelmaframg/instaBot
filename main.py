from selenium import webdriver
import sqlite3
from time import sleep

class Bot():
    def __init__(self):
        self.login('user', 'password')
        self.home()
        self.followers()
        self.addFollower()

    def login(self, username, password):
        #login function
        self.driver = webdriver.Chrome('chromedriver.exe')
        self.driver.get('https://www.instagram.com/accounts/login/?hl=en')
        sleep(2)
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/button[1]').click() #Aceita os cookies do navegador
        sleep(5)
        user_name_input = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
        user_name_input.send_keys(username)
        user_password = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
        user_password.send_keys(password)
        sleep(2)
        self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button').click() #Login button
        sleep(7)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click() #Not now
        sleep(5)
        self.driver.find_element_by_xpath('//button[contains(text(), "Agora não")]').click() #Not now
        print("Successfully Logged In!")
        sleep(1)

    def home(self):
        #realiza acesso a pagina inicial do profile

        self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/span').click()
        sleep(1)
        self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div[2]/div[2]/a[1]').click()
        sleep(7)

    def followers(self):
        #captura lista com os seguidores do perfil

        self.driver.find_element_by_partial_link_text('seguidores').click()
        sleep(3)
        jscommand = """ 
        followers = document.querySelector(".isgrP");
        followers.scrollTo(0, followers.scrollHeight);
        var lenOfPage=followers.scrollHeight;
        return lenOfPage;
        """

        self.lenPage = self.driver.execute_script(jscommand)
        self.match = False
        while (self.match == False):
            self.lastCount = self.lenPage
            sleep(1)
            self.lenPage = self.driver.execute_script(jscommand)
            if self.lastCount == self.lenPage:
                self.match = True

        sleep(2)

        db = sqlite3.connect("followers.sqlite")
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS followers(username TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS unfollow(username TEXT)")
        db.close()

        users = self.driver.find_elements_by_css_selector("._0imsa")
        self.followers_list = []

        for user in users:
            each = user.text
            self.followers_list.append(each)

        print(self.followers_list)
        print("Followers have been successfully received.")
        sleep(2)

    def addFollower(self):
        #adiciona no bd do sqlite os usuarios capturados pela lista da função anterior

        db = sqlite3.connect("followers.sqlite")
        cursor = db.cursor()

        select = "SELECT * FROM followers"
        cursor.execute(select)
        dbRead = cursor.fetchall()

        for item in dbRead:
            if item[0] in self.followers_list:
                self.followers_list.pop(self.followers_list.index(item[0]))
            else:
                delData = "DELETE FROM followers WHERE username = ?"
                cursor.execute(delData, (item[0],))
                db.commit()

                insData = "INSERT INTO unfollow VALUES(?)"
                cursor.execute(insData, (item[0],))
                db.commit()
                print(f"{item[0]} has stopped following you!")

        for i in self.followers_list:
            selData = "SELECT * FROM unfollow WHERE username = ?"
            cursor.execute(selData, (i,))
            result = cursor.fetchall()

            if len(result) > 0:
                delData2 = "DELETE FROM unfollow WHERE username = ?"
                cursor.execute(delData2, (i,))
                db.commit()

            insData2 = "INSERT INTO followers VALUES(?)"
            cursor.execute(insData2, (i,))
            db.commit()
            print(f"New follower: {i}")

        db.close()
        print("Process completed. You can close the program and browse the database.")

def main():
    mybot = Bot()

if __name__ == '__main__':
    main()
