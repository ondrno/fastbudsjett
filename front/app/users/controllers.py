from flask import (
    Blueprint, render_template, redirect, session, url_for, request
)
from flask_babel import refresh
from ..auth.controllers import login_required
from ..utils import rest, is_get_request
from .forms import UsersForm


mod_users = Blueprint('users', __name__, url_prefix="/users")


def prepare_data(r: request):
    data = {'email': r.form['email'],
            'default_locale': r.form['default_locale'],
            'is_active': r.form['is_active'],
            'is_superuser': r.form['is_superuser'],
            }
    return data


@mod_users.route('/', methods=['GET'])
@login_required
def index():
    users = rest.iface.get_users()
    current_user = rest.iface.whoami()
    me = {'id': current_user._user_id, 'email': current_user._email, 'locale': current_user._locale}
    print(f"users->index(): users={users}")
    print(f"users->index(): me={me}")
    return render_template('users/index.html', users=users, current_user=me)


@mod_users.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit(user_id: int):
    me = rest.iface.whoami()

    if is_get_request(request):
        form = UsersForm(default_locale=me._locale, email=me._email)

    if form.validate_on_submit():
        data = prepare_data(request)
        if me.id == user_id:
            data.remove('email')
            data.remove('is_superuser')
            data.remove('is_active')

        rest.iface.update_user(user_id, data)

        session["locale"] = data['default_locale']
        refresh()
        return redirect(url_for('users.index'))

    return render_template('users/edit.html', form=form, known_users=[me])


@mod_users.route('/remove/<int:user_id>', methods=['GET', 'POST'])
@login_required
def remove(user_id: int):
    me = rest.iface.whoami()
    if me.get_id() == user_id:
        return render_template('500.html')
