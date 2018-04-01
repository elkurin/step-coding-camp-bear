import os
import wp

try:
	os.remove("./data/indexOpeningText.db")
except OSError:
	pass

collection = wp.WikipediaCollection("./data/wp.db")
# index = wp.Index("./data/index.db", collection)
# index.generate()
