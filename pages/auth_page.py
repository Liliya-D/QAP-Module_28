from .base_page import BasePage
from .locators import AuthLocators


class AuthPage(BasePage):

    def __init__(self, driver, timeout=10, ):
        super().__init__(driver, timeout)
        url = 'https://b2c.passport.rt.ru'
        driver.maximize_window()
        driver.get(url)

        self.tub_phone = driver.find_element(*AuthLocators.tub_phone)
        self.active_tub_phone = driver.find_element(*AuthLocators.active_tub_phone)
        self.tub_email = driver.find_element(*AuthLocators.tub_email)
        self.email = driver.find_element(*AuthLocators.auth_email)
        self.pass_eml = driver.find_element(*AuthLocators.auth_pass_eml)
        self.btn_enter = driver.find_element(*AuthLocators.auth_btn_enter)
        self.tub_login = driver.find_element(*AuthLocators.tub_login)
        self.login = driver.find_element(*AuthLocators.auth_login)
        self.pass_log = driver.find_element(*AuthLocators.auth_pass_log)
        self.tub_ls = driver.find_element(*AuthLocators.tub_ls)
        self.placeholder_name = driver.find_element(*AuthLocators.placeholder_name)
        self.forgot_password_link = driver.find_element(*AuthLocators.forgot_password_link)
        self.register_link = driver.find_element(*AuthLocators.register_link)
        self.page_right = driver.find_element(*AuthLocators.page_right)
        self.page_left = driver.find_element(*AuthLocators.page_left)
        self.card_of_auth = driver.find_element(*AuthLocators.card_of_auth)
        self.menu_tub = driver.find_element(*AuthLocators.menu_tub)
        self.agree = driver.find_element(*AuthLocators.agree)
        self.ok_btn = driver.find_element(*AuthLocators.ok_btn)
        self.vk_btn = driver.find_element(*AuthLocators.vk_btn)
        self.mail_btn = driver.find_element(*AuthLocators.mail_btn)
        self.ya_btn = driver.find_element(*AuthLocators.ya_btn)

    def find_other_element(self, by, location):
        return self.driver.find_element(by, location)

class CodeForm(BasePage):
    def __init__(self, driver, timeout=5):
        super().__init__(driver, timeout)
        url = 'https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?response_type=' \
              'code&scope=openid&client_id=lk_b2c&redirect_uri=https%3A%2F%2Flk.rt.ru%2Fsso-' \
              'auth%2F%3Fredirect%3Dhttps%253A%252F%252Flk.rt.ru%252F&state=%7B%22uuid%22%3A%226E714FE0-102A-4B02' \
              '-8629-2B910304A131%22%7D'

        driver.get(url)

        self.address = driver.find_element(*AuthLocators.address)
        self.code_btn = driver.find_element(*AuthLocators.code_btn)

    def get_click(self):
        self.code_btn.click()