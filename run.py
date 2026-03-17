from part3.app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

def get_app():
    return app
