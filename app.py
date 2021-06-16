from flask import Flask
from flask import request, Response
import json

from dev_form_bot import DevFormBot
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.data:
        data = json.loads(request.data.decode("utf-8"))
        task = data["task"]
        bot = None
        if data["bot_settings"]:
            bot_settings = json.loads(data["bot_settings"])
            bot = DevFormBot(task, bot_settings)
        else:
            bot = DevFormBot(task)

        response = bot.check_task()
        if response:
            return response

    return Response(status=200)


if __name__ == "__main__":
    app.run()
