from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

SOLR_URL = "http://localhost:8983/solr/jcgArticles/select"

def solr_search(query, filter_category=None, filter_published=None):
    base_query = f"title:*{query}* OR category:*{query}* OR author:*{query}*"
    filters = []

    if filter_category:
        filters.append(f"category:{filter_category}")
    if filter_published:
        filters.append(f"published:{filter_published}")

    params = {
        'q': base_query,
        'wt': 'json'
    }
    if filters:
        params['fq'] = filters

    response = requests.get(SOLR_URL, params=params)
    return response.json()["response"]["docs"]

@app.route("/")
def index():
    query = request.args.get("q", "")
    filter_category = request.args.get("category")
    filter_published = request.args.get("published")
    results = []

    if query:
        results = solr_search(query, filter_category, filter_published)

    return render_template("index.html", results=results, query=query)

@app.route("/autocomplete")
def autocomplete():
    term = request.args.get("term", "")
    docs = solr_search(term)
    titles = [doc.get("title", "") for doc in docs]
    return jsonify(titles)

if __name__ == "__main__":
    app.run(debug=True)
