from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import json
import time

URL='https://www.google.com/search?q='

class Google(object):
    """docstring for  Google"""
    def __init__(self):
        super(Google, self).__init__()
        options = ChromeOptions()
        options.add_argument('--headless')
        self.driver = Chrome(options=options)
        self.driver.implicitly_wait(10) # seconds
        self.results = []
        
    def scroll_by_element(self, element, offset = 0):
        height = self.driver.execute_script("return arguments[0].offsetHeight;", element)
        height = int(element.get_attribute('offsetHeight'))

        self.driver.execute_script("arguments[0].scrollIntoView();", element)

        if (offset != 0):
            script = "window.scrollTo(0, window.pageYOffset + " + str(offset) + ");"
            self.driver.execute_script(script)

    def query(self, keyword, count=100):
        self.driver.get(URL + keyword)
        try:
            self.handle_search_result(count)
            data = {
                'keyword': keyword,
                'sites': self.results
            }
            with open('sites.json', 'w') as f:
                json.dump(data, f)
        except Exception as e:
            with open('page_source.html', 'w') as f:
                f.write(self.driver.page_source)
            raise e
        finally:
            self.driver.quit()

    def handle_search_result(self, count):
        while len(self.results) < count:
            print(self.driver.current_url)
            anchor_list = self.driver.find_elements_by_css_selector('div.g div.rc > div.r > a')
            for a in anchor_list:
                if a.get_attribute('class') == 'fl':
                    continue  # skip "translate this page" link
                url = a.get_attribute('href')
                if url.find('wikipedia.org/wiki/') >= 0 or url.find('kotobank.jp/word/') >= 0:
                    continue
                name = ''
                try:
                    h3 = a.find_element_by_tag_name('h3')
                    name = h3.text
                except Exception as e:
                    outerHTML = self.driver.execute_script("return arguments[0].outerHTML;", a)
                    print(outerHTML)
                # print(name, url)
                self.results.append((name, url))
                if len(self.results) >= count:
                    break
            else:
                if not self.goto_next_page():
                    print('No more result (count={})'.format(len(self.results)))
                    break

    def goto_next_page(self):
        # page_anchors = self.driver.find_elements_by_css_selector('table#nav a.fl')
        # last_page = int(page_anchors[-1].text)
        # if cur >= last_page:
        #     print('Reached to the last page {}'.format(last_page))
        #     break
        # cur += 1
        try:
            next_page = self.driver.find_element_by_css_selector('a#pnnext')
            self.scroll_by_element(next_page)
            print('Going to the next page (count={})'.format(len(self.results)))
            next_page.click()
            return True
        except NoSuchElementException as e:
            return False


if __name__ == '__main__':
    import sys
    google = Google()
    count = 100
    if len(sys.argv) >= 3:
        count = int(sys.argv[2])
    google.query(sys.argv[1], count)
