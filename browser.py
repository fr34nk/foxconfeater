from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from helpers import el_select
from utilities import dotdict, str_to_boolean

class Browser():
    driver=None
    Keys=None
    By=None

    def __init__ (self):
        firefox_opts = Options
        # firefoxOpts.add_argument('--headless')
        geckoManager = GeckoDriverManager()
        driver_path = geckoManager.install()

        driver = webdriver.Firefox(service=FirefoxService(driver_path))
        self.driver = driver
        self.Keys = Keys
        self.By = By
