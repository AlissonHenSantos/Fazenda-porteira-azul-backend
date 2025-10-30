import os

from . import create_app
app = create_app(os.getenv("CONFIG_MODE"))


@app.route('/')
def hello():
    return "Hello World!"

from .user import urls
from .cultura import urls


if __name__ == "__main__":
    app.run()