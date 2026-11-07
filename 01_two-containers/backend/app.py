from flask import Flask

app = Flask(__name__)


@app.route("/api/data")
def get_data():
    #  フロント（画面）からリクエストが来たら、この文字を返します！
    return {"message": "Hello from Python Backend!", "status": "Success"}


if __name__ == "__main__":
    # コンテナの裏側で、5000番のドアを開けて人間（フロント）を待ち受けます
    app.run(host="0.0.0.0", port=5000)
