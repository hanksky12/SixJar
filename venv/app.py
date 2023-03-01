from app import create_app

app = create_app()

if __name__ == '__main__':
    # app.run(port=8080)  # 配合google app engine
    app.run()  # 配合docker  '0.0.0.0'是內部設定
