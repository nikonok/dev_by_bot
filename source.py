dev_by_url = 'https://dev.by/registration'

class User:
    def __init__(self, _name, _password):
        self.name = _name
        self.password = _password
        self.email = self.name + '@mailinator.com'

    def __str__(self):
        return self.name + '\t' + self.password + '\t' + self.email


class RegistrationBot:
    path_to_chrome = './chromedriver'
    mailinator = 'https://www.mailinator.com/v2/inbox.jsp'
    file_name = 'nicknames'

    def __init__(self, page, user):
        from selenium import webdriver as wd
        self.wd = wd
        self.user = user
        self.page = page
        self.driver = wd.Chrome(self.path_to_chrome)
        file = open(self.file_name, 'a')
        file.write(str(user) + '\n')


    def registration(self):
        self.driver.get(self.page)

        self.driver.find_element_by_id('user_username').send_keys(self.user.name)
        self.driver.find_element_by_id('user_email').send_keys(self.user.email)
        self.driver.find_element_by_id('user_password').send_keys(self.user.password)
        self.driver.find_element_by_id('user_password_confirmation').send_keys(self.user.password)
        self.driver.find_element_by_id('user_agreement').click()
        self.driver.find_element_by_name('commit').click()

        self.driver.get(self.mailinator)
        self.driver.find_element_by_id('inbox_field').send_keys(self.user.email)
        self.driver.find_element_by_id('inbox_button').click()

        from selenium.webdriver.support.ui import WebDriverWait as Wait
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions as ec

        string_path = '/html/body/main/section/ul/li[@class=\'all_message-item all_message-item-parent cf ng-scope\']'

        Wait(self.driver, 50).until(ec.presence_of_element_located((By.XPATH, string_path)))
        elements = self.driver.find_elements_by_xpath(string_path)
        dev_by = None
        for e in elements:
            if 'Dev.by' in e.text:
                dev_by = e
        dev_by.click()

        Wait(self.driver, 50).until(ec.presence_of_element_located((By.TAG_NAME, 'iframe')))

        frame = self.driver.find_element_by_id('msg_body')
        self.driver.switch_to_frame(frame)
        Wait(self.driver, 50).until(ec.presence_of_element_located((By.TAG_NAME, 'p')))
        self.driver.find_element_by_link_text('подтвердить').click()

        import smtplib
        text = "You nickname = " + self.user.name + "\n\tpassword = " + self.user.password + "\n"
        server = smtplib.SMTP('smtp.gmail.com', 587)  # port 465 or 587
        server.starttls()
        server.login('antonsh90@gmail.com', 'nikonok2016')
        server.sendmail('antonsh90@gmail.com', self.user.email, text)
        server.close()

        self.driver.close()


if __name__ == '__main__':
    from random import choice
    from string import ascii_lowercase
    from sys import argv
    n = 12
    try:
        RegistrationBot.path_to_chrome = argv[2]
    except IndexError:
        pass

    for i in range(int(argv[1])):
        username = ''.join(choice(ascii_lowercase) for _ in range(n))
        user = User(username, username)
        RegistrationBot(dev_by_url, user).registration()

    print("Program finished")
