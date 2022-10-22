import yaml
from logging.config import dictConfig
from typing import Dict, List
from flask import Flask, request
import sys

from reaction_types import reaction_builder_factory, Reaction
from tot_message import TotMessage

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})
app = Flask(__name__)


def filter_requests(character_name: str, npcs: Dict) -> bool:
    upper_case_names = map(lambda x: x.upper(), npcs.keys())

    return character_name.upper in upper_case_names


@app.route("/conan", methods=['GET'])
def handle_message():
    args = request.args
    app.logger.info("#############################")
    tot_message = TotMessage(args)
    app.logger.info(args.get("message"))
    app.logger.info(tot_message)
    app.logger.info("#############################")

    for reaction in reactions:
        reaction.handle_message(tot_message=tot_message)

    return "<p>Hello, World!</p>"


if __name__ == "__main__":
    reactions: List[Reaction] = []
    with open("config.yaml", "r") as stream:
        try:
            config_dict = yaml.safe_load(stream)
            for reaction in config_dict:
                reactions.append(reaction_builder_factory(reaction))
        except yaml.YAMLError as exc:
            sys.exit(1)

    #app.run("0.0.0.0", port=5000)


