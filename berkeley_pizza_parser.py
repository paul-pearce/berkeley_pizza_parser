from BeautifulSoup import BeautifulSoup as bs
import BeautifulSoup
import urllib2
import dateutil.parser
import json
from datetime import date
from datetime import datetime
import sys

class Pizza:
    url = None
    page = None

    def fetch(self):
        try:
            self.page = urllib2.urlopen(self.url)
        except:
            pass
    
    def parse(self):
        assert False
    
    def getMePizza(self):
        self.fetch()
        return self.parse()

class CheeseBoard(Pizza):
    def __init__(self):
        self.url = "http://cheeseboardcollective.coop/pizza/"
    
    def parse(self):
        soup = bs(self.page)
        days = soup.find("div", {"class": "pizza-list"})
        ret = {}
        for day in days:
            if isinstance(day, BeautifulSoup.NavigableString):
                    continue
            d = dateutil.parser.parse(day.find("div", {"class": "date"}).text).date()
            if not day.find("div", {"class": "menu"}).text:
                continue
            p = day.find("div", {"class": "menu"}).text.split(":")[1].strip()
            if p.endswith("Salad"):
                p = p[:-len("Salad")]
            if p.lower().startswith("new pizza") and p[len("new pizza")] != " ":
                p = p[0:len("new pizza")] + " " + p[len("new pizza"):]
            ret[d] = p
        return ret

class Sliver(Pizza):
    def __init__(self, location):
        self.url = "https://www.sliverpizzeria.com/menu-weekly"
        self.location = location.lower()

    def parse(self):
        soup = bs(self.page)
        locations = soup.findAll("div", {"class": "summary-item-list-container sqs-gallery-container"})
        location = None
        for this_location in locations:
            location_text = this_location.findAll("span", {"class": "summary-collection-title"})[0].text
            if self.location not in location_text.lower(): 
                continue
            location = this_location

        months = location.findAll("span", {"class": "summary-thumbnail-event-date-month"})
        months = [x.text for x in months]

        days = location.findAll("span", {"class": "summary-thumbnail-event-date-day"})
        days = [x.text for x in days]
        
        dates = zip(months, days)
        dates = [ "%s %s" % x for x in dates]
        dates = [ dateutil.parser.parse(x).date() for x in dates]

        pizzas = location.findAll("div", {"class": "summary-excerpt"})
        pizzas = [ x.text for x in pizzas]

        pairs = zip(dates, pizzas)

        ret = {}
        for date, pizza in pairs:
            ret[date] = pizza
        return ret

def mergePizza(l):

    labels = map(lambda s: s[0], l)
    pizzas = map(lambda s: s[1], l)

    keys = []
    for item in pizzas:
        keys += item.keys()

    keys = set(keys)
    ret = {}
    for key in keys:
        ret[key] = {}
        
        for i in xrange(0, len(pizzas)):
            val = None
            if key in pizzas[i]:
                val = pizzas[i][key]
            ret[key][labels[i]] = val

    return ret

def tagPizza(pizza):
    d = {
            "data": pizza,
            "meta": {
                        "source": "https://github.com/Paul-pearce/berkeley_pizza_parser",
                        "author": "Paul Pearce <pearce@cs.berkeley.edu>",
                        "timestamp": datetime.utcnow().isoformat(),
                    },
        }
    return d

def jsonPizza(pizza):
    for key in pizza["data"].keys():
        pizza["data"][key.isoformat()] = pizza["data"][key]
        del pizza["data"][key]

    return json.dumps(pizza, sort_keys=True, indent=4, separators=(',', ': '))

def writePizza(pizza, filename):
    # I want the trailing \n that json.dump() does not give.
    f = open(filename, "w")
    f.write(pizza)
    f.write("\n")
    f.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: python berkeley_pizza_parser.py output.json"
        exit(-1)

    cheese = CheeseBoard().getMePizza()
    sliver_shattuck = Sliver("shattuck").getMePizza()
    sliver_telegraph = Sliver("telegraph").getMePizza()
    sliver_oakland = Sliver("broadway").getMePizza()
    pizza = mergePizza([["Cheeseboard", cheese], ["Sliver Shattuck", sliver_shattuck], ["Sliver Telegraph", sliver_telegraph], ["Sliver Broadway", sliver_oakland]])
    taggedPizza = tagPizza(pizza)
    jsonPizza = jsonPizza(taggedPizza)
    writePizza(jsonPizza, sys.argv[1])
