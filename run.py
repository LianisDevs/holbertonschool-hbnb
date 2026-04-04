from pathlib import Path
from flask import redirect, send_from_directory
from part3.app import create_app

app = create_app()

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "part4"

@app.get("/part4/<path:filename>")
def frontend_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)

@app.get("/app")
def frontend_index():
    return redirect("/part4/html/index.html", code=302)

if __name__ == '__main__':
    app.run(debug=True)

def get_app():
    return app
