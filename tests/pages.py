from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from allure import step


class LoginPage:
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.wait = WebDriverWait(webdriver, 10, 0.5)

    @step("Войти пользователем {username}")
    def login(self, username, password):
        self.webdriver.find_element(By.ID, "identifierId").send_keys(username)
        self.webdriver.find_element(By.ID, "identifierNext").click()
        password_field = self.wait.until(lambda wd: wd.find_element(By.ID, "password"))
        password_field.find_element(By.TAG_NAME, "input").send_keys(password)
        self.webdriver.find_element(By.ID, "passwordNext").click()
        return MainPage(self.webdriver)


class MainPage:
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.wait = WebDriverWait(webdriver, 10, 0.5)

    @step("Написать сообщение")
    def open_write_message(self):
        self.wait.until(
            lambda wd: self.webdriver.find_element(By.XPATH,
                                                   "//div[@role = 'button' and . = 'Написать']")).click()
        dialog = self.wait.until(
            lambda x: self.webdriver.find_element(By.XPATH, "//div[@role = 'dialog']"))
        return WriteMessageDialog(dialog)

    def get_notification(self):
        return GmailNotification(self.webdriver)

    def get_alert(self):
        return AlertDialog(self.webdriver)


class WriteMessageDialog:
    def __init__(self, element):
        self.element = element
        self.webdriver = element.parent
        self.wait = WebDriverWait(self.webdriver, 10, 0.5)

    @step("Заполнить сообщение для [{to}] c  темой [{subject}] и телом [{body}]")
    def fill_message(self, to, subject, body):
        self.element.find_element(By.XPATH, "//form//textarea[@name = 'to']").send_keys(to)
        self.element.find_element(By.XPATH, "//form//input[@name = 'subjectbox']").send_keys(subject)
        self.element.find_element(By.XPATH, "//div[@role = 'textbox' and @aria-label = 'Тело письма']").send_keys(
            body)
        return self

    @step("Отправить сообщение")
    def send_message(self):
        self.element.find_element(By.XPATH, "//div[@role = 'button' and . = 'Отправить']").click()


class GmailNotification:
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.element = webdriver.find_element(By.XPATH, "//div[@role = 'alert']")
        self.wait = WebDriverWait(webdriver, 10, 0.5)

    @step("Проверить, что сообщение отправлено")
    def check_message_send(self):
        self.wait.until(lambda x: self.element.is_displayed())
        assert self.wait.until(lambda x: self.element.find_element(By.XPATH, "//span[. = 'Письмо отправлено.']"))


class AlertDialog:
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.element = webdriver.find_element(By.XPATH, "//div[@role = 'alertdialog']")
        self.wait = WebDriverWait(webdriver, 10, 0.5)

    @step("Проверить, что получена ошибка {message}")
    def check_error_message(self, message):
        self.wait.until(lambda x: self.element.is_displayed())
        assert self.wait.until(lambda x: self.element.find_element(By.XPATH, "div[. = '" + message + "']"))
