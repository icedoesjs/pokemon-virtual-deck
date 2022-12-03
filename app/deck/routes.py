from flask import render_template, request, Blueprint, url_for, redirect, flash
from flask_login import current_user, login_required
from app.models import Deck, Users
from .forms import AddToDeck
from requests import get
import json

deck = Blueprint('deck', __name__, template_folder='deck_templates')

def getpmInfo(name):
    url = f'https://pokeapi.co/api/v2/pokemon/{name}'
    res = get(url)
    if res.ok:
        data = res.json()
        return data 
    else:
        return False
    
poke_info = {}
def addtoInfo(name, ability, base_exp, sprite_url, attack_base, hp_base, def_base):
    poke_info["name"] = name.title()
    poke_info["ability"] = ability
    poke_info["base_exp"] = base_exp
    poke_info["front_shiny"] = sprite_url
    poke_info["attack_base"] = attack_base
    poke_info["hp_base"] = hp_base
    poke_info["defense_base"] = def_base

@deck.route('/deck/view', methods=['GET', 'POST'])
@login_required
def view_deck():
    user = Users.query.get(current_user.id)
    deck = Deck.query.get(current_user.id)
    pokemon = json.loads(deck.pokemon)
    if deck:
        return render_template('view_deck.html', deck=pokemon, user=user)
    else:
        return redirect(url_for('deck.create_deck'))
    
    
    
@deck.route('/deck/remove/<name>')
@login_required
def remove_from_deck(name):
    deck = Deck.query.get(current_user.id)
    # Pass dict of deck
    poke_deck = json.loads(deck.pokemon)
    if deck:
        del poke_deck[name]
        deck.pokemon = json.dumps(poke_deck)
        deck.update_db()
        return redirect(url_for('deck.view_deck'))
    else:
        return redirect(url_for('deck.create_deck'))
    
@deck.route('/deck/add', methods=['GET', 'POST'])
@login_required
def add_to_deck():
    user = current_user.id
    deck = Deck.query.get(user)
    if deck:
        form = AddToDeck()
        if request.method == 'POST':
            if form.validate():
                first_poke = form.name.data.lower() 
                valid_poke = getpmInfo(first_poke)
                # Convert STR to dict
                current_deck = json.loads(deck.pokemon)
                if valid_poke:
                    if (len(current_deck.keys()) >= 10): return flash('You can only have 10 pokemon in your deck', 'danger')
                    if not first_poke in current_deck.keys(): 
                        current_deck[first_poke] = {}
                        current_deck[first_poke]["ability"] = valid_poke["abilities"][1]["ability"]["name"]
                        current_deck[first_poke]["base_xp"] = valid_poke["base_experience"]
                        current_deck[first_poke]["sprite_url"] = valid_poke["sprites"]["front_shiny"]
                        current_deck[first_poke]["stat"] = valid_poke["stats"][1]["base_stat"]
                        current_deck[first_poke]["hp_base"] = valid_poke["stats"][0]["base_stat"]
                        current_deck[first_poke]["def_base"] = valid_poke["stats"][2]["base_stat"]
                        # Convert dict back to string 
                        deck.pokemon = json.dumps(current_deck)
                        deck.update_db()
                    else:
                        flash('That pokemon is already in your deck', 'danger')
                    return redirect(url_for('deck.view_deck'))
        return render_template('add_to_deck.html', form=form)
    else:
        return redirect(url_for('deck.create_deck'))
    
@deck.route('/deck/create', methods=['GET', 'POST'])
@login_required
def create_deck():
    user = current_user.id
    deck = Deck.query.get(user)
    if deck:
        return redirect(url_for('deck.view_deck'))
    else:
        form = AddToDeck()
        if request.method == 'POST':
            if form.validate():
                first_poke = form.name.data 
                valid_poke = getpmInfo(first_poke.lower())
                deck_data = {}
                if valid_poke:
                    deck_data[first_poke] = {}
                    deck_data[first_poke]["ability"] = valid_poke["abilities"][1]["ability"]["name"]
                    deck_data[first_poke]["base_xp"] = valid_poke["base_experience"]
                    deck_data[first_poke]["sprite_url"] = valid_poke["sprites"]["front_shiny"]
                    deck_data[first_poke]["stat"] = valid_poke["stats"][1]["base_stat"]
                    deck_data[first_poke]["hp_base"] = valid_poke["stats"][0]["base_stat"]
                    deck_data[first_poke]["def_base"] = valid_poke["stats"][2]["base_stat"]
                    d = Deck(current_user.id, json.dumps(deck_data)) 
                    d.save_to_db()
                    return redirect(url_for('deck.view_deck'))
                else:
                    flash('That pokemon was not found', 'danger')     
        return render_template('add_to_deck.html', form=form)
                

