#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as ui
from PIL import Image
from pytesseract import image_to_string
from sys import platform
import time

class Bot:
    def parse(self, url):
        if platform == 'linux' or platform == 'linux2':
            self.driver = webdriver.Chrome('dri/linux/chromedriver')
        elif platform == 'win32':
            self.driver = webdriver.Chrome('dri/win32/chromedriver.exe')
        return self.navigate(url)

    def take_screenshot(self):
        self.driver.save_screenshot('avito_screenshot.png')

    def crop(self, location, size):
        image = Image.open('avito_screenshot.png')
        x = location['x']
        y = location['y']
        width = size['width']
        height = size['height']

        image.crop((x - 10, y, x + width, y + height)).save('tel.gif')
        image = Image.open('tel.gif')
        return image_to_string(image)

    def navigate(self, url):
        driver = self.driver
        driver.get(url)

        
        try:
            driver.find_element_by_xpath(
                u"(.//*[normalize-space(text()) and normalize-space(.)='₽'])[3]/following::span[1]"
            ).click()

        except:
           
            try:
                driver.find_element_by_xpath(
                    u"(.//*[normalize-space(text()) and normalize-space(.)='Цена не указана'])[2]/following::span[1]"
                ).click()
            except:
                driver.quit()

        try:
            ui.WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH,
                     u"(.//*[normalize-space(text()) and normalize-space(.)='оферту'])[1]/following::img[2]")))
        except TimeoutException:
            driver.quit()
        

        self.take_screenshot()
        image = self.driver.find_element_by_xpath(
            '//div[@class="item-phone-big-number js-item-phone-big-number"]//*'
        )
        location = image.location
        size = image.size
        driver.quit()
        return self.crop(location, size)
