from fixture_tests import browser, BASE_URL


def test__main_page(browser):
    browser.get(BASE_URL)

    assert BASE_URL + "/" == browser.current_url
