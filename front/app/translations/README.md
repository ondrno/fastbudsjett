# How to update translations
- Extract the ``_()`` or ``lazy_text()`` occurences from all python and jinja files:
    

    ~/fastbudsjett/front/app $  pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .

- Merge the changes with the existing translations:


    ~/fastbudsjett/front/app $  pybabel update -i messages.pot -d translations

- Compile the translations:


    ~/fastbudsjett/front/app $  pybabel compile -d translations


See further: [flask-babel documentation](https://flask-babel.tkte.ch/)