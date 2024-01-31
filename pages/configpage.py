from pages.page import Page
from enum import Enum

from helpers import el_select
from utilities import dotdict, str_to_boolean
from exceptions.attribute import PropertyExceptionCode, PropertyException

class ConfigType (Enum): 
    NEW_USER_PROPERTY = "NEW_USER_PROPERTY"
    CHANGED = "CHANGED"
    UNTOUCHED = "UNTOUCHED"

class RowConfig ():
    element=None
    type=ConfigType
    key=None
    value=None
    def __init__ (self, elrow):
        el_th = elrow.find_element("xpath", './th')
        el_td = elrow.find_element("xpath", './td[contains(@class, "cell-value")]')
        el_class = elrow.get_attribute('class')

        self.element = elrow
        self.key = el_th.text

        if 'has-user-value' in el_class:
            self.type = ConfigType.CHANGED
            self.value = el_td.text
        elif 'add' in el_class or 'deleted' in el_class:
            self.type = ConfigType.NEW_USER_PROPERTY
        else:
            self.type = ConfigType.UNTOUCHED
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

    def input_search (self, term):
        input_search = el_select(self.browser.driver, 'input', 'id', 'about-config-search')
        if input_search:
            input_search.value.send_keys(term)
            input_search.value.send_keys(self.browser.Keys.RETURN)

    def input_search_clear (self):
        input_search = el_select(self.browser.driver, 'input', 'id', 'about-config-search')
        input_search.value.clear()

    def edit_property (self, property, value):
        row_config = self.find_property_element(property)
        if row_config is None:
            return None

        config = RowConfig(row_config[0])

        if config.type == ConfigType.UNTOUCHED or \
            config.type == ConfigType.CHANGED:
            if type(str_to_boolean(value)) == bool:
                current_prop_value = str_to_boolean(config.value)
                boolValue = str_to_boolean(value)
                if not (boolValue == current_prop_value):
                    config.element.find_element(self.browser.By.XPATH, '//td[@class="cell-edit"]').click()
                return True

            if type(value) == str:
                # Form value (need to click to make form appear)
                edit_button = config.element.find_element(self.browser.By.XPATH, './td[contains(@class, "cell-edit")]')
                edit_button.click()

                cur_value = config.element.find_element(self.browser.By.XPATH, './td[contains(@class, "cell-value")]/form/input').get_attribute('value')


                if not (cur_value == value):

                    input_el = config.element.find_element(self.browser.By.XPATH, './td[contains(@class,"cell-value")]/form/input')
                    # breakpoint()
                    if (value == ''):
                        input_el.clear() 
                    else: 
                        input_el.send_keys(value)

                    edit_button.click()
                    # input_el.send_keys(self.browser.Keys.RETURN)
                return True

        elif config.type == ConfigType.NEW_USER_PROPERTY:
            pass

        raise Exception('[Edit_Error] Unsupported property type')

    def search_and_edit_property (self, property, value):
        try:

            self.input_search(property)
            self.edit_property(property, value)

        except Exception as e:
            return None
        finally:
            self.input_search_clear()

    def search_and_get_property_value (self, property):
        value=None
        new_value=False
        try:
            self.input_search(property)
            elrows = self.find_property_element(property)

            if len(elrows) == 0:
                raise PropertyException(PropertyExceptionCode.PROPERTY_NOT_FOUND)
            # TODO Treatment
            elrow = elrows[0]

            row_config = RowConfig(elrow)
            if row_config.type == ConfigType.CHANGED:
                value = row_config.value
            elif RowConfig(elrow).type == ConfigType.NEW_USER_PROPERTY:
                value = row_config.value
                new_value = True
            elif RowConfig(elrow).type == ConfigType.UNTOUCHED:
                value = row_config.value
            else: 
                raise PropertyException(PropertyExceptionCode.PROPERTY_NOT_RECOGNIZED)

        except Exception as e:
            if not isinstance(e, PropertyException):
                raise e
        finally:
            self.input_search_clear()

        return dotdict({
            "value": value,
            "new_value": new_value
        })

    def find_property_element (self, property):
        el_row_list = self.browser.driver.find_elements(self.browser.By.XPATH, '//table/tr[not(contains(@class, "hidden"))]')

        if el_row_list and len(el_row_list) > 0:
            row_list=[]
            for el_row in el_row_list:
                th_text = el_row.find_element(self.browser.By.XPATH, './th').text

                if property in th_text:
                    row_list.append(el_row)

        return row_list
