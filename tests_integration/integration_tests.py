import datetime
import os
import time
import unittest
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import docs
from tests_integration import img

PATH_TO_TESTS_INTEGRATION_IMG = os.path.join(Path(img.__file__).parent)
PATH_TO_DOCS = os.path.join(Path(docs.__file__).parent)


class TestGenerateDB(unittest.TestCase):
    now_date = None
    chrome_options = None
    browser: webdriver.chrome = None
    base_url: str = None
    random_user: dict[str, str] = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.chrome_options = Options()
        # cls.chrome_options.add_argument("--headless")  # without GUI
        # cls.service = Service(executable_path=r"tests_integration/chromedriver.exe")

        cls.browser = webdriver.Chrome(options=cls.chrome_options)
        cls.base_url = 'http://127.0.0.1:8000/'
        cls.data = {
            'first_name': 'Andrii', 'last_name': 'Sky',
            'username': 'andrii', 'email': 'andrii@gmail.ru',
            'password1': '12345678pP', 'password2': '12345678pP',
        }

    @classmethod
    def tearDownClass(cls) -> None:
        cls.browser.close()
        cls.browser.quit()

    @classmethod
    def create_screenshot(cls, filename) -> None:
        """Create screenshot 'test_01_login_2023.02.25_11.55.17.450565.png' """
        cls.now_date = datetime.datetime.now().strftime("%Y.%m.%d_%H.%M.%S.%f")
        cls.browser.save_screenshot(f"{PATH_TO_TESTS_INTEGRATION_IMG}\\{filename}_{cls.now_date}.png")

    def test_01_log_in(self):
        self.browser.get(self.base_url)
        self.assertEqual(self.browser.title, 'Store')
        self.create_screenshot(self._testMethodName)

        self.browser.find_element(By.XPATH, '//a[@id="log_in"]').click()
        self.assertEqual(self.browser.title, 'Store - Authorization')
        self.create_screenshot(self._testMethodName)

    def test_02_users_register(self):
        # url = 'http://127.0.0.1:8000/users/login/'
        # self.browser.get(self.base_url)
        self.assertEqual(self.browser.title, 'Store - Authorization')
        self.browser.find_element(By.XPATH, '//a[@id="users_register"]').click()
        self.create_screenshot(self._testMethodName)

        self.browser.find_element(By.XPATH, '//input[@id="id_first_name"]').send_keys(self.data['first_name'])
        self.create_screenshot(self._testMethodName)
        self.browser.find_element(By.XPATH, '//input[@id="id_last_name"]').send_keys(self.data['last_name'])
        self.create_screenshot(self._testMethodName)
        self.browser.find_element(By.XPATH, '//input[@id="id_username"]').send_keys(self.data['username'])
        self.create_screenshot(self._testMethodName)
        self.browser.find_element(By.XPATH, '//input[@id="id_email"]').send_keys(self.data['email'])
        self.create_screenshot(self._testMethodName)
        self.browser.find_element(By.XPATH, '//input[@id="id_password1"]').send_keys(self.data['password1'])
        self.create_screenshot(self._testMethodName)
        self.browser.find_element(By.XPATH, '//input[@id="id_password2"]').send_keys(self.data['password2'])
        self.create_screenshot(self._testMethodName)

        self.browser.find_element(By.XPATH, '//input[@class="btn btn-primary btn-block"]').click()

        self.assertEqual(self.browser.title, 'Store - Authorization')
        alert_text = self.browser.find_element(By.XPATH,
                                               '//*[@id="layoutAuthentication_content"]/main/div/div/div/div[1]').text
        self.assertIn('You have successfully registered!', alert_text)
        self.create_screenshot(self._testMethodName)

    def test_03_log_in(self):
        self.browser.find_element(By.XPATH, '//input[@id="id_username"]').send_keys(self.data['username'])
        self.create_screenshot(self._testMethodName)

        self.browser.find_element(By.XPATH, '//input[@id="id_password"]').send_keys(self.data['password1'])
        self.create_screenshot(self._testMethodName)

        self.browser.find_element(By.XPATH, '//input[@id="Login"]').click()
        self.assertEqual(self.browser.title, 'Store')

        alert_text = self.browser.find_element(By.XPATH, '/html/body/section/div/div[1]/div/div').text
        self.assertIn('You have successfully logged in!', alert_text)

        self.create_screenshot(self._testMethodName)

    def test_04_start_shopping_carousel(self):
        self.browser.find_element(By.XPATH, '//a[@id="start-purchase-link"]').click()

        self.browser.find_element(By.XPATH, '/html/body/div/div/div[1]/div/a[1]').click()
        self.create_screenshot(self._testMethodName)

        self.browser.find_element(By.XPATH, '/html/body/div/div/div[1]/div/a[2]').click()
        self.create_screenshot(self._testMethodName)

        self.browser.find_element(By.XPATH, '/html/body/div/div/div[1]/div/a[3]').click()
        self.create_screenshot(self._testMethodName)

        self.browser.find_element(By.XPATH, '/html/body/div/div/div[1]/div/a[4]').click()
        self.create_screenshot(self._testMethodName)

        self.create_screenshot(self._testMethodName)

    def test_05_cart(self):
        self.browser.find_element(By.XPATH, '/html/body/div/div/div[1]/div/a[1]').click()
        self.create_screenshot(self._testMethodName)

        self.browser.find_element(By.XPATH, '//img[@class="card-img-top"]').click()
        self.create_screenshot(self._testMethodName)

    def test_06_add_comment(self):
        add_comment = 'Testing adding a comment'
        self.browser.execute_script("window.scrollTo(0, 1000)")
        self.create_screenshot(self._testMethodName)
        self.browser.find_element(By.XPATH, '//*[@id="id_body"]').send_keys(add_comment)
        self.create_screenshot(self._testMethodName)

        self.browser.find_element(By.XPATH, '//button[@class="btn btn-info"]').click()
        self.create_screenshot(self._testMethodName)

        self.browser.execute_script("window.scrollTo(0, 1000)")
        time.sleep(1)
        self.create_screenshot(self._testMethodName)

        self.browser.find_element(By.XPATH, '//*[@id="comment_like"]').click()
        self.browser.execute_script("window.scrollTo(0, 1000)")
        time.sleep(1)
        self.create_screenshot(self._testMethodName)

        self.browser.find_element(By.XPATH, '//*[@id="comment_like"]').click()
        self.browser.execute_script("window.scrollTo(0, 1000)")
        time.sleep(1)
        self.create_screenshot(self._testMethodName)



if __name__ == '__main__':
    unittest.main()
