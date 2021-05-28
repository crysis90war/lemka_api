<div align="center">
  <img src="https://user-images.githubusercontent.com/32033245/119997358-eec5ad80-bfcf-11eb-84a6-84583263b944.png" width="50%">
  
  <h1>Bienvenue dans le dépôt "Lemka Api"</h1>
  
  <p>
    Travail de fin d’études en vue de l’obtention du diplôme de bachelier en informatique de gestion dans l'Enseignement de promotion sociale à EIC Ecaussinnes, 2020-2021.
  </p>

</div>

<br/>

## Table des matières

- [Introduction](#introduction)
- [Diagramme](#diagramme)
- [Requirements](#requirements)
- [Analyse de la base de données](#analyse-de-la-base-de-données)
- [Installation](#installation)
- [Autres](#autres)

# Introduction

...

# Diagramme

![alt text](https://github.com/crysis90war/lemka_api/blob/main/diagram.png?raw=true)

# Requirements

|                          Technology                          |      Version       | Technology | Version |
| :----------------------------------------------------------: | :----------------: |:---: | :---: |
|           [**Python**](https://docs.python.org/3/)           |      **3.x**       | [**django-cors-headers**](https://docs.python.org/3/) | **3.x** |
|           [**Django**](https://docs.djangoproject.com/en/3.1/)           |      **3.1.2**       | [**Python**](https://docs.python.org/3/) | **3.x** |
|           [**asgiref**](https://asgi.readthedocs.io/en/latest/)           |      **3.2.10**       | [**Python**](https://docs.python.org/3/) | **3.x** |
|           [**boto3**](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)           |      **1.16.60**       | [**Python**](https://docs.python.org/3/) | **3.x** |
|           [**botocore**](https://botocore.amazonaws.com/v1/documentation/api/latest/index.html)           |      **1.19.60**       | [**Python**](https://docs.python.org/3/) | **3.x** |
|           [**django-allauth**](https://botocore.amazonaws.com/v1/documentation/api/latest/index.html)           |      **1.19.60**       | [**Python**](https://docs.python.org/3/) | **3.x** |
|           [**django-crispy-forms**](https://botocore.amazonaws.com/v1/documentation/api/latest/index.html)           |      **1.19.60**       | [**Python**](https://docs.python.org/3/) | **3.x** |
|           [**django-registration**](https://botocore.amazonaws.com/v1/documentation/api/latest/index.html)           |      **1.19.60**       | [**Python**](https://docs.python.org/3/) | **3.x** |
|           [**django-rest-auth**](https://botocore.amazonaws.com/v1/documentation/api/latest/index.html)           |      **1.19.60**       | [**Python**](https://docs.python.org/3/) | **3.x** |
|           [**django-webpack-loader**](https://botocore.amazonaws.com/v1/documentation/api/latest/index.html)           |      **1.19.60**       | [**Python**](https://docs.python.org/3/) | **3.x** |
|           [**djangorestframework**](https://botocore.amazonaws.com/v1/documentation/api/latest/index.html)           |      **1.19.60**       | [**Python**](https://docs.python.org/3/) | **3.x** |

# Analyse de la base de données

## Les tables principales

<details><summary>Type Service</summary><br>
  
  | **Colonne**  | **Type**          | **Unique** | **Null** | **Blank** | **Par défaut** | **Description**                        |
  |--------------|-------------------|------------|----------|-----------|----------------|----------------------------------------|
  | id           | integer           | True       | False    | False     | auto_increment | Identifiant unique du type service     |
  | nom          | varchar(255)      | True       | False    | False     |                | Nom du type service                    |
  | duree_minute | integer(unsigned) | False      | False    | False     |                | Durée représentée en minute du service |
  
</details>

<details><summary>Article</summary><br>

| **Colonne**      | **Type**     | **Unique** | **Null** | **Blank** | **Par défaut** | **Description**                            |
|------------------|--------------|------------|----------|-----------|----------------|--------------------------------------------|
| id               | integer      | True       | False    | False     | auto_increment | Identifiant unique de l'article            |
| slug             | varchar(255) | True       | False    | False     |                | Slug unique de l'article                   |
| est_active       | bool         | False      | False    | False     | False          | État de publication de l'article           |
| titre            | varchar(255) | False      | False    | False     |                | Titre de l'article                         |
| description      | text         | False      | False    | True      |                | Description de l'article                   |
| created_at       | datetime     | False      | False    | False     |                | Date et heure de création de l'article     |
| updated_at       | datetime     | False      | False    | False     |                | Date et heure de modification de l'article |
| ref_type_service | integer      | False      | False    | False     |                | Clé étrangère liée au TypeService          |
| ref_catalogue    | integer      | False      | False    | False     |                | Clé étrangère liée au Catalogue            |

</details>

<details><summary>Tag</summary><br>

| **Colonne** | **Type**     | **Unique** | **Null** | **Blank** | **Par défaut** | **Description**            |
|-------------|--------------|------------|----------|-----------|----------------|----------------------------|
| id          | integer      | True       | False    | False     | auto_increment | Identifiant unique du tag  |
| nom         | varchar(255) | True       | False    | False     |                | Nom unique attribué au tag |

</details>

## Les tables associatives



# Installation

Assurez-vous que Python 3.x est installé et que la dernière version de pip est installée avant d'exécuter ces étapes.

Clonez le dépôt à l'aide de la commande suivante

```bash
git clone https://github.com/crysis90war/lemka_api.git
# Après le clonage, déplacez-vous dans le répertoire contenant les fichiers du projet
# à l'aide de la commande de changement de répertoire
cd lemka_api
```

Créez un environnement virtuel où tous les packages python requis seront installés

```bash
# Utilisez ceci sur Windows
python -m venv env
# Utilisez ceci sur Linux et Mac
python -m venv env
```

Activez l'environnement virtuel

```bash
# Windows
.\env\Scripts\activate
# Linux et Mac
source env/bin/activate
```

Installez toutes les exigences du projet

```bash
pip install -r requirements.txt
```

- Appliquez les migrations et créez votre superutilisateur (suivez les invites)

```bash
# appliquer les migrations et créer votre base de données
python manage.py migrate

# Créez un utilisateur avec manage.py
python manage.py createsuperuser
```

Exécutez le serveur de développement

```bash
# exécuter le serveur de développement django
python manage.py runserver
```

# Autres

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

  <details><summary><b>Semantic Commit Messages :</b></summary><br>
  
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

  </details>
  
