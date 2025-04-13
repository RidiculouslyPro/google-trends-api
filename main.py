rom flask import Flask, jsonify
from pytrends.request import TrendReq
import os

app = Flask(__name__)
app.debug = True

@app.route('/trending')
def get_trending():
    try:
        pytrends = TrendReq(hl='en-US', tz=-300)  # EST timezone
        pytrends.build_payload(kw_list=["tech", "AI", "SaaS"], cat=47, timeframe='now 1-d', geo='US', gprop='news')
        related = pytrends.related_queries()

        results = []
        for keyword, queries in related.items():
            rising = queries.get('rising')
            if rising is not None and not rising.empty:
                for row in rising.to_dict('records'):
                    results.append({
                        "keyword": keyword,
                        "topic": row['query'],
                        "value": row['value']
                    })

        if not results:
            return jsonify({"message": "No trending topics found."}), 204

        unique = {item['topic']: item for item in results}.values()
        sorted_topics = sorted(unique, key=lambda x: x['value'], reverse=True)
        return jsonify([x['topic'] for x in sorted_topics[:5]])

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print(f"Running on port {port}...")
    app.run(host='0.0.0.0', port=port)
