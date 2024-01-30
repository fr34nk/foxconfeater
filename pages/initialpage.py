from pages.page import Page

from helpers import el_select
from utilities import dotdict, str_to_boolean

class InitialPage(Page):
    driver=None

    def goto_config_page (self):
        """Removes configuration for warning and go to config list"""
        driver = self.browser.driver
        print(driver)

        driver.get("about:config")
        el_checkbox = el_select(driver, 'input', 'id', "showWarningNextTime")\
            .with_sibling('label', 'for', 'showWarningNextTime')

        if not el_checkbox: 
            pass
        else:
            checkbox = el_checkbox.value
            assert checkbox and checkbox.is_selected()
            checkbox.click() 

        el_button = el_select(driver, None, 'id', 'warningButton')
        if el_button:
            el_button.value.click()
        else:
            raise Exception("Could nof find button to continue to config page")

