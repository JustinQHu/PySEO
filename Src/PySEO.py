from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
"""
PySEO by Justin Hu
"""
class SearchClicker:

    search_engines = {
        'Google': {
            'url': 'https://www.google.com/',
            'engine_name': 'Google',
            'search_box_name': 'q',
            'mobile_search_box_name': 'q',
            'next_button_identity': 'Next',
            'mobile_next_button_identity': 'More results'
        },
        'Baidu': {
            'url': 'https://www.baidu.com/',
            'engine_name': '百度',
            'search_box_name': 'wd',
            'mobile_search_box_name': 'word',
            'next_button_identity': '下一页',
            'mobile_first_next_button_identity': 'new-nextpage-only',
            'mobile_next_button_identity': 'new-nextpage'
        }
    }

    browser_drive_path = {
        'Chrome': '/Users/huqijun/PycharmProjects/PySEO/bin/chromedriver'
    }

    mobile_chrome_user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Mobile Safari/537.36"

    def __init__(self, kw, target_identity, browser_name, target_search_engine, mobile_mode=False):
        """
        :param kw:  keyword to search for
        :param target_identity: identity of the target search result
        :param browser_name: which browser to user
        :param target_search_engine: which search engine to use
        :param mobile_mode: use mobile mode or not
        """
        self.kw = kw
        self.target_identity = target_identity
        self.browser_name = browser_name
        self.browser_driver = None
        self.target_search_engine = target_search_engine
        self.mission_completed = False
        self.search_engine = None
        self.mobile_mode = mobile_mode

    def add_mobile_user_agent(self, opt):
        """
        add special mobile user agent for browser(now is chrome)
        :param opt: Option for browser driver
        :return:
        """
        if opt:
            opt.add_argument("user-agent="+self.mobile_chrome_user_agent)

    def init(self):
        """
        init browser driver for Selenium
        :return:
        """
        if self.browser_name in self.browser_drive_path:
            option = None
            if self.browser_name == 'Chrome':
                if self.mobile_mode is True:
                    option = webdriver.ChromeOptions()
                    self.add_mobile_user_agent(option)
                self.browser_driver = webdriver.Chrome(executable_path=self.browser_drive_path[self.browser_name],
                                                       options=option)
            elif self.browser_name == 'Firefox':
                if self.mobile_mode is True:
                    option = webdriver.FirefoxOptions()
                    self.add_mobile_user_agent(option)
                self.browser_driver = webdriver.Firefox(executable_path=self.browser_drive_path[self.browser_name],
                                                        options=option)
            elif self.browser_name == 'Edge':
                self.browser_driver = webdriver.Edge(executable_path=self.browser_drive_path[self.browser_name])
            elif self.browser_name == 'Safari':
                self.browser_driver = webdriver.Safari(executable_path=self.browser_drive_path[self.browser_name])

            self.browser_driver.implicitly_wait(20)
        else:
            print('browser {} not in supported'.format(self.browser_name))
            raise Exception('browser type: {} not supported'.format(self.browser_name))

        if self.target_search_engine in self.search_engines:
            self.search_engine = self.search_engines[self.target_search_engine]
        else:
            print('target search engine: {} not supported'.format(self.target_search_engine))
            raise Exception('target search engine: {} not supported'.format(self.target_search_engine))

    def search(self):
        """
        implementation of search
        works for both Google Search(Desktop) and Baidu Search(Desktop)
        If other search engines requires, please override this method
        :return:
        """
        self.browser_driver.get(self.search_engine['url'])
        if self.search_engine['engine_name'] not in self.browser_driver.title:
            print('not open Google Correctly')
            raise Exception('not open Google Correctly')

        # get search box and input keyword and RETURN
        if self.mobile_mode is False:
            search_box = self.browser_driver.find_element_by_name(self.search_engine['search_box_name'])
        else:
            search_box = self.browser_driver.find_element_by_name(self.search_engine['mobile_search_box_name'])
        search_box.clear()
        search_box.send_keys(self.kw)
        search_box.send_keys(Keys.RETURN)

    def click(self):
        """
        try to find and click what we need by target_identity
        click() must be called after search()
        :return:
        """
        while self.mission_completed is False:
            try:
                item = self.browser_driver.find_element_by_partial_link_text(self.target_identity)
                item.click()
                self.mission_completed = True

            except NoSuchElementException as e:
                # not found in this page, try next page
                print("item not found this page, try next page , {}".format(e))
                self.go_to_next_page()
            except Exception as e:
                print("error occurred, {}".format(e))
                raise e

        # stay on this target page for 10 seconds
        time.sleep(10)
        self.browser_driver.close()

    def go_to_next_page(self):
        """
        implementation of going to next page
        :return:
        """
        try:
            if self.mobile_mode is False:
                next_button = self.browser_driver.find_element_by_partial_link_text(
                    self.search_engine['next_button_identity'])
            else:
                next_button = self.browser_driver.find_element_by_partial_link_text(
                    self.search_engine['mobile_next_button_identity'])

            next_button.click()

        except NoSuchElementException as e:
            # not found in this page, try next page
            print("no next button find , {}".format(e))
            raise e
        except Exception as e:
            print("error occurred, {}".format(e))
            raise e

    def close(self):
        """
        release browser driver
        :return:
        """
        self.browser_driver.quit()

    def run(self):
        """
        execute click and search
        :return:
        """
        self.init()
        self.search()
        self.click()
        self.close()


class GoogleSearchClicker(SearchClicker):
    """
    child class does nothing, but makes code more clear
    Because search_click() in parent class just work to Google Search(Desktop) and Baidu Search(Desktop)
    """
    pass


class GoogleMobileSearchClicker(SearchClicker):
    """
    Google results on mobile devices have no 'Next' button, you just scroll down to see more results
    That's the difference
    """
    def __init__(self, kw, target_identity, browser_name, target_search_engine):
        """
        Google Mobile Search
        :param kw:
        :param target_identity:
        :param browser_name:
        :param target_search_engine:
        """
        super().__init__(kw, target_identity, browser_name, target_search_engine, True)


class BaiduSearchClicker(SearchClicker):
    """
    child class does nothing, but makes code more clear
    Because search_click() in parent class just work to Google Search(Desktop) and Baidu Search(Desktop)
    """
    pass


class BaiduMobileSearchClicker(SearchClicker):
    """
    Baidu mobile search and desktop search have a lof of difference:
        1. baidu mobile has a different search box name from its desktop version
        2. unique next page identity
        3. next page identity in 1st page is different from others
        4. search results different from desktops: no explict <a> tag ,
           otherwise binding <h3> with click() event using JS dynamically
    """
    def __init__(self, kw, target_identity, browser_name, target_search_engine):
        super().__init__(kw, target_identity, browser_name, target_search_engine, True)
        self.page = 1

    def click(self):
        """
        special handling of Baidu Mobile that has lots difference from Baidu Desktop
        :return:
        """
        while self.mission_completed is False:
            try:
                items = self.browser_driver.find_elements_by_tag_name('h3')
                for item in items:
                    if self.target_identity in item.text:
                        item.click()
                        self.mission_completed = True
                        break
                if self.mission_completed is False:
                    # not found in this page, try next page
                    print("item not found this page, try next page , {}".format(e))
                    self.go_to_next_page()

            except NoSuchElementException as e:
                print("error occurred while find h3 element, {}".format(e))
                raise e
            except Exception as e:
                print("error occurred, {}".format(e))
                raise e

        # stay on this target page for 10 seconds
        time.sleep(10)
        self.browser_driver.close()

    def go_to_next_page(self):
        """
        going to next page implemented in Parent class does not work for Baidu Mobile
        Baidu Mobile needs a special version of going to next page implementation
        1. baidu mobile has a different search box name from its desktop version
        2. unique next page identity
        3. next page identity in 1st page is different from others
        4. search results different from desktops: no explict <a> tag ,
           otherwise binding <h3> with click() event using JS dynamically
        :return:
        """
        try:
            if self.page == 1:
                next_button = self.browser_driver.find_element_by_class_name(
                        self.search_engine['mobile_first_next_button_identity'])
            else:
                next_button = self.browser_driver.find_element_by_class_name(
                    self.search_engine['mobile_next_button_identity'])

            next_button.click()
            self.page = self.page + 1

        except NoSuchElementException as e:
            # not found in this page, try next page
            print("no next button find , {}".format(e))
            raise e
        except Exception as e:
            print("error occurred, {}".format(e))
            raise e
