from flask import render_template, request, Blueprint, url_for, redirect, flash 
from flask_login import current_user, login_required
from app.models import Deck, Users 
from .forms import SearchUser
import json

battle = Blueprint('battle', __name__, template_folder='battle_templates')

@battle.route('/battle/', methods=['GET', 'POST'])
@login_required
def search_user():
    user = Users.query.get(current_user.id)
    deck = Deck.query.get(current_user.id)
    if deck:
        form = SearchUser()
        if request.method == 'POST':
            if form.validate():
                user_name = form.name.data.lower()
                opponent = Users.query.filter_by(username=user_name).first()
                if not opponent: 
                    flash('A user with that username was not found', 'danger')
                    return render_template('search_user.html', form=form)
                if opponent.id == current_user.id: 
                    flash('You cannot battle yourself', 'danger')
                    return render_template('search_user.html', form=form)
                op_deck = Deck.query.get(opponent.id)
                if not op_deck: 
                    flash('The user provided has not created a deck', 'danger')
                    return render_template('search_user.html', form=form)
                return render_template('pre_battle.html', user=json.loads(deck.pokemon), opponent=json.loads(op_deck.pokemon), op_id=opponent.id, user_id=user.id)
        return render_template('search_user.html', form=form)        
    else:
        flash('You must first create a deck', 'danger')
        return redirect(url_for('deck.create_deck'))
                
@battle.route('/battle/start/<int:opponent_id>', methods=['GET', 'POST'])
@login_required
def battle_user(opponent_id):
    u_deck = Deck.query.get(current_user.id)
    v_deck = Deck.query.get(opponent_id)
    
    me = Users.query.get(current_user.id)
    opponent = Users.query.get(opponent_id)
    opponent_name = opponent.username
    
    # Define all stats, set to 0
    total_opponent_attack = 0
    total_opponent_defense = 0
    total_opponent_health = 0
    total_self_attack = 0
    total_self_defense = 0
    total_self_health = 0
    
    # Get all stats of opponent pokemons
    for k, v in json.loads(v_deck.pokemon).items():
        total_opponent_attack += v['attack']
        total_opponent_defense += v['def_base']
        total_opponent_health += v['hp_base']
        
    # Get all stats of user pokemons
    for k,v in json.loads(u_deck.pokemon).items():
        total_self_attack += v['attack']
        total_self_defense += v['def_base']
        total_self_health += v['hp_base']
        
    # Get total health (defense + health)
    self_health = total_self_health + total_self_defense
    opponent_health = total_self_health + total_opponent_defense
    
    # Get attack on health
    self_left_with = self_health - total_opponent_attack
    op_left_with = opponent_health - total_self_attack
    
    # Note
    # If this was a deployed app and I had time
    # I would implement you cannot battle the same deck again
    # As well as you cannot battle the same user within 24 hrs 
    # To avoid farming wins and loses
    if self_left_with > op_left_with:
        # you win 
        me.wins += 1
        opponent.lose += 1
        me.update_db()
        opponent.update_db()
        return render_template('you_win.html', left_with=total_opponent_attack, name=opponent_name)
    elif self_left_with == op_left_with:
        # Match Tie
        return render_template('tie.html', name=opponent_name)
    elif self_left_with < op_left_with:  
        # You lose
        me.lose += 1 
        me.update_db()
        opponent.wins += 1 
        opponent.update_db()
        return render_template('you_lost.html', total_damage=total_opponent_attack, name=opponent_name)
    else:
        return redirect(url_for('home'))
    