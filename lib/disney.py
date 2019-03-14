import requests
from worker import FileWorker
from bs4 import BeautifulSoup
import time


class Disney:

    def __init__(self, delay):
        
        self.session = requests.session()
        self.run = True
        self.delay = delay
        
        self.startStore()

    def startStore(self):
        try:
    
            f = FileWorker('productStore.json')
            status = f.look()

            if status:
                self.currentStore = f.load()
                if len(self.currentStore) > 0:
                    self.hash = f.hash(f.dump(self.currentStore))
                else:
                    self.hash = []
                print 'Initialized Store: {} Products'.format(len(self.currentStore))
            else:
                f.create()
                self.currentStore = []
                self.hash = []

        except:
            print 'Error in JSON Initialization'
            exit()
    
    def makeQuery(self, query):

        self.query = query

        # THIS METHOD IS NOT WELL TESTED

        uri = 'https://gql.matterhorn.disney.io/graphql/query/autosuggest?query={q}'.format(q=self.query)
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Origin': 'https://www.shopdisney.com',
            'Referer': 'https://www.shopdisney.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        r = self.session.get(uri, headers=headers)

        f = FileWorker('productStore.json')
        newStore = []
        
        d = r.json()
        if not d:
            print 'Error'

        a = d['search']['products']
        
        for t in a:
            itemObj = {}
            itemObj['title']=t['title']
            itemObj['pid']=t['pid']
            itemObj['url']=t['url']
            itemObj['thumb']=t['thumbImage']
            newStore.append(itemObj)

        for item in newStore:
            print 'Checking'
            try:
                self.currentStore.index(item)
            except:
                print 'New item {}'.format(item)
                self.currentStore.append(item)

    def parseVinylHtml(self):
        uri = 'https://www.shopdisney.com/movies-shows/disney/toys?sort=popularity&order=desc&categories=1000284'
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Origin': 'https://www.shopdisney.com',
            'Referer': 'https://www.shopdisney.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        r = self.session.get(uri, headers=headers)

        f = FileWorker('productStore.json')
        
        soup = BeautifulSoup(r.text, features="lxml")

        for product in soup.find_all('div', {'data-entity-type': 'OtiDisneyStoreProduct'}):
            
            gettin_soupy = BeautifulSoup(str(product), features='lxml')
            
            link_el = gettin_soupy.find('a', {'class':'ada-el-focus'})
            img_le = gettin_soupy.find('div', {'class':'bg-image'})
            
            handle = str(link_el.get('href'))
            title = str(img_le.get('title'))
            image = str(img_le.get('data-src'))

            product_store = {'title':title, 'handle':handle, 'image':image}

            try:

                self.currentStore.index(product_store)

            except:

                ## NEW ITEM LOGIC HERE ##

                self.currentStore.append(product_store)

                print 'New Item {}'.format(product_store['title'])


        f.saveStore(f.dump(self.currentStore))

    def startMonitor(self):
        
        while self.run:

            self.parseVinylHtml()

            time.sleep(float(self.delay))
