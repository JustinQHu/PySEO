import unittest
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
from Src.PySEO import GoogleSearchClicker, BaiduSearchClicker, GoogleMobileSearchClicker, BaiduMobileSearchClicker


def matchTitle(kw, items):
    for i, item in zip(range(len(items)), items):
        # 获取每个节点的html,去除里面的标签
        html = item.get_attribute("innerHTML")
        if html.find(kw) != -1:
            item.click()
            return i

    return False


class MyTestCase(unittest.TestCase):


    def test_baidu_search_click(self):
        driver = webdriver.Chrome(executable_path='/Users/huqijun/PycharmProjects/PySEO/bin/chromedriver')
        driver.implicitly_wait(10)
        driver.get("https://www.baidu.com/")
        assert "百度" in driver.title
        elem = driver.find_element_by_name('wd')
        elem.clear()
        elem.send_keys("v2ray 多用户")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source
        items = driver.find_elements_by_tag_name('h3')
        print('items length {}'.format(len(items)))
        for item in items:
            temp = item.text
            print(temp)
            if temp.find('The Hu Post') != -1:
                item.click()

                break

        time.sleep(10)
        driver.close()

    def test_baidu_search_click_next_page(self):
        mission_compelete = False
        driver = webdriver.Chrome(executable_path='/Users/huqijun/PycharmProjects/PySEO/bin/chromedriver')
        driver.implicitly_wait(10)
        driver.get("https://www.baidu.com/")
        assert "百度" in driver.title
        elem = driver.find_element_by_name('wd')
        elem.clear()
        elem.send_keys("v2ray bad request")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source
        # find_element_by_name only works for Google
        # Baidu has some special handling of its search results
        # So here use find_elements_by_tag_name

        while mission_compelete is False:

            items = driver.find_elements_by_tag_name('h3')
            print('items length {}'.format(len(items)))
            for item in items:
                temp = item.text
                print(temp)
                if temp.find('The Hu Post') != -1:
                    item.click()
                    mission_compelete = True
                    break
            next_pages = driver.find_element_by_id('page')
            next_button = next_pages.find_element_by_partial_link_text('下一页')
            next_button.click()

        time.sleep(10)
        driver.close()

    def test_baidu_get_next_buttion(self):
        driver = webdriver.Chrome(executable_path='/Users/huqijun/PycharmProjects/PySEO/bin/chromedriver')
        driver.implicitly_wait(10)
        driver.get("https://www.baidu.com/")
        assert "百度" in driver.title
        elem = driver.find_element_by_name('wd')
        elem.clear()
        elem.send_keys("v2ray伪装 客户端配置")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source

        try:
            next_button = driver.find_element_by_partial_link_text('下一页')
            print("next page button click")
            next_button.click()
        except NoSuchElementException as e:
            print('error occurred {}'.format(e))
        except Exception as e:
            print('error occurred {}'.format(e))

        time.sleep(10)
        driver.close()



    def test_google_search_click(self):
        driver = webdriver.Chrome(executable_path='/Users/huqijun/PycharmProjects/PySEO/bin/chromedriver')
        driver.implicitly_wait(10)
        driver.get("https://www.google.com/")
        assert "Google" in driver.title
        elem = driver.find_element_by_name('q')
        elem.clear()
        elem.send_keys("site:huqijun.org")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source
        # find_element_by_name only works for Google
        # Baidu has some special handling of its search results
        # So here use find_elements_by_tag_name
        items = driver.find_elements_by_tag_name('h3')
        print('items length {}'.format(len(items)))
        for item in items:
            temp = item.text
            print(temp)
            if temp.find('The Hu Post') != -1:
                item.click()

                break

        time.sleep(10)
        driver.close()

    def test_google_search_click_next_page(self):
        mission_compelete = False
        driver = webdriver.Chrome(executable_path='/Users/huqijun/PycharmProjects/PySEO/bin/chromedriver')
        driver.implicitly_wait(10)
        driver.get("https://www.google.com/")
        assert "Google" in driver.title
        elem = driver.find_element_by_name('q')
        elem.clear()
        elem.send_keys("v2ray 多用户")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source
        # find_element_by_name only works for Google
        # Baidu has some special handling of its search results
        # So here use find_elements_by_tag_name

        while mission_compelete is False:

            items = driver.find_elements_by_tag_name('h3')
            print('items length {}'.format(len(items)))
            for item in items:
                temp = item.text
                print(temp)
                if temp.find('The Hu Post') != -1:
                    item.click()
                    mission_compelete = True
                    break
            next_button = driver.find_element_by_id('pnnext')
            next_button.click()

        time.sleep(10)
        driver.close()


    def test_google_search_clicker(self):
        """
        keyword: v2ray 多用户 now appears in the first page of Google search results
        need another test case to test keywords that is not in the first page
        :return:
        """
        GoogleClicker = GoogleSearchClicker('V2ray 多用户', 'The Hu Post', 'Chrome', 'Google')
        GoogleClicker.run()


    def test_google_search_clicker_2(self):
        """
        keyword: c++ vector 初始化	now is in the second page
        :return:
        """
        google_clicker = GoogleSearchClicker('c++ vector 初始化', 'The Hu Post', 'Chrome', 'Google')
        google_clicker.run()

    def test_google_search_clicker2(self):
        """
        keyword: tinystl is now in the 7th page
        :return:
        """
        google_clicker = GoogleSearchClicker('centos7 bbr', 'The Hu Post', 'Chrome', 'Google')
        google_clicker.run()

    def test_baidu_search_clicker(self):
        """
        keyword: v2ray 多用户 now appears in the first page of Baidu search results
        need another test case to test keywords that is not in the first page
        :return:
        """
        baidu_clicker = BaiduSearchClicker('V2ray 多用户', 'The Hu Post', 'Chrome', 'Baidu')
        baidu_clicker.run()


    def test_baidu_search_clicker_2(self):
        """
        keyword: v2ray伪装 客户端配置 now appears in the first page of Baidu search results
        need another test case to test keywords that is not in the first page
        :return:
        """
        baidu_clicker = BaiduSearchClicker('v2ray伪装 客户端配置', 'The Hu Post', 'Chrome', 'Baidu')
        baidu_clicker.run()


    def test_google_mobile_search_clicker(self):
        """
        keyword: v2ray 多用户 now appears in the 2nd page of Google Mobile search results
        need another test case to test keywords that is not in the first page
        :return:
        """
        google_mobile_clicker = GoogleMobileSearchClicker('V2ray 多用户', 'The Hu Post', 'Chrome', 'Google')
        google_mobile_clicker.run()

    def test_baidu_mobile_search_clicker(self):
        """
        keyword: c++vector 指针初始化 now appears in the 4th page of Baidu Mobile search results
        need another test case to test keywords that is not in the first page
        :return:
        """
        baidu_mobile_clicker = BaiduMobileSearchClicker('V2ray 多用户', 'The Hu', 'Chrome', 'Baidu')
        baidu_mobile_clicker.run()

if __name__ == '__main__':
    unittest.main()



