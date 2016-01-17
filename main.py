from splinter import Browser
import sys
import time
import datetime

origin = 'CHI'
# airports = ['PAR', 'BRU', 'CRL', 'AMS', 'RTM', 'EIN', 'LON']
airports = ['PAR', 'BRU', 'AMS', 'LON']
flights = {
    'price': 2000,
    'url': ''
}
# url = "http://www.kayak.com/flights/CHI-PAR/2016-07-14/BRU-CHI/2016-07-26"
date_start = []
date_init = '2016-07-11'
d1 = datetime.datetime.strptime(date_init, "%Y-%m-%d").date()
for i in range(12):
    date_start.append(d1 + datetime.timedelta(days=i+1))

# date_start = ['2016-07-11', '2016-07-12', '2016-07-13', '2016-07-14', '2016-07-15', '2016-07-16', '2016-07-17', '2016-07-18', '2016-07-19', '2016-07-20', '2016-07-21'];

data = []

def wait_for(secs):
    print 'sleep for ', secs
    for i in range(secs):
        print '.'
        time.sleep(1)
    print 'awake'

with Browser() as browser:

    for date_a in date_start:

        # date_a = datetime.datetime.strptime(d1, "%Y-%m-%d").date()
        date_b = date_a + datetime.timedelta(days=10)

        for i in range(len(airports)-1):
            for j in range(len(airports)):
                if i >= j:
                    continue
                airp_a = airports[i]
                airp_b = airports[j]
                url = 'http://www.kayak.com/flights/' + origin + '-' + airp_a + '/' + date_a.strftime('%Y-%m-%d') + '/' + airp_b + '-' + origin + '/' + date_b.strftime('%Y-%m-%d')
                print url
                # break
                browser.visit(url)
                wait_for(5)

                if browser.is_element_present_by_css('.results_price', wait_time=10):
                    print '\t.results_price found'
                    prices = []
                    for item in browser.find_by_css('.results_price'):
                        try:
                            print '\tsaving price', item.text
                            prices.append(item.text)
                        except:
                            print '\texcept'
                            pass
                            # print "Unexpected error:", sys.exc_info()[0]
                    data.append({
                        'url': url,
                        'prices': prices
                    })
                break
                wait_for(30)
            break
        break

    for item in data:
        for price in item['prices']:
            priceInt = int(price.replace('$', ''))
            item['prices'] = priceInt
            if priceInt < flights['price']:
                flights['price'] = priceInt
                flights['url'] = item['url']

    print 'data', data
    print 'luck', flights
