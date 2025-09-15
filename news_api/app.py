from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# 🔑 World News API Key
API_KEY = "1691c85d309544ca906fb5426ad5ba24"
BASE_URL = "https://api.worldnewsapi.com/search-news"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/news")
def get_news():
    query = request.args.get("query", "india")

    params = {
        "source-country": "in",
        "language": "en",
        "number": 10,
        "text": query
    }

    headers = {"x-api-key": API_KEY}
    response = requests.get(BASE_URL, params=params, headers=headers)
    data = response.json()

    articles = []
    if "news" in data:
        for i, item in enumerate(data["news"]):
            articles.append({
                "id": i,
                "title": item.get("title"),
                "description": (item.get("text")[:150] + "...") if item.get("text") else "No description available",
                "full_text": item.get("text"),
                "image": item.get("image")
            })

    return jsonify({"articles": articles})

@app.route("/article")
def article():
    title = request.args.get("title", "No Title")
    content = request.args.get("content", "No Content")
    image = request.args.get("image", "")

    return render_template("article.html", title=title, content=content, image=image)

if __name__ == "__main__":
    app.run(debug=True)
