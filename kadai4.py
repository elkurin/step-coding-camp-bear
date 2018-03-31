import bottle
import wp
import json
import os

collection = wp.WikipediaCollection("./data/wp.db")
index = wp.Index("./data/index2.db", collection)
analyse = wp.AnalyseQuery()

gameEnd = False
wordsState = []

@bottle.route('/action')
def action():
    global wordsState, gameEnd
    query = bottle.request.query.q
    bottle.response.content_type = 'application/json'
    if gameEnd:
        if query == 'はい':
            gameEnd = False
            return json.dumps({
                'textToSpeech': 'ゲームを始めるよ'
            }, indent=2, separators=(',', ': '), ensure_ascii=False)
        else:
            return json.dumps({
                'textToSpeech': '聞こえないよ？'
            }, indent=2, separators=(',', ': '), ensure_ascii=False)


    terms = analyse.extractWords(query)
    wordsState += terms
    titles = index.search(wordsState)
    if len(titles) == 0:
        wordsState = []
        gameEnd = True
        return json.dumps({
            'textToSpeech': '記事が見つかりませんでした。あなたの負けー。もう一度遊びますか'
        }, indent=2, separators=(',', ': '), ensure_ascii=False)
    return json.dumps({
        'textToSpeech': '記事が{}件見つかりました。今言われた単語は{}です'.format(len(titles), 'と'.join(wordsState))
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
