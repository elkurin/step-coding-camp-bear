import os
import wp

try:
	os.remove("./data/index3.db")
except OSError:
	pass

collection = wp.WikipediaCollection("./data/wp.db")
index = wp.Index("./data/index3.db", collection)
index.generateFromOpeningText()

