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
  - [Les tables principales](#les-tables-principales)
  - [Les tables associatives](#les-tables-associatives)
- [Installation](#installation)
- [Autres](#autres)

# Introduction

...

# Diagramme

![alt text](https://github.com/crysis90war/lemka_api/blob/main/diagram.png?raw=true)

# Requirements

[Requirements](lemka_api/requirements.txt)

# Analyse de la base de données

## Les tables principales

<details><summary>Pays</summary><br>

  | **Colonne** | **Type**     | **Unique** | **Null** | **Blank** | **Par défaut** | **Description**                 |
  |-------------|--------------|------------|----------|-----------|----------------|---------------------------------|
  | id          | integer      | True       | False    | False     | auto_increment | Identifiant unique              |
  | pays        | varchar(255) | True       | False    | False     |                | Le nom du pays                  |
  | code        | varchar(50)  | True       | False    | False     |                | Le code en lettres du pays 'BE' |

</details>

<details><summary>Ville</summary><br>

  | **Colonne**  | **Type**     | **Unique** | **Null** | **Blank** | **Par défaut** | **Description**               |
  |--------------|--------------|------------|----------|-----------|----------------|-------------------------------|
  | id           | integer      | True       | False    | False     | auto_increment | Identifiant unique            |
  | ville        | varchar(255) | False      | False    | False     |                | Le nom de la ville            |
  | code_postale | varchar(255) | False      | False    | False     |                | Le code postal de la ville    |
  | ref_pays_id  | integer      | False      | False    | False     |                | La clé étrangère liée au pays |

</details>

<details><summary>Entreprise_Lemka</summary><br>

  | **Colonne**      | **Type**     | **Unique** | **Null** | **Blank** | **Par défaut** | **Description**                                  |
  |------------------|--------------|------------|----------|-----------|----------------|--------------------------------------------------|
  | id               | integer      | True       | False    | False     | auto_increment | Identifiant unique                               |
  | nom_societe      | varchar(255) | False      | False    | False     |                | Le nom de l'entreprise                           |
  | ref_ville_id     | integer      | False      | False    | False     |                | Clé étrangère liée à la ville/commune            |
  | rue              | varchar(255) | False      | False    | False     |                | La rue où l'entreprise                           |
  | numero           | varchar(255) | False      | False    | False     |                | Le numéro d'adresse de l'entreprise              |
  | numero_tva       | varchar(254) | False      | False    | False     |                | Le numéro de TVA de l'entreprise                 |
  | numero_tel       | varchar(255) | False      | False    | False     |                | Le numéro de téléphone pour joindre l'entreprise |
  | mail_contact     | varchar(255) | False      | False    | False     |                | L'e-mail pour joindre l'entreprise               |
  | site_web         | varchar(255) | False      | False    | True      |                | Le site web de l'entreprise                      |
  | facebook_link    | varchar(255) | False      | False    | True      |                | Le lien vers la page facebook de l'entreprise    |
  | instagram_link   | varchar(255) | False      | False    | True      |                | Le lien vers la page instagram de l'entreprise   |
  | twitter_link     | varchar(255) | False      | False    | True      |                | Le lien vers la page twitter de l'entreprise     |
  | linkedin_link    | varchar(255) | False      | False    | True      |                | Le lien vers la page linkedin de l'entreprise    |
  | a_propos_resume  | varchar(255) | False      | False    | True      |                | Un petite description de l'entreprise            |
  | a_propos_complet | text         | False      | False    | True      |                | Une description complète de l'entreprise         |

</details>

<details><summary>Genre</summary><br>

  | **Colonne** | **Type**     | **Unique** | **Null** | **Blank** | **Par défaut** | **Description**             |
  |-------------|--------------|------------|----------|-----------|----------------|-----------------------------|
  | id          | integer      | True       | False    | False     | auto_increment | Identifiant unique du genre |
  | nom         | varchar(255) | True       | False    | False     |                | Nom unique du genre         |

</details>

<details><summary>User</summary><br>

| **Colonne**   | **Type**     | **Unique** | **Null** | **Blank** | **Par défaut** | **Description**                                                                  |
|---------------|--------------|------------|----------|-----------|----------------|----------------------------------------------------------------------------------|
| id            | integer      | True       | False    | False     | auto_increment | Identifiant unique de l'utilisateur                                              |
| password      | varchar(128) | False      | False    | False     |                | Mot de passe de l'utilisateur hashé et salé                                      |
| last_login    | datetime     | False      | False    | True      |                | La date et l'heure de la dernière connexion de l'utilisateur (non-utilisée)      |
| is_superuser  | bool         | False      | False    | False     | False          | L'utilisateur qui a la plus haute hiérarchie                                     |
| username      | varchar(255) | True       | False    | False     |                | Le pseudo unique de l'utilisateur (modifiable)                                   |
| email         | varchar(255) | True       | False    | False     |                | L'e-mail unique de l'utilisateur                                                 |
| image         | varchar(255) | False      | False    | False     | default.jpg    | Image de l'utilisateur. Image prédéfinie lors de la création du compte           |
| first_name    | varchar(255) | False      | False    | True      |                | Le prénom de l'utilisateur                                                       |
| last_name     | varchar(255) | False      | False    | True      |                | Le nom de l'utilisateur                                                          |
| numero_tel    | varchar(255) | False      | False    | True      |                | Le numéro de téléphone de l'utilisateur                                          |
| is_verified   | bool         | False      | False    | False     | False          | Le jeton généré sera envoyé par mail à l'utilisateur pour l'activation du compte |
| is_active     | bool         | False      | False    | False     | True           | Permet de bannir ou débannir l'utilisateur                                       |
| created_at    | datetime     | False      | False    | False     | auto_now_add   | La date et heure de création de l'utilisateur                                    |
| updated_at    | datetime     | False      | False    | False     | auto_add       | La date et heure du modification de l'utilisateur                                |
| auth_provider | varchar(255) | False      | False    | False     | email          | Fournisseur d'authentification                                                   |
| ref_genre_id  | integer      | False      | True     | True      |                | Clé étrangère liée au genre                                                      |

</details>

<details><summary>Adresse</summary><br>

  | **Colonne**  | **Type**     | **Unique** | **Null** | **Blank** | **Par défaut** | **Description**                    |
  |--------------|--------------|------------|----------|-----------|----------------|------------------------------------|
  | id           | integer      | True       | False    | False     | auto_increment | Identifiant unique                 |
  | rue          | varchar(255) | False      | False    | False     |                |                                    |
  | numero       | varchar(255) | False      | False    | False     |                | Le numéro du lieu de la résidence  |
  | boite        | varchar(255) | False      | False    | True      |                | La boite, si existe                |
  | ref_user_id  | integer      | False      | False    | False     |                | Clé étrangère liée à l'utilisateur |
  | ref_ville_id | integer      | False      | False    | False     |                | Clé étrangère liée à la ville      |

</details>

<details><summary>Mensuration</summary><br>

  | **Colonne** | **Type**     | **Unique** | **Null** | **Blank** | **Par défaut** | **Description**            |
  |-------------|--------------|------------|----------|-----------|----------------|----------------------------|
  | id          | integer      | True       | False    | False     | auto_increment | Identifiant unique         |
  | nom         | varchar(255) | True       | False    | False     |                | Le nom unique de la mesure |

</details>

<details><summary>User_Mensuration</summary><br>

  | **Colonne** | **Type**     | **Unique** | **Null** | **Blank** | **Par défaut** | **Description**                                          |
  |-------------|--------------|------------|----------|-----------|----------------|----------------------------------------------------------|
  | id          | integer      | True       | False    | False     | auto_increment | Identifiant unique                                       |
  | titre       | varchar(255) | False      | False    | False     |                | Le titre de la mensuration d'utilisateur                 |
  | is_main     | bool         | False      | False    | False     |                | Identifie si la mensuration est principale ou secondaire |
  | ref_user_id | integer      | False      | False    | False     |                | Clé étrangère liée à l'utilisateur                       |
  | remarque    | text         | False      | False    | True      |                | Remarque spécifique dont l'utilisateur va mentionner     |

</details>

<details><summary>Rayon</summary><br>

  | **Colonne** | **Type**     | **Unique** | **Null** | **Blank** | **Par défaut** | **Description**              |
  |-------------|--------------|------------|----------|-----------|----------------|------------------------------|
  | id          | integer      | True       | False    | False     | auto_increment | Identifiant unique du rayon  |
  | nom         | varchar(255) | True       | False    | False     |                | Nom unique attribué au rayon |

</details>

<details><summary>Section</summary><br>

  | **Colonne** | **Type**     | **Unique** | **Null** | **Blank** | **Par défaut** | **Description**                   |
  |-------------|--------------|------------|----------|-----------|----------------|-----------------------------------|
  | id          | integer      | True       | False    | False     | auto_increment | Identifiant unique de la section  |
  | nom         | varchar(255) | True       | False    | False     |                | Nom unique attribué à la section  |

</details>

<details><summary>Type_Produit</summary><br>

  | **Colonne** | **Type**     | **Unique** | **Null** | **Blank** | **Par défaut** | **Description**                     |
  |-------------|--------------|------------|----------|-----------|----------------|-------------------------------------|
  | id          | integer      | True       | False    | False     | auto_increment | Identifiant unique du type produit  |
  | nom         | varchar(255) | True       | False    | False     |                | Nom unique attribué au type produit |

</details>

<details><summary>Catalogue</summary><br>

| **Colonne**         | **Type** | **Unique** | **Null** | **Blank** | **Par défaut** | **Description**                    |
|---------------------|----------|------------|----------|-----------|----------------|------------------------------------|
| id                  | integer  | True       | False    | False     | auto_increment | Identifiant unique du catalogue    |
| ref_rayon_id        | integer  | False      | False    | False     |                | Clé étrangère liée au rayon        |
| ref_section_id      | integer  | False      | False    | False     |                | Clé étrangère liée à la section    |
| ref_type_produit_id | integer  | False      | False    | False     |                | Clé étrang!re liée au type produit |

</details>

<details><summary>Type_Service</summary><br>
  
  | **Colonne**  | **Type**          | **Unique** | **Null** | **Blank** | **Par défaut** | **Description**                        |
  |--------------|-------------------|------------|----------|-----------|----------------|----------------------------------------|
  | id           | integer           | True       | False    | False     | auto_increment | Identifiant unique du type service     |
  | nom          | varchar(255)      | True       | False    | False     |                | Nom du type service                    |
  | duree_minute | integer(unsigned) | False      | False    | False     |                | Durée représentée en minute du service |
  
</details>

<details><summary>Article</summary><br>

  | **Colonne**         | **Type**     | **Unique** | **Null** | **Blank** | **Par défaut** | **Description**                            |
  |---------------------|--------------|------------|----------|-----------|----------------|--------------------------------------------|
  | id                  | integer      | True       | False    | False     | auto_increment | Identifiant unique de l'article            |
  | slug                | varchar(255) | True       | False    | False     |                | Slug unique de l'article                   |
  | est_active          | bool         | False      | False    | False     | False          | État de publication de l'article           |
  | titre               | varchar(255) | False      | False    | False     |                | Titre de l'article                         |
  | description         | text         | False      | False    | True      |                | Description de l'article                   |
  | created_at          | datetime     | False      | False    | False     |                | Date et heure de création de l'article     |
  | updated_at          | datetime     | False      | False    | False     |                | Date et heure de modification de l'article |
  | ref_type_service_id | integer      | False      | False    | False     |                | Clé étrangère liée au TypeService          |
  | ref_catalogue_id    | integer      | False      | False    | False     |                | Clé étrangère liée au Catalogue            |

</details>

<details><summary>Article_Image</summary><br>
  
  | **Colonne**    | **Type**     | **Unique** | **Null** | **Blank** | **Par défaut** | **Description**                             |
  |----------------|--------------|------------|----------|-----------|----------------|---------------------------------------------|
  | id             | integer      | True       | False    | False     | auto_increment | Identifiant unique                          |
  | image          | varchar(255) | False      | False    | False     |                | L'url de l'image ou il sera stocké (AWS S3) |
  | is_main        | bool         | False      | False    | False     | True           | Première image sera vrai                    |
  | ref_article_id | integer      | False      | False    | False     |                | Clé étrangère liée à l'article              |
  
</details>

<details><summary>Tag</summary><br>

  | **Colonne** | **Type**     | **Unique** | **Null** | **Blank** | **Par défaut** | **Description**            |
  |-------------|--------------|------------|----------|-----------|----------------|----------------------------|
  | id          | integer      | True       | False    | False     | auto_increment | Identifiant unique du tag  |
  | nom         | varchar(255) | True       | False    | False     |                | Nom unique attribué au tag |

</details>

<details><summary>Demande_Devis</summary><br>

  | **Colonne**          | **Type**        | **Unique** | **Null** | **Blank** | **Par défaut** | **Description**                                                    |
  |----------------------|-----------------|------------|----------|-----------|----------------|--------------------------------------------------------------------|
  | id                   | integer         | True       | False    | False     | auto_increment | Identifiant unique                                                 |
  | numero_demande_devis | bigint unsigned | True       | False    | False     |                | Numéro de demande de devis unique généré automatiquement           |
  | titre                | varchar(255)    | False      | False    | False     |                | Titre donné à la demande par l'utilisateur                         |
  | remarque             | text            | False      | False    | False     |                | Une marque qui se précisée par l'utilisateur                       |
  | est_urgent           | bool            | False      | False    | False     | False          | L'utilisateur spécifie si la demande est urgent                    |
  | en_cours             | bool            | False      | False    | False     | False          | En cours de rédaction par l'utilisateur avant de soumettre         |
  | est_soumis           | bool            | False      | False    | False     | False          | Demande soumise par l'utilisateur pour le traitement               |
  | est_traite           | bool            | False      | False    | False     | False          | Demande de devis traité par gérante pour soumettre à l'utilisateur |
  | created_at           | datetime        | False      | False    | True      | auto_now_add   | Date et heure de création de la demande                            |
  | ref_article_id       | integer         | False      | True     | True      |                | Clé étrangère liée à l'article                                     |
  | ref_mensuration_id   | integer         | False      | False    | False     |                | Clé étrangère liée à la mensuration de l'utilisateur               |
  | ref_type_service     | integer         | False      | False    | False     |                | Clé étrangère liée au type service                                 |
  | ref_user_id          | integer         | False      | False    | False     |                | Clé étrangère liée à l'utilisateur                                 |

</details>

<details><summary>Devis</summary><br>

  | **Colonne**          | **Type**        | **Unique** | **Null** | **Blank** | **Par défaut** | **Description**                                            |
  |----------------------|-----------------|------------|----------|-----------|----------------|------------------------------------------------------------|
  | id                   | integer         | True       | False    | False     | auto_increment | Identifiant unique                                         |
  | numero_devis         | bigint unsinged | True       | False    | False     |                | Numéro de devis unique généré automatiquement              |
  | created_at           | datetime        | False      | False    | False     | auto_add_now   | Date et heure de création du devis                         |
  | updated_at           | datetime        | False      | False    | False     | auto_add       | Date et heure de la modification du devis                  |
  | remarque             | text            | False      | False    | True      |                | Remarque de la gérante si nécessaire                       |
  | est_accepte          | bool            | False      | True     | False     |                | Décision de l'utilisateur à l'égard du devis               |
  | est_soumis           | bool            | False      | False    | False     | False          | Devis est soumis à l'utilisateur pour qu'il puisse le voir |
  | ref_demande_devis_id | integer         | True       | False    | False     |                | Clé étrangère liée à la demande de devis                   |

</details>

<details><summary>TVA</summary><br>

  | **Colonne** | **Type** | **Unique** | **Null** | **Blank** | **Par défaut** | **Description**                          |
  |-------------|----------|------------|----------|-----------|----------------|------------------------------------------|
  | id          | integer  | True       | False    | False     | auto_increment | Identifiant unique                       |
  | taux        | float    | False      | False    | False     |                | Taux de TVA entre 0 et 1                 |
  | applicable  | bool     | False      | False    | False     | True           | Précise si le taux de TVA est applicable |

</details>

## Les tables associatives

<details><summary>User_Mesure</summary><br>

  | **Colonne**             | **Type** | **Unique** | **Null** | **Blank** | **Par défaut** | **Description**                              |
  |-------------------------|----------|------------|----------|-----------|----------------|----------------------------------------------|
  | id                      | integer  | True       | False    | False     | auto_increment | Identifiant unique                           |
  | ref_mensuration_id      | integer  | False      | False    | False     |                | Clé étrangère liée à la mensuration          |
  | ref_user_mensuration_id | integer  | False      | False    | False     |                | Clé étrangère liée à user mensuration        |
  | mesure                  | float    | False      | False    | False     | 0.00           | La mesure de la mensuration de l'utilisateur |

</details>

<details><summary>Article_Ref_Tags</summary><br>

  | **Colonne** | **Type** | **Unique** | **Null** | **Blank** | **Par défaut** | **Description**                |
  |-------------|----------|------------|----------|-----------|----------------|--------------------------------|
  | id          | integer  | True       | False    | False     | auto_increment | Identifiant unique du tag      |
  | article_id  | integer  | False      | False    | False     |                | Clé étrangère liée à l'article |
  | tag_id      | integer  | False      | False    | False     |                | Clé étrangère liée au tag      |

</details>

<details><summary>Article_Likes</summary><br>

  | **Colonne** | **Type** | **Unique** | **Null** | **Blank** | **Par défaut** | **Description**                    |
  |-------------|----------|------------|----------|-----------|----------------|------------------------------------|
  | id          | integer  | True       | False    | False     | auto_increment | Identifiant unique du like         |
  | article_id  | integer  | False      | False    | False     |                | Clé étrangère liée à l'article     |
  | user_id     | integer  | False      | False    | False     |                | Clé étrangère liée à l'utilisateur |

</details>

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
  
