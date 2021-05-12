# LEMKA - Atelier de couture
Travail de fin d’études en vue de l’obtention du Diplôme de bachelier en Informatique de Gestion dans l'Enseignement de Promotion Sociale à EIC Ecaussinnes.

## Outils & Technologie

### Backend | Django 3.1.2 - Python 3.8
<details><summary><b>Commande(s) :</b></summary><br>
  
> - pip install
> - pip freeze > requirements.txt
> - python manage.py makemigrations
> - python manage.py migrate
> - python manage.py createsuperuser
> - python manage.py dumpdata app.class > class.json
> - python manage.py loaddata app.class < class.json
> - python manage.py loaddata class.json
  
</details>

- django-allauth
- django-crispy-forms
- django-registration
- django-rest-auth
- django-webpack-loader
- djangorestframework
- django-cors-headers

![alt text](https://github.com/crysis90war/lemka_api/blob/main/diagram.png?raw=true)

### Semantic Commit Messages
> - feat - A new feature
> - fix - A bug fix
> - docs - Documentation only changes
> - style - Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
> - refactor - A code change that neither fixes a bug nor adds a feature
> - perf - A code change that improves performance
> - test - Adding missing tests or correcting existing tests
> - build - Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)
> - ci - Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs)
> - chore - Other changes that don't modify src or test files
> - revert - Reverts a previous commit