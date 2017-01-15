# Berkeley Pizza Parser

This tool fetches the current pizza schedule for Cheeseboard and Sliver, parses it, and displays today's pizza as well as the entire schedule. 

Disclaimer: This is not meant for serious usage. It has minimal error handling. It was written in haste.

Sample usage:
```
$ python berkeley_pizza_parser.py pizza.json 
$ python berkeley_pizza_printer.py pizza.json 
--Today's Pizza--
Cheeseboard:   Cremini mushroom, onion, mozzarella and Capricho de Cabra fresh goat cheese, garlic olive oil, parsley, oregano
Sliver:        Fresh asparagus, crimini mushrooms, mozzarella, campo de Montalban cheese, gremolata & garlic olive oil

*********

--Wednesday, January 11--
Cheeseboard:   Bartlett pear, caramelized onion, mozzarella and Dunbarton blue cheese,toasted Walnut, garlic olive oil, parsley
Sliver:        Fresh corn, chile pasilla, yellow onions, mozzarella, French feta & garlic olive oil.

--Thursday, January 12--
Cheeseboard:   Artichoke heart, baby spinach, mozzarella and local Belfiore ricotta cheese, chive, lemon zest, parsley
Sliver:        Roma tomatoes, red onions, mozzarella, aged asiago cheese, fresh herbs & garlic olive oil.

--Friday, January 13--
Cheeseboard:   Crushed tomato, red onion, mozzarella and BelGioioso aged Asiago cheese, garlic olive oil, parsley, oregano
Sliver:        Roasted crimini mushrooms, yellow onions, mozzarella, fresh goat cheese, fresh herbs, chanterelle mushroom infused garlic olive oil.

--Saturday, January 14--
Cheeseboard:   Roasted potato, caramelized onion, mozzarella and Gruyere cheese, garlic olive oil, parsley, oregano
Sliver:        Roasted Yukon potatoes, onions, chile pasilla, mozzarella, Bulgarian feta cheese, limes, cilantro & garlic olive oil.

--Sunday, January 15--
Cheeseboard:   None
Sliver:        Juicy pineapple, red bell peppers, mozzarella, French feta cheese & garlic olive oil. Topped with fresh arugula tossed in lemon vinaigrette.
```

Works great as a cron:

```
python berkeley_pizza_printer.py pizza.json |  mail -s "[pizza] $(date --date=today +%Y-%m-%d) Pizza Report" -r 'pearce@cs.berkeley.edu' 'pearce@cs.berkeley.edu'
