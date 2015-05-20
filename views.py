"""All the views for the site are included here"""
from flask import Blueprint, url_for, request, render_template, redirect, flash
from flask.ext.login import LoginManager, login_user, logout_user, \
    current_user
from sqlalchemy import func
from models import db, User, Animal
from oauth import OAuthSignIn

blueprint = Blueprint('views', __name__)


@blueprint.route('/')
def index():
    if current_user.is_anonymous():
        return render_template('index.html')
    return render_template('search_home.html')


@blueprint.route('/search')
def search():
    if current_user.is_anonymous():
        return redirect(url_for('views.index'))
    keywords = request.args.get('query')
    if not keywords:
        return render_template('search.html', animals={}, keywords=keywords)
    query = keywords.split(' ')
    animals = Animal.query.filter(Animal.name.ilike("%" + func.lower(query.pop()) + "%"))
    while query:
        animals = animals.union(Animal.query.filter(Animal.name.ilike("%" + func.lower(query.pop()) + "%")))
    print(query)
    return render_template('search.html', animals=animals, keywords=keywords)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.index'))


@blueprint.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('views.index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@blueprint.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('views.index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('views.index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, username=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('views.index'))


