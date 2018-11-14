import sys
import os
import time
import datetime
import time
import sqlite3

from pync import Notifier
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
    query = ("INSERT INTO kayak_one_city(start, end, price, url, date_a, date_b, date_query) VALUES ("
        "'" + data['start'] + "', "
        "'" + data['end'] + "', "
        "'" + data['price'] + "', "
        "'" + data['url'] + "', "
        "'" + data['date_a'] + "', "
        "'" + data['date_b'] + "', "
        "'" + data['date_query'] + "')")
    c.execute(query)
    conn.commit()


def main():
    start_time = time.time()
    origin = 'CHI'
    airport = 'SAN'
    date_start = []
    date_end = ['2016-03-20', '2016-03-21']
    date_init = '2016-03-16'
    d1 = datetime.datetime.strptime(date_init, "%Y-%m-%d").date()
    delay_a = 30
    delay_b = 3
    cont_pages = 0
    cont_flights = 0
    span_days = 4
    max_inner_prices = 3

    # trip_span = 12
    # limit_date_to_get_bru = datetime.datetime.strptime('2016-07-19', '%Y-%m-%d').date()
    # date_departure_bru = datetime.datetime.strptime('2016-07-25', '%Y-%m-%d').date()
    # date_departure_bru_plus_one = datetime.datetime.strptime('2016-07-25', '%Y-%m-%d').date() + datetime.timedelta(days=1)
    for i in range(span_days):
        date_start.append(d1 + datetime.timedelta(days=i))
    data = []
    os.system('say "lets do this"')
    with Browser() as browser:
        for date_b in date_end:
            for date_a in date_start:
                print '================'
                print '====', date_a, date_b
                print '================'

                cont_pages += 1
                url = 'http://www.kayak.com/flights/' + origin + '-' + airport + '/' + date_a.strftime('%Y-%m-%d') + '/' + date_b
                print str(datetime.datetime.now()), cont_pages, url
                browser.visit(url)
                # wait until all flights are displayed, normally kayak takes less than 30secs
                wait_for(delay_a)

                if browser.is_element_present_by_css('.results_price', wait_time=10):
                    print '\t.results_price found'
                    cont_inner = 0
                    for item in browser.find_by_css('.results_price'):
                        cont_inner += 1
                        # save only the first 'max_inner_prices', since they are already sorted there's no reason to save expensier flights
                        if cont_inner > max_inner_prices:
                            break
                        cont_flights += 1
                        try:
                            print '\tsaving price', item.text
                            price = str(item.text).replace('$', '')
                            save_flight({
                                'start': origin,
                                'end': airport,
                                'price': price,
                                'url': url,
                                'date_a': date_a.strftime('%Y-%m-%d'),
                                'date_b': date_b,
                                'date_query': str(datetime.datetime.now())
                            })
                        except:
                            print '\texcept', sys.exc_info()[0]
                            pass
                    print '\tcont_flights', cont_flights
                else:
                    # this happens when kayak shows robot verification popup
                    print '\tprove kayak you are not a robot, and hit enter on the terminal'
                    os.system('say "prove kayak you are not a robot, and hit enter on the terminal"')
                    Notifier.notify('prove kayak you are not a robot, and hit enter on the terminal')
                    raw_input("Press Enter to continue...")
                # break
                # lets wait before trying next airport
                wait_for(delay_b)

        print str(datetime.datetime.now()), 'cont_pages', cont_pages, 'cont_flights', cont_flights
        conn.close()
        os.system('say "which you luck"')
        time_passed_in_secs = (time.time() - start_time)
        m, s = divmod(time_passed_in_secs, 60)
        h, m = divmod(m, 60)
        print "--- %d:%02d:%02d" % (h, m, s)


if __name__ == "__main__":
    main()
