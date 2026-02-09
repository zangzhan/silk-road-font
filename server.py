from app import app

if __name__ == '__main__':
    print("正在启动武威汉简数字博物馆服务器...")
    print("访问地址: http://127.0.0.1:5000")
    # Set debug=False for a more stable "server" experience
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
