# Nginx + Python Flask の2コンテナ構成

## 概要

Docker Composeを使用して、NginxとPython Flaskを連携させたWebアプリケーション環境を構築しました。

Nginxをフロントエンド、Python Flaskをバックエンドとして分離し、Nginxが受け取ったAPIリクエストをFlaskへ転送する構成です。

ブラウザからボタンを押すとFlaskのAPIが呼び出され、バックエンドから返されたデータを画面に表示します。

## 動作環境
Ubuntu 26.04.1 LTS

Docker 29.9.2


## 📁 フォルダ構成 (Directory Structure)

本プロジェクトのファイルおよびディレクトリの配置は以下の通りです。

```text
01_two-containers/            # プロジェクトのルートディレクトリ
├── docker-compose.yml          # Docker Compose設定ファイル
├── Dockerfile                  # Nginx用のDockerfile
├── default.conf                # Nginxの設定ファイル
├── index.html                  # フロントエンドの画面ファイル
└── backend-app                 # バックエンド用ディレクトリ
    ├── Dockerfile              # Flask用のDockerfile
    └── app.py                  # Flask（Python）のメインプログラム
```

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

ブラウザからは、Nginxのホスト側ポートを利用してアクセスします。

```text
http://localhost:/
```

# 構築中に発生した問題と対応

### 1. NginxからFlaskのサービスを名前解決できない（起動順序のエラー）

Nginxの起動時に、Flaskのサービス名を解決できないエラーが発生しました。

```text
nginx: [emerg] host not found in upstream "back-app"
```

**原因と対応:**
Nginxがわずか0.1秒で爆速オープンした際、隣のFlask（Python）厨房が起動準備中（1〜2秒かかる）だったため、Nginxがサービス名を見つけられずにパニックを起こしたことが原因です。
`docker-compose.yml` に `depends_on: - back-app` の記述を追加し、先にFlaskが起動してからNginxが立ち上がるように制御して修正しました。

### 2. Flaskのアプリケーションファイルが見つからない

Flask側では、以下のエラーが発生しました。

```text
python: can't open file '/app.py':
[Errno 2] No such file or directory
```

**原因と対応:**
Dockerfileでアプリケーションファイルをコンテナ内へコピーする設定が不足していたことが原因でした。
レシピ（Dockerfile）内に `COPY app.py /app.py` の記述を追加し、アプリケーションファイルがコンテナ内に正しく配置されるように修正しました。

### 3. コンテナ起動時にシェル（sh）が見つからない（ボリューム同期エラー）

過去に作成したコンテナを再起動しようとした際、以下のエラーが発生しました。

```text
sh: command not found
```

**原因と対応:**
Docker Composeのボリューム機能（`-v`）で、手元の「中身が空っぽのフォルダ」を、コンテナ側のLinuxシステムにとって最重要である `/bin` フォルダにマウント（同期）してしまい、コンテナ内のシステムファイルが空っぽに上書きされて消滅したことが原因です。
マウント先をシステム必須のフォルダから、影響のない安全な空フォルダ（`/mnt` など）へ変更して修正しました。


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
