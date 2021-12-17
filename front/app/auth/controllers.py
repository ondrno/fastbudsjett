import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_babel import refresh
from ..utils import rest
from .forms import LoginForm


mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


@mod_auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form['email']
        password = request.form['password']

        error = None
        try:
            auth_token = rest.iface.login(email, password)
        except rest.ApiLoginError as e:
            error = f'{e}'
        except rest.ApiException as e:
            error = f'Unknown user or password, error={e}'
        except rest.ApiConnectionError as e:
            error = f'Could not establish connection, error={e}'

        if error is None:
            session.clear()
            session['auth_token'] = auth_token
            return redirect(url_for('items.index'))

        flash(error)

    return render_template('auth/login.html', form=form)


@mod_auth.before_app_request
def load_logged_in_user():
    auth_token = session.get('auth_token')

    if auth_token is None:
        g.user = None
        g.is_superuser = None
    else:
        try:
            user = rest.iface.whoami()
            session['locale'] = user._default_locale
            refresh()
            g.user = user.get_id()
            g.is_superuser = user.is_superuser
        except rest.ApiException:
            session.clear()
            return redirect(url_for('auth.login'))


@mod_auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
