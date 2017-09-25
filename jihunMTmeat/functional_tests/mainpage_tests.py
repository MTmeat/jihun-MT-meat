import time

from fixture_tests import browser, BASE_URL

from selenium.webdriver.common.keys import Keys


def test_main_page(browser):
    browser.get(BASE_URL)

    assert BASE_URL + "/" == browser.current_url


def test__select_meat_count(browser):
    browser.get(BASE_URL)

    browser.find_element_by_xpath("//input[@name='삼겹']").clear()
    browser.find_element_by_xpath("//input[@name='삼겹']").send_keys('5')
    browser.find_element_by_xpath("//input[@name='목살']").clear()
    browser.find_element_by_xpath("//input[@name='목살']").send_keys('4')

    browser.find_element_by_xpath("//input[@type='submit']").send_keys(Keys.ENTER)

    assert browser.current_url == BASE_URL + '/ordermeats/new/'
    assert browser.find_element_by_xpath("//input[@name='삼겹']").get_attribute('value') == '5'
    assert browser.find_element_by_xpath("//input[@name='목살']").get_attribute('value') == '4'




