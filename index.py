import os
from uu import Error 
from browser import Browser
from time import sleep

from pages.initialpage import InitialPage
from pages.configpage import ConfigPage

dir_path = os.path.dirname(os.path.realpath(__file__))

LOG_ERROR_FILE= dir_path + '/error.txt'

import json

def main ():
    try:
        config_file = open('./config.json')
        config = json.load(config_file)
    except Exception as e:
        raise Exception('Problem reading config file: ', e)

    browser = Browser()

    initialPage = InitialPage(browser)
    initialPage.goto_config_page()

    configPage = ConfigPage(browser)

    for [prop,value] in list(config.items()):
        try:
            configPage.edit_property(prop, value)
        except Exception as e:
            with open(LOG_ERROR_FILE, mode='w+') as error_file:
                error_msg='[PropertyEditError] property: {}, value: {}'
                error_file.write(error_msg.format(prop, value))
                error_file.write(str(e))


    for [prop,value] in list(config.items()):
        try:
            value = configPage.get_property_value(prop, value)

        except Exception as e:
            print('Could not get prop {} config'.format(prop))

main()
