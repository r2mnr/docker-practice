# Nginx + Python Flask の2コンテナ構成

## 概要

Docker Composeを使用して、NginxとPython Flaskを連携させたWebアプリケーション環境を構築しました。

Nginxをフロントエンド、Python Flaskをバックエンドとして分離し、Nginxが受け取ったAPIリクエストをFlaskへ転送する構成です。

ブラウザからボタンを押すとFlaskのAPIが呼び出され、バックエンドから返されたデータを画面に表示します。

### 動作環境
Ubuntu 26.04.1 

## システム構成

本プロジェクトでは、以下の2つのコンテナを使用しています。

| コンテナ | 役割 | 使用イメージ |
|---|---|---|
| Nginx | HTMLの配信・リバースプロキシ | nginx |
| Flask | APIの処理 | python:3.10-slim |

### 通信の流れ

1. ブラウザからNginxへアクセスする。
2. NginxがHTMLファイルを配信する。
3. ブラウザ上のボタン操作によってAPIリクエストが送信される。
4. Nginxが `/api/data` へのリクエストをFlaskへ転送する。
5. Flaskがリクエストを処理し、JSON形式のデータを返す。
6. ブラウザにレスポンスが表示される。

## 使用技術

- Docker
- Docker Compose
- Dockerfile
- Nginx
- Python
- Flask
- HTML
- JavaScript

## 各コンテナの役割

### 1. Nginx（フロントエンド）

NginxはWebサーバーとしてHTMLファイルを配信します。

また、Nginxの設定ファイルである `default.conf` を使用し、APIへのアクセスをFlaskへ転送するようにしています。

### 2. Python Flask（バックエンド）

FlaskではAPIを作成しています。

`/api/data` というエンドポイントを用意し、リクエストを受け取るとJSON形式のデータを返す仕組みです。

Flaskはコンテナ内の5000番ポートで待ち受けます。

## Dockerfileについて

本プロジェクトでは、Nginx用とFlask用にそれぞれDockerfileを作成しました。

Dockerfileを使用して、各コンテナに必要なファイルや実行環境を用意しています。

- Nginx側：HTMLファイルとNginxの設定ファイルを配置
- Flask側：Python環境にFlaskをインストールし、アプリケーションを配置

## Docker Composeについて

Docker Composeを使用して、NginxとFlaskの2つのサービスをまとめて管理しています。

それぞれのコンテナを個別に起動するのではなく、Composeファイルからまとめて起動できる構成にしました。

## 起動方法

リポジトリを取得し、対象ディレクトリへ移動します。

```bash
cd 01_two-containers
```

Docker Composeで起動します。

```bash
docker compose up --build
```

停止する場合は、以下を実行します。

```bash
docker compose down
```

※実際のComposeファイル名や配置に合わせて、必要に応じてコマンドを調整してください。

## 動作確認

ブラウザからNginxへアクセスし、HTMLページが表示されることを確認します。

ページ上のボタンを押すと、FlaskのAPIへリクエストが送信されます。

Flaskから返されたJSON形式のデータがブラウザに表示されることを確認しました。

## 構築中に発生した問題と対応

### 1. NginxからFlaskのサービスを名前解決できない

Nginxの起動時に、Flaskのサービス名を解決できないエラーが発生しました。

```text
nginx: [emerg] host not found in upstream "back-app"
```

Nginxから別のコンテナへ通信する場合、Docker Composeのネットワーク内でサービス名を利用できます。

そのため、Nginxの転送先とCompose側のサービス名が一致しているかを確認し、設定を修正しました。

### 2. Flaskのアプリケーションファイルが見つからない

Flask側では、以下のエラーが発生しました。

```text
python: can't open file '/app.py':
[Errno 2] No such file or directory
```

原因は、Dockerfileでアプリケーションファイルをコンテナ内へコピーする設定が不足していたことでした。

`COPY` の記述を追加し、アプリケーションファイルがコンテナ内に配置されるように修正しました。

## 学んだこと

今回の構築を通して、以下の内容を実践しました。

- Dockerfileを使ったイメージの作成
- Docker Composeによる複数コンテナの管理
- NginxによるHTMLファイルの配信
- Nginxのリバースプロキシ設定
- Flaskを使ったAPIの作成
- コンテナ間の通信
- Dockerのログやエラーメッセージを使った原因調査

特に、NginxとFlaskを別々のコンテナとして構成し、サービス名を利用して通信させる仕組みを実践できたことが大きな学びでした。

## 今後の課題

今回はNginxとFlaskの2コンテナ構成でしたが、今後はデータベースも追加し、バックエンドからデータベースへ接続する仕組みについても理解を深めていきたいと考えています。
