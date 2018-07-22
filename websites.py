from BeautifulSoup import BeautifulSoup
import urllib2
import re
from threads import ScanQue, Thread
from time import sleep
import ssl



class Url(object):
    def __init__(self, url):
        self.url = url
        self.header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                  'Accept-Encoding': 'none',
                  'Accept-Language': 'en-US,en;q=0.8',
                  'Connection': 'keep-alive'}
        self.threads_pool = ScanQue()


    def get_link_number(self):
        ssl._create_default_https_context = ssl._create_unverified_context
        req = urllib2.Request(self.url, headers=self.header, unverifiable=True)
        try:
            html_page = urllib2.urlopen(req)
            soup = BeautifulSoup(html_page)
            urls = []
            for url in soup.findAll('a'):
                urls.append(url.get('href'))
            self.links = urls
            return {"The number of links ": "{}".format(len(self.links))}
        except ValueError:
            return "The URL: {} is invalid".format(self.url)

    def check_if_valid(self, url):
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if type(url) in [str, unicode]:
            return re.match(regex, url)
        else:
            return None

    def func_to_thread(self,link):
        print(link)
        try:
            req = urllib2.Request(link, headers=self.header)
            response = urllib2.urlopen(req)
            if response:
                if response.code in [400, 404, 403, 408, 409, 501, 502, 503]:
                    return 1
        except:
            return 1



    def check_for_broken_links(self):
        first = True
        while(not self.threads_pool.end):
            if first:
                counter = []
                for link in self.links:
                    if self.check_if_valid(link):
                        counter.append(link)
                        self.threads_pool.ls.add(link)
                self.threads_pool.last_send = True
            first = False
            sleep(0.5)
        return True


    def run(self):
        Thread(target=self.threads_pool.run_process, args=(tuple([self.func_to_thread]))).start()
        self.get_link_number()
        res = self.check_for_broken_links()
        return {"URL": "{}".format(self.url), "The number of links": len(self.links), "The number of broken links": self.threads_pool.result}












if __name__ == '__main__':
    o = Url('http://www.one.co.il/')
    print(o.run())








