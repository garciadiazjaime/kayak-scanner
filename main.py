import sys
import time
import datetime
import sqlite3

from splinter import Browser
conn = sqlite3.connect('data.sqlite')
c = conn.cursor()
# url = "http://www.kayak.com/flights/CHI-PAR/2016-07-14/BRU-CHI/2016-07-26"

def wait_for(secs):
    print 'sleep for ', secs
    for i in range(secs):
        print i
        time.sleep(1)
    print 'awake'


def save_flight(data):
    query = ("INSERT INTO kayak_two_cities(start_a, end_a, end_b, price, url, date_a, date_b, date_query) VALUES ("
        "'" + data['start_a'] + "', "
        "'" + data['end_a'] + "', "
        "'" + data['end_b'] + "', "
        "'" + data['price'] + "', "
        "'" + data['url'] + "', "
        "'" + data['date_a'] + "', "
        "'" + data['date_b'] + "', "
        "'" + data['date_query'] + "')")
    c.execute(query)
    conn.commit()


def main():
    origin = 'CHI'
    airports = ['PAR', 'BRU', 'AMS', 'LON', 'BER']
    flights = {
        'price': 2000,
        'url': ''
    }
    date_start = []
    date_init = '2016-07-13'
    d1 = datetime.datetime.strptime(date_init, "%Y-%m-%d").date()
    delay_a = 1
    delay_b = 0
    cont_pages = 30
    cont_flights = 30
    span_days = 12
    for i in range(span_days):
        date_start.append(d1 + datetime.timedelta(days=i))

    data = []
    with Browser() as browser:

        for date_a in date_start:
            date_b = date_a + datetime.timedelta(days=11)

            for i in range(len(airports)-1):
                for j in range(len(airports)):
                    if i >= j:
                        continue
                    airp_a = airports[i]
                    airp_b = airports[j]
                    cont_pages += 1
                    url = 'http://www.kayak.com/flights/' + origin + '-' + airp_a + '/' + date_a.strftime('%Y-%m-%d') + '/' + airp_b + '-' + origin + '/' + date_b.strftime('%Y-%m-%d')
                    print cont_pages, url
                    browser.visit(url)
                    wait_for(delay_a)

                    if browser.is_element_present_by_css('.results_price', wait_time=10):
                        print '\t.results_price found'
                        for item in browser.find_by_css('.results_price'):
                            cont_flights += 1
                            try:
                                print '\tsaving price', item.text
                                price = str(item.text).replace('$', '')
                                save_flight({
                                    'start_a': origin,
                                    'end_a': airp_a,
                                    'end_b': airp_b,
                                    'price': price,
                                    'url': url,
                                    'date_a': date_a.strftime('%Y-%m-%d'),
                                    'date_b': date_b.strftime('%Y-%m-%d'),
                                    'date_query': str(datetime.datetime.now())
                                })
                            except:
                                print '\texcept'
                                pass
                        print '\tcont_flights', cont_flights
                    # break
                    wait_for(delay_b)
                # break
            # break
        print 'cont_pages', cont_pages, 'cont_flights', cont_flights
        conn.close()


if __name__ == "__main__":
    main()
