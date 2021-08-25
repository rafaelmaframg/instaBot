from selenium import webdriver
import credentials as cr
import sqlite3
from time import sleep

class Bot:
    def __init__(self):
        self.login(cr.username, cr.password)
        self.home()
        self.seguidores = self.followers('seguidores')
        self.seguindo = self.followers('seguindo')
        self.unfollow = []
        print(len(self.seguindo))
        print(len(self.seguidores))
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
        sleep(5)

    def followers(self, item):
        #captura lista com de acordo com o parametro 'item' especificado 'followers' 'following'

        self.driver.find_element_by_partial_link_text(item).click()
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

        users = self.driver.find_elements_by_css_selector("._0imsa")
        self.followers_list = []

        for user in users:
            each = user.text
            self.followers_list.append(each)

        print(f"{item} have been successfully received.")
        sleep(2)
        self.driver.find_element_by_xpath('/html/body/div[6]/div/div/div[1]/div/div[2]/button').click()
        return self.followers_list

    def addFollower(self):
        #adiciona no bd do sqlite os usuarios capturados pela lista da função anterior

        db = sqlite3.connect("followers.sqlite")
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS followers(username TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS following(username TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS unfollow(username TEXT)")
        cursor.execute("DELETE FROM followers")
        cursor.execute("DELETE FROM following")
        cursor.execute("DELETE FROM unfollow")
        db.commit()

        #adiciona ao bd cada pessoa da lista de followers
        for seguidor in self.seguidores:
            cursor.execute("INSERT INTO followers VALUES(?)", (seguidor,))
            db.commit()

        #captura e adiciona a lista cada pessoa na lista de following e realiza verificação
        # se a pessoa o segue de volta e adiciona a outra lista e BD
        for seguindo in self.seguindo:
            cursor.execute("INSERT INTO following VALUES(?)", (seguindo,))
            if seguindo not in self.seguidores:
                self.unfollow.append(seguindo)
                cursor.execute("INSERT INTO unfollow VALUES(?)", (seguindo,))
            db.commit()

        db.close()
        print("Process completed. You can close the program and browse the database.")


def main():
    mybot = Bot()

if __name__ == '__main__':
    main()
