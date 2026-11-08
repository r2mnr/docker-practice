# Nginx + Python Flask + MySQL の3コンテナ構成

## 概要

Docker Composeを使用して、Nginx・Python Flask・MySQLの3つを連携させた環境を構築しました。

1作品目ではNginxとFlaskの2コンテナ構成でしたが、今回はMySQLを追加し、バックエンドからデータベースへ接続する構成に発展させました。

ブラウザからAPIを呼び出すと、FlaskがMySQLと連携してデータを登録する仕組みです。

本プロジェクトでは、Dockerfileを使用せず、Docker Compose内で既存のイメージを指定して構築しています。

## 動作環境
Ubuntu 26.04.1 LTS

Docker 29.9.2

## 📁 フォルダ構成 (Directory Structure)

本プロジェクトのファイルおよびディレクトリの配置は以下の通りです。

```text
02_three-containers/            # プロジェクトのルートディレクトリ
├── docker-compose.yml          # Docker Compose設定ファイル
├── app.py                      # Flask（Python）のメインプログラム
├── default.conf                # Nginxの設定ファイル
└── index.html                  # フロントエンドの画面ファイル
```



## システム構成

| コンテナ | 役割 | 使用イメージ |
|---|---|---|
| Nginx | HTMLの配信・リバースプロキシ | nginx:latest |
| Flask | APIの処理・データベース接続 | python:3.10-slim |
| MySQL | データの保存・管理 | mysql:8.0 |

### 通信の流れ

1. ブラウザからNginxへアクセスする。
2. NginxがHTMLファイルを配信する。
3. ブラウザからAPIリクエストを送信する。
4. NginxがリクエストをFlaskへ転送する。
5. FlaskがMySQLへ接続する。
6. FlaskからMySQLへデータを登録する。
7. 処理結果がブラウザへ返される。

## 使用技術

- Docker
- Docker Compose
- Nginx
- Python
- Flask
- SQLAlchemy
- MySQL Connector
- MySQL 8.0
- HTML
- JavaScript

## 各コンテナの役割

### 1. Nginx（フロントエンド）

NginxはWebサーバーとしてHTMLファイルを配信します。

また、`default.conf` にリバースプロキシの設定を記述し、APIへのアクセスをFlaskへ転送します。

ホスト側の8000番ポートをコンテナ内の80番ポートに割り当てています。

### 2. Python Flask（バックエンド）

FlaskではAPIの処理を担当します。

Nginxから転送されたリクエストを受け取り、MySQLへ接続してデータを操作します。

今回の構成では、SQLAlchemyなどを利用してデータベースとの連携を行っています。

Flaskはコンテナ内の5000番ポートで待ち受けます。

### 3. MySQL（データベース）

MySQLはデータを保存するためのデータベースです。

今回の構成では、`study_db` というデータベースを用意しました。

FlaskからMySQLへ接続し、テーブルにデータを登録する仕組みを構築しています。

## Docker Composeについて

今回はDockerfileを作成せず、Composeファイル内で各サービスのイメージを直接指定しています。

使用しているイメージは以下のとおりです。

```yaml
front-web:
  image: nginx:latest

back-app:
  image: python:3.10-slim

db-store:
  image: mysql:8.0
```

また、`volumes` を利用してホスト側のファイルを各コンテナ内にマウントしています。

Flask側では、起動時に必要なPythonライブラリをインストールしてからアプリケーションを実行する構成にしました。

## 起動方法

リポジトリを取得し、対象ディレクトリへ移動します。

```bash
cd 02_three-containers
```

Docker Composeで起動します。

```bash
docker compose up
```

停止する場合は、以下を実行します。

```bash
docker compose down
```

※MySQLの初期化には時間がかかる場合があります。Flaskから接続できない場合は、MySQLの起動状態やログを確認してください。

## ポート設定

今回のComposeでは、以下のポートを使用しています。

| サービス | ホスト側 | コンテナ側 |
|---|---:|---:|
| Nginx | 8000 | 80 |
| Flask | 5000 | 5000 |
| MySQL | 3306 | 3306 |

ブラウザからは、Nginxのホスト側ポートを利用してアクセスします。

```text
http://localhost:8000/
```

## データベースへの接続と確認

FlaskからMySQLへ接続し、`study_db` データベース内のテーブルへデータを登録する処理を実装しました。

また、MySQLコンテナへ直接入って、登録されたデータを確認しました。

```bash
docker compose exec db-store bash
```

MySQLへログインした後、データベースを選択します。

```sql
USE study_db;
```

テーブルのデータを確認します。

```sql
SELECT * FROM user;
```

実際に確認した結果は以下のとおりです。

| id | name |
|---:|---|
| 1 | aikio |

この結果から、MySQL内にデータが登録されていることを確認できました。

## 構築中に発生した問題と対応

### 1. Pythonライブラリのインストールに関する問題

MySQLとの接続に必要なライブラリをインストールする際、パッケージ名の指定に誤りがあり、インストールに失敗しました。

指定しているパッケージ名を確認し、正しい名前に修正することで解決しました。

### 2. MySQLの起動準備が完了する前にFlaskが接続する問題

FlaskがMySQLへ接続しようとした際、MySQL側の準備が完了しておらず、接続エラーが発生しました。

Docker Composeの `depends_on` は基本的にサービスの起動順序を制御するものであり、MySQLが接続可能な状態になるまで待機するものではありません。

今回の学習では、Python側に `time.sleep(5)` を追加し、起動後に一定時間待つ方法で対応しました。

ただし、この方法は起動時間によっては失敗する可能性があるため、今後はヘルスチェックや接続リトライなどを利用した方法についても学習したいと考えています。

### 3. NginxからFlaskへの転送先の指定

Nginxの転送先を `localhost:5000` としていたため、Flaskへの通信がうまくいかない問題が発生しました。

Nginxコンテナ内の `localhost` はNginx自身を指します。

別のコンテナであるFlaskへ接続する場合は、Composeのネットワーク内でサービス名を指定する必要があります。

そのため、Flaskのサービス名である `back-app` を使う設定に修正しました。

## 学んだこと

今回の構築を通して、以下の内容を実践しました。

- Docker Composeによる3コンテナ構成
- 既存イメージを利用したコンテナの起動
- Composeでのボリュームマウント
- Nginxのリバースプロキシ設定
- FlaskによるAPIの作成
- FlaskからMySQLへの接続
- SQLAlchemyなどを利用したデータベース連携
- SQLを使ったデータの確認
- コンテナ間通信とサービス名による名前解決
- コンテナの起動順序とデータベースの準備状態

1作品目ではNginxとFlaskの連携が中心でしたが、今回はMySQLを追加したことで、バックエンドとデータベースの連携についても実践することができました。

## 今後の課題

今回の構成は学習用のものです。

今後は以下の内容について、さらに理解を深めていきたいと考えています。

- MySQLのデータ永続化
- Docker Composeのヘルスチェック
- データベース接続のリトライ処理
- 環境変数を利用した設定情報の管理
- Dockerネットワークの仕組み
- コンテナのログや状態の調査方法

今回の構築を通して、複数のコンテナを組み合わせてアプリケーション環境を作る基本的な流れを実践できました。
