from flask import (
    Blueprint, render_template, redirect, session, url_for, request
)
from flask_babel import refresh
from ..auth.controllers import login_required
from ..utils import rest
from .forms import UsersForm


mod_users = Blueprint('users', __name__, url_prefix="/users")


def prepare_data(r: request):
    data = {'email': r.form['email'],
            'default_locale': r.form['default_locale'],
            }
    return data


@mod_users.route('/', methods=['GET'])
@login_required
def index():
    current_user = rest.iface.whoami()
    me = {'id': current_user._user_id, 'email': current_user._email, 'locale': current_user._locale}
    users = [me]
    return render_template('users/index.html', known_users=users)


@mod_users.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit(user_id: int):
    me = rest.iface.whoami()
    form = UsersForm(default_locale=me._locale, email=me._email)
    if form.validate_on_submit():

        data = prepare_data(request)
        rest.iface.update_user(user_id, data)

        # show the same month as the date of the item which was created/modified
        session["locale"] = data['default_locale']
        refresh()
        return redirect(url_for('users.index'))

    return render_template('users/edit.html', form=form, known_users=[me])
