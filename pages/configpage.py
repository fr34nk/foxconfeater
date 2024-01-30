from pages.page import Page
from enum import Enum

from helpers import el_select
from utilities import dotdict, str_to_boolean

class ConfigType (Enum): 
    NEW = "NEW"
    TOUCHED = "TOUCHED"
    UNTOUCHED = "UNTOUCHED"

class RowConfig ():
    element=None
    # new :: configuration that was not present in the browser
    # touched :: configuration that was changed since last browser initilization
    # untouched :: configuration that was present since last browser intialization
    type=ConfigType
    key=None
    value=None
    def __init__ (self, el):
        el_th = el.find_element("xpath", '//th')
        el_td = el.find_element("xpath", '//td[@class="cell-value"]')
        el_class = el.get_attribute('class')

        if 'has-user-value' in el_class:
            self.type = ConfigType.NEW
        elif 'add' in el_class or 'deleted' in el_class:
            self.type = ConfigType.TOUCHED
        else:
            self.type = ConfigType.UNTOUCHED

        self.element = el
        self.key = el_th.text
        self.value = el_td.text

class ConfigPage (Page):

    def __init__ (self, browser):
        super().__init__(browser)

    def build_row (self, el):
        return RowConfig(el)

    def get_property_element_list (self):
        input_search = el_select(self.browser.driver, 'input', 'id', "about-config-search")

        if input_search:
            el = input_search.value
            el.send_keys('.*')
            el.send_keys(self.browser.Keys.RETURN)

        el_row_list = self.browser.driver.find_elements(self.browser.By.XPATH, '//table/tr')
        if el_row_list and  len(el_row_list) > 0:
            row_list=[]
            for el_row in el_row_list:
                row_list.append(el_row)
        return row_list


    def edit_property (self, property, value):
        row_config = self.get_property_element(property)

        if row_config is None:
            return None

        # TODO: apply treatment for multiple values
        config = RowConfig(row_config[0])

        if config.type == ConfigType.UNTOUCHED or config.type == ConfigType.TOUCHED:
            if type(value) == bool:
                    prop_value = config.element.find_element(self.browser.By.XPATH, '//td[@class="cell-value"]').text
                    boolValue = str_to_boolean(prop_value)
                    if not (boolValue == value):
                        config.element.find_element(self.browser.By.XPATH, '//td[@class="cell-edit"]').click()
                    return True

            if type(value) == str:
                # Form value (need to click to make form appear)
                config.element.find_element(self.browser.By.XPATH, '//td[@class="cell-edit"]').click()
                prop_value = config.element.find_element(self.browser.By.XPATH, '//td[@class="cell-value"]').text

                if not (prop_value == value):
                    input_el = config.element.find_element(self.browser.By.XPATH, '//td[@class="cell-value"]/form/input')
                    input_el.send_keys(value)
                    input_el.send_keys(self.browser.Keys.RETURN)
                    return True

        raise Exception('[Edit_Error] Unsupported property type')

    def get_property_element (self, property):
        input_search = el_select(self.browser.driver, 'input', 'id', 'about-config-search')

        if input_search:
            input_search.value.send_keys(property)
            input_search.value.send_keys(self.browser.Keys.RETURN)

        el_row_list = self.browser.driver.find_elements(self.browser.By.XPATH, '//table/tr')


        if el_row_list and len(el_row_list) > 0:
            row_list=[]
            for el_row in el_row_list:
                th_text = el_row.find_element(self.browser.By.XPATH, '//th').text
                if property in th_text:
                    row_list.append(el_row)

        input_search.value.clear()
        return row_list

    def get_property_value (self, property):
        el = self.get_property_element(property)
        value = el.find_element(self.browser.By.XPATH, '//th')

        if value:
            return value.text

        return None
