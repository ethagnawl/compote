# /// script
# dependencies = [
#   "flask==3.1.2",
# ]
# ///

from compote import Compote
from flask import Flask, current_app


class Config(Compote):
    GREETING = Compote.fetch_from_env_or_default(
        "GREETING", "Hiya!", transform_value=lambda x: f"{x.upper()}!!"
    )


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    @app.route("/")
    def root():
        return current_app.config["GREETING"]

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
