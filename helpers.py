from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from utilities import dotdict



def el_select (driver, el_type=None, el_attr=None, el_attr_value=None, opts={}):
    """Select elements based on type,attr,attr_value
    - sub selections can be applyied: with_parent, with sibbling
    """

    eltype=el_type or "*"
    if el_attr is not None and el_attr_value is not None:
        xpath_selector = '//{}[@{}=\"{}\"]'.format(eltype, el_attr, el_attr_value)
    else:
        xpath_selector = '//{}'.format(eltype)

    el = driver.find_element(By.XPATH, xpath_selector)

    if not el: return None

    def with_sibling (el_type, el_attr, el_attr_value, el=el):
        parent = el.find_element(By.XPATH, '..')
        try:
            parent.find_element(By.XPATH, "//{}[@{}=\"{}\"]".format(el_type, el_attr, el_attr_value))
        except NoSuchElementException:
            return None
        return dotdict({ "value": el })

    def with_parent (el_type, el_attr, el_attr_value, el=el):
        parent = el.find_element(By.XPATH, '..[@{}=\"{}\"]'.format(el_attr, el_attr_value))
        if parent:
            return dotdict({ "value": el })
        else:
            return None

    return dotdict({
        "value": el,
        "with_sibling": with_sibling,
        "with_parent": with_parent
    })


