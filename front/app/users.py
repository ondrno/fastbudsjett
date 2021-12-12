from flask import (
    Blueprint, render_template, redirect, session, url_for, request
)
from flask_wtf import FlaskForm
from wtforms import SubmitField, EmailField, RadioField, SelectField
from wtforms.validators import InputRequired, Email, DataRequired

from .auth import login_required
from . import rest, utils


bp = Blueprint('users', __name__)


class UsersForm(FlaskForm):
    email = EmailField('Email address', [DataRequired(), Email()])
    default_locale = SelectField('Language', choices=[('en', 'English'), ('de', 'Deutsch')],
                                 validators=[InputRequired()])
    submit = SubmitField('Update')


def prepare_data(r: request):
    data = {'email': r.form['email'],
            'default_locale': r.form['default_locale'],
            }
    return data


@bp.route('/users', methods=['GET'])
@login_required
def index():
    current_user = rest.iface.whoami()
    me = {'id': current_user._user_id, 'email': current_user._email, 'default_locale': current_user._default_locale}
    users = [me]
    return render_template('users/index.html', known_users=users)


@bp.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit(user_id: int):
    me = rest.iface.whoami()
    form = UsersForm(default_locale=me._default_locale, email=me._email)
    if form.validate_on_submit():

        data = prepare_data(request)
        rest.iface.update_user(user_id, data)

        # show the same month as the date of the item which was created/modified
        session["locale"] = data['default_locale']
        return redirect(url_for('users.index'))

    return render_template('users/edit.html', form=form, known_users=[me])
