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
            'is_active': r.form.get('is_active', True),
            'is_superuser': r.form.get('is_superuser', False),
            }
    return data


@mod_users.route('/', methods=['GET'])
@login_required
def index():
    me = rest.iface.whoami()
    if me.is_superuser:
        users = rest.iface.get_users()
    else:
        users = me

    print(f"users->index(): users={users}")
    print(f"users->index(): me={me}")
    return render_template('users/index.html', users=users, current_user=me)


@mod_users.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit(user_id: int):
    me = rest.iface.whoami()
    user = rest.iface.get_user(user_id)

    form = UsersForm(default_locale=user._locale, email=user.email,
                     is_active=user.is_active, is_superuser=user.is_superuser)

    if me._user_id == user_id:
        form.is_active.render_kw = {'disabled': 'disabled'}
        form.is_superuser.render_kw = {'disabled': 'disabled'}

    if form.validate_on_submit():
        data = prepare_data(request)
        if me.get_id() == user_id:
            data.remove('email')

        rest.iface.update_user(user_id, data)

        session["locale"] = data['default_locale']
        refresh()
        return redirect(url_for('users.index'))

    return render_template('users/edit.html', form=form, known_users=[me])


@mod_users.route('/remove/<int:user_id>', methods=['GET', 'POST'])
@login_required
def remove(user_id: int):
    me = rest.iface.whoami()
    if me._user_id == user_id:
        return render_template('500.html')
