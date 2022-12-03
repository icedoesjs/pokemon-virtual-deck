from app import site
from flask import render_template
from app.models import Deck
import json
from flask_login import current_user

@site.route('/')
@site.route('/home')
def index():
    if current_user.is_authenticated:
            deck = Deck.query.get(current_user.id)
            if deck:
                return render_template('index.html', config=site.config, deck=json.dumps(deck.pokemon))
            else:
                return render_template('index.html', config=site.config, deck=None)
    else:
        return render_template('index.html', config=site.config, deck=None)

