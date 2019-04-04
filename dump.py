from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import json
import time

class SiteDumper(object):
    """docstring for  Google"""
    def __init__(self):
        super(SiteDumper, self).__init__()
        options = ChromeOptions()
        options.add_argument('--headless')
        self.driver = Chrome(options=options)
        self.driver.implicitly_wait(10) # seconds
        self.results = []
        
    def start(self, site_file):
        with open(site_file, 'r') as f:
            data = json.load(f)
        for (index, (name, url)) in enumerate(data['sites']):
            self.dump(url, index)
        self.driver.quit()

    def dump(self, url, index):
        print(url)
        self.driver.get(url)
        time.sleep(2)
        try:
            with open(str(index) + '.html', 'w') as f:
                f.write(self.driver.page_source)
            self.driver.save_screenshot(str(index) + '.png')
            text = self.driver.find_element_by_tag_name('body').text
            with open(str(index) + '.txt', 'w') as f:
                f.write(text)
        except Exception as e:
            raise e

if __name__ == '__main__':
    import sys
    dumper = SiteDumper()
    dumper.start(sys.argv[1])
