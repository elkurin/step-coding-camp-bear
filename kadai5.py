import bottle
import wp
import json
import os

collection = wp.WikipediaCollection("./data/wp.db")
index = wp.Index("./data/indexWithTimes.db", collection)
indexOpeningText = wp.Index("./data/indexOpeningText.db", collection)
analyse = wp.AnalyseQuery()

@bottle.route('/action')
def action():
   query = bottle.request.query.q
   terms = analyse.extractWords(query)
   (vectors1, defaultVector1) = index.sortSearchReturnVectors(terms)
   (vectors2, defaultVector2) = indexOpeningText.sortSearchReturnVectors(terms)
   title = index.sortSearchFromTwoVectors(vectors1, vectors2, defaultVector1, defaultVector2)
   """
   table1 = index.sortSearchReturnTable(terms)
   table2 = indexOpeningText.sortSearchReturnTable(terms)
   title = index.returnBestFromTable(index.mergeTable(table1, table2))
   """
   bottle.response.content_type = 'application/json'
   if title is None:
       return json.dumps({
           'textToSpeech': 'はい残念みつからないよー'
           }, index=2, separators = (',', ':'),
           ensure_ascii = False)
   return json.dumps({
       'textToSpeech': title
   }, indent=2, separators=(',', ': '), ensure_ascii=False)


@bottle.route('/article/<title>')
def article(title):
    article = collection.get_document_by_id(title)
    bottle.response.content_type = 'application/json'
    if article is None:
        bottle.abort(404, "Not found")
    return json.dumps({
        'title': article.title,
        'text': "<<<Omitted>>>",
        'opening_text': article.opening_text,
        'auxiliary_text': article.auxiliary_text,
        'categories': article.categories,
        'headings': article.headings,
        'wiki_text': "<<<Omitted>>>",
        'popularity_score': article.popularity_score,
        'num_incoming_links': article.num_incoming_links,
    }, indent=2, separators=(',', ': '), ensure_ascii=False)

@bottle.route('/article/wiki_text/<title>')
def article_wiki_text(title):
    article = collection.get_document_by_id(title)
    if article is None:
        bottle.abort(404, "Not found")
    bottle.response.content_type = 'text/plain;charset=utf-8'
    return article.wiki_text

@bottle.route('/article/text/<title>')
def article_text(title):
    article = collection.get_document_by_id(title)
    if article is None:
        bottle.abort(404, "Not found")
    bottle.response.content_type = 'text/plain;charset=utf-8'
    return article.text()

port = 8081
if 'WPSEARCH_PORT' in os.environ:
    port = int(os.environ['WPSEARCH_PORT'])
bottle.run(host='0.0.0.0', port=port, reloader=False)
