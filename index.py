import os
from browser import Browser
from time import localtime
from exceptions.attribute import PropertyException, PropertyExceptionCode

from pages.initialpage import InitialPage
from pages.configpage import ConfigPage

dir_path = os.path.dirname(os.path.realpath(__file__))

OUTPUT_DIR= dir_path
LOG_ERROR_FILE = OUTPUT_DIR + '/error.txt'
FINAL_CONFIG_FILENAME_PREFIX = 'property_config'

NEW_PROPERTIES_ADDED_FILENAME_PREFIX = 'new_properties'

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
            configPage.search_and_edit_property(prop, value)
        except Exception as e:
            with open(LOG_ERROR_FILE, mode='w+') as error_file:
                if isinstance(e, PropertyException): 
                    if PropertyException.code == PropertyExceptionCode.PROPERTY_NOT_RECOGNIZED or \
                         PropertyException.code == PropertyExceptionCode.PROPERTY_NOT_FOUND:
                        error_msg='[UnknownProperty] property: {}'
                        error_file.write(error_msg.format(prop))
                        print(e)
                    if PropertyException.code == PropertyExceptionCode.PROPERTY_VALUE_ERROR:
                        error_msg='[CouldNotGetValue] property: {}. Exception: {}'
                        error_file.write(error_msg.format(prop, e.__str__))
                        print(e)
                    if PropertyException.code == PropertyExceptionCode.PROPERTY_NOT_RECOGNIZED:
                        print(e)

                else:
                    error_msg='[PropertyEditError] property: {}, value: {}'
                    error_file.write(error_msg.format(prop, value))

                    error_file.write(str(e))

    prop_state={}
    new_properties={}
    for [prop,value] in list(config.items()):
        try:
            result = configPage.search_and_get_property_value(prop)

            if result.new_value == True:
                new_properties[prop]=result.value

            if result.value != None:
                prop_state[prop]=result.value

        except Exception as e:
            print('Could not get prop {}'.format(prop))
            print(e)

    save_file_with_time_suffix(
        FINAL_CONFIG_FILENAME_PREFIX,
        json.dumps(prop_state, indent=4)
    )
    save_file_with_time_suffix(
        NEW_PROPERTIES_ADDED_FILENAME_PREFIX,
        json.dumps(new_properties, indent=4)
    )

def save_file_with_time_suffix (filename_prefix, content):
    now = localtime()
    config_state_filename=filename_prefix \
        + '_{}{}{}_{}{}{}.json'.format(
            str(now.tm_year).zfill(2), 
            str(now.tm_mon).zfill(2), 
            str(now.tm_mday).zfill(2), 
            str(now.tm_hour).zfill(2),
            str(now.tm_min).zfill(2),
            str(now.tm_sec).zfill(2),
        )

    with open(config_state_filename, 'w+') as f:
        f.write(content)
        f.close()

main()
