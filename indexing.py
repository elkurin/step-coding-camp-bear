import os
import wp

try:
	os.remove("./data/index.db")
except OSError:
	pass

collection = wp.WikipediaCollection("./data/wp.db")
index = wp.Index("./data/index.db", collection)
index.generate()

