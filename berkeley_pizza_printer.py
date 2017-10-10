import dateutil.parser
import json
from datetime import date
import sys

def printPizza(pizza):
    def parseDates(d):
        for key in d.keys():
            d[dateutil.parser.parse(key).date()] = d[key]
            del d[key] 
    def printWorker(d):
        s = []
        for k in sorted(d.keys()):
            v = d[k]
            k = "%s:" % k
            k = k.ljust(15, " ")
            s.append("%s%s" % (k, v))
        return "\n".join(s)

    parseDates(pizza)
    today = date.today()
    print "--Today's Pizza (%s)--" % today.strftime("%A, %B %d")
    if today in pizza:
        print printWorker(pizza[today])
    else:
        print "None. :("
   
    print
    print "*********"
    
    for day in sorted(pizza.keys()):
        if day <= today:
            continue
        print
        print "--%s--" % day.strftime("%A, %B %d")
        print printWorker(pizza[day])

def fixUTF8():
    import codecs
    if sys.stdout.encoding == None :
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    if sys.stderr.encoding == None :
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: python berkeley_pizza_printer.py pizza.json"
        exit(-1)
    
    fixUTF8()
    jsonPizza = json.load(open(sys.argv[1]))
    printPizza(jsonPizza["data"])
