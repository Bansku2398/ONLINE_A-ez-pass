from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from time import sleep

import config


class EasyPass:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.binary_location = r"C:\Users\micha\AppData\Local\Google\Chrome\Application\chrome.exe"
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.login()
        self.tests_to_do = self.get_list_of_tests_from_file()
        self.list_of_tests_url = self.get_list_of_test_url()
        self.open_list_of_tests()
        self.solve_tests()

    def solve_tests(self):
        for test in self.tests_to_do:
            try:
                link = self.get_test_link(test)
            except AttributeError:
                continue
            if link is None:
                continue
            self.driver.get(link)
            self.find(By.XPATH, "//button[contains(text(), 'Spustit nový odpovědník')]").click()
            self.find(By.XPATH, "//button[contains(text(), 'Odevzdat')]").click()
            self.find(By.LINK_TEXT, "Prohlídka").click()
            answers = self.driver.find_elements(By.XPATH, "//span[@class='ok']")
            answers = [answer.text[1:-1].split(',')[0].strip() for answer in answers]
            self.find(By.XPATH, "//a[contains(text(), 'Zpět')]").click()
            self.find(By.XPATH, "//button[contains(text(), 'Spustit nový odpovědník')]").click()
            cells = self.driver.find_elements(By.XPATH, "//input[@type='text']")
            for i, cell in enumerate(cells):
                cell.send_keys(answers[i])
            self.find(By.XPATH, "//button[contains(text(), 'Odevzdat')]").click()
            sleep(1)
            self.open_list_of_tests()

    def get_list_of_test_url(self):
        self.driver.get(config.student_page)
        self.find(By.XPATH, "//a[span/strong[contains(text(), 'ONLINE_A')]]").click()
        self.find(By.XPATH, ".//div[@class='row student_row_b']/div/a")
        link = self.driver.find_elements(By.XPATH, ".//div[@class='row student_row_b']/div/a")[-2].get_attribute("href")
        return link

    def open_list_of_tests(self):
        self.driver.get(self.list_of_tests_url)

    def login(self):
        self.driver.get(config.login_url)

        elem = self.driver.find_element(By.NAME, "credential_0")
        elem.send_keys(config.UCO)

        elem = self.driver.find_element(By.NAME, "credential_1")
        elem.send_keys(config.primary_password)
        elem.send_keys(Keys.RETURN)

    def find(self, by_method, pattern, wait_time=10):
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((by_method, pattern))
            )
            return element
        except:
            self.driver.quit()

    def get_list_of_tests_from_file(self):
        with open("tests.txt", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines()]

    def get_test_link(self, test):
        element = self.find(By.XPATH, f"//*[@id=\"vyber_odpovedniku_body\"]/div/div/div/div[2]/div/table/tbody//tr["
                                      f"td/a[contains(text(), '{test}')]]")
        try:
            points = element.find_element(By.XPATH, "td/div/div/span[@class='pozn_blok']")
            if points.text != "*0":
                return
            test_link = points.find_element(By.XPATH, "../../../../td[@class='uzel']/a").get_attribute("href")
            return test_link
        except NoSuchElementException:
            test_link = element.find_element(By.XPATH, "td[@class='uzel']/a").get_attribute("href")
            return test_link


a = EasyPass()
sleep(5)
a.driver.quit()
