import time
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 1. 接続テスト用：MySQL倉庫（db-store:3306）への秘密のルートをFlaskに教えてあげる
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:aikio_password@db-store:3306/study_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 2. 倉庫の中に「お名前（name）」を保存するためのノート（テーブル）を定義する
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

#  呼び鈴（URL）
@app.route('/api/data')
def send_message():
    try:
        # 3. 呼び鈴が鳴るたびに、倉庫のノートに「aikio」という名前を1行書き込む！
        new_user = User(name="aikio")
        db.session.add(new_user)
        db.session.commit() # 確定（保存）！

        # 4. 倉庫に無事保存できたら、お皿に載せてブラウザにメッセージを返す
        return {"message": "MySQL倉庫へのデータ保存、大成功！！！"}
    except Exception as e:
        # もし倉庫がまだ開いていなくて失敗したらエラーを返す
        return {"message": f"倉庫への保存失敗... 原因: {str(e)}"}, 500

if __name__ == '__main__':

    #  起動したあと、MySQLが完全に起きるまで5秒だけ待ってあげる！
    print("MySQL倉庫の開店を待っています...")
    time.sleep(5)

    # 5. コンテナ起動時に自動で倉庫の中にノート（テーブル）を作成させる
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
