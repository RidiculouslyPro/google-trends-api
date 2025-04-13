from flask import Flask, jsonify
from pytrends.request import TrendReq
import os

app = Flask(__name__)

@app.route('/trending')
def get_trending():
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(kw_list=["tech", "AI", "SaaS"], cat=47, timeframe='now 1-d', geo='US', gprop='')
    related = pytrends.related_queries()

    results = []
    for keyword, queries in related.items():
        if queries['rising'] is not None:
            for row in queries['rising'].to_dict('records'):
                results.append({
                    "keyword": keyword,
                    "topic": row['query'],
                    "value": row['value']
                })

    unique = {item['topic']: item for item in results}.values()
    sorted_topics = sorted(unique, key=lambda x: x['value'], reverse=True)
    return jsonify([x['topic'] for x in sorted_topics[:5]])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print(f"Running on port {port}...")
    app.run(host='0.0.0.0', port=port)
