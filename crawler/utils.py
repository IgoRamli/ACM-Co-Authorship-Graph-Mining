from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import numpy as np

TIMEOUT = 30

class DriverUtil():
    def __init__(self, driver):
        self.driver = driver

    def scroll(self, height):
        '''
        Scroll in Selenium
        '''
        self.driver.execute_script("window.scrollTo(0, {})".format(height))


    def get_single_element(self, xpath):
        '''
        Get single element by xpath in Selenium
        '''
        # WebDriverWait(self.driver, TIMEOUT).until(
        #     EC.presence_of_element_located((By.XPATH, xpath)))
        return self.driver.find_element(By.XPATH, xpath)


    def get_multiple_element(self, xpath):
        '''
        Get multiple element by xpath in Selenium
        '''
        # WebDriverWait(self.driver, TIMEOUT).until(
        #     EC.presence_of_all_elements_located((By.XPATH, xpath)))
        return self.driver.find_elements(By.XPATH, xpath)


    def get_text(self, element):
        '''
        Extract text of an element in Selenium
        '''
        return self.driver.execute_script("return arguments[0].innerText;", element)


    def get_content(self, xpath):
        '''
        Extract text of an element that is selected by xpath in Selenium
        '''
        return self.get_text(self.get_single_element(xpath))