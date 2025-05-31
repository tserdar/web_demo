"""Entry point for the web application."""

from app import my_web_app

app = my_web_app()

if __name__ == "__main__":
    app.run(debug=True)
