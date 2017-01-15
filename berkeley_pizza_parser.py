from BeautifulSoup import BeautifulSoup as bs
import BeautifulSoup
import urllib2
import dateutil.parser
import json
from datetime import date

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
            p = day.find("div", {"class": "menu"}).text.split(":")[1].strip()
            if p.endswith("Salad"):
                p = p[:-len("Salad")]
            ret[d] = p
        return ret

class Sliver(Pizza):
    def __init__(self):
        self.url = "http://sliverpizzeria.com/pizza/"
    
    def parse(self):
        soup = bs(self.page)
        days = soup.findAll("div", {"class": "caption"})
        ret = {}
        for day in days:
            if "PIZZA OF THE DAY" in day.text:
                continue
            d = dateutil.parser.parse(day.contents[0].text).date()
            p = day.contents[1].strip()
            ret[d] = p
        return ret

def mergePizza(cheeseboard, sliver):
    keys = sliver.keys() + cheeseboard.keys()
    keys = set(keys)
    ret = {}
    for key in keys:
        ret[key] = {}
        val = None
        if key in sliver:
            val = sliver[key]
        ret[key]["Sliver"] = val

        val = None
        if key in cheeseboard:
            val = cheeseboard[key]
        ret[key]["Cheeseboard"] = val
    return ret

def printPizza(pizza):
    def f(d):
        s = []
        for k in sorted(d.keys()):
            v = d[k]
            k = "%s:" % k
            k = k.ljust(15, " ")
            s.append("%s%s" % (k, v))
        return "\n".join(s)
    today = date.today()
    print "--Today's Pizza--"
    if today in pizza:
        print f(pizza[today])
    else:
        print "None. :("
   
    print
    print "*********"
    
    for day in sorted(pizza.keys()):
        if day <= today:
            continue
        print
        print "--%s--" % day.strftime("%A, %B %d")
        print f(pizza[day])


if __name__ == "__main__":
    cheese = CheeseBoard().getMePizza()
    sliver = Sliver().getMePizza()
    pizza = mergePizza(cheese, sliver)
    printPizza(pizza)
