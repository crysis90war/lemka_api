# Generated by Django 3.1.2 on 2021-04-23 14:29

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import lemka.manager
import lemka.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(db_index=True, max_length=255, unique=True)),
                ('email', models.EmailField(db_index=True, max_length=255, unique=True)),
                ('image', models.ImageField(default='default.jpg', upload_to=lemka.utils.path_and_rename_user_image)),
                ('first_name', models.CharField(blank=True, default='', max_length=255)),
                ('last_name', models.CharField(blank=True, default='', max_length=255)),
                ('numero_tel', models.CharField(blank=True, default='', max_length=255)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('auth_provider', models.CharField(default='email', max_length=255)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', lemka.manager.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('slug', models.SlugField(blank=True, editable=False, max_length=255, unique=True)),
                ('est_active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('likes', models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Caracteristique',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'ordering': ['nom'],
            },
        ),
        migrations.CreateModel(
            name='Couleur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DemandeDevis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_demande_devis', models.PositiveBigIntegerField(unique=True)),
                ('titre', models.CharField(max_length=255)),
                ('remarque', models.TextField()),
                ('est_urgent', models.BooleanField(default=False)),
                ('est_soumis', models.BooleanField(default=False)),
                ('en_cours', models.BooleanField(default=False)),
                ('est_traite', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ref_article', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lemka.article')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Devis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_devis', models.PositiveBigIntegerField(unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('remarque', models.TextField(blank=True, default='')),
                ('est_accepte', models.BooleanField(null=True)),
                ('est_soumis', models.BooleanField(default=False)),
                ('ref_demande_devis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lemka.demandedevis')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Horaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jour', models.CharField(max_length=255)),
                ('jour_semaine', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(7)])),
                ('heure_ouverture', models.TimeField(blank=True, null=True)),
                ('pause_debut', models.TimeField(blank=True, null=True)),
                ('pause_fin', models.TimeField(blank=True, null=True)),
                ('heure_fermeture', models.TimeField(blank=True, null=True)),
                ('sur_rdv', models.BooleanField()),
                ('est_ferme', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Mensuration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Mercerie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=255, unique=True)),
                ('nom', models.CharField(max_length=255)),
                ('est_publie', models.BooleanField(default=False)),
                ('description', models.TextField(default='')),
                ('prix_u_ht', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(999999999.99)])),
                ('stock', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(999999.9)])),
                ('ref_categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lemka.categorie')),
                ('ref_couleur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lemka.couleur')),
            ],
            options={
                'ordering': ['nom', 'ref_couleur__nom'],
            },
        ),
        migrations.CreateModel(
            name='Pays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pays', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Rayon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rayon', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'ordering': ['section'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taux', models.FloatField(unique=True)),
                ('applicable', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['taux'],
            },
        ),
        migrations.CreateModel(
            name='TypeProduit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_produit', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'ordering': ['type_produit'],
            },
        ),
        migrations.CreateModel(
            name='TypeService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_service', models.CharField(max_length=255, unique=True)),
                ('duree_minute', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(180)])),
            ],
        ),
        migrations.CreateModel(
            name='UserMensuration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=255)),
                ('is_main', models.BooleanField(default=False)),
                ('ref_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mensurations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['ref_user__username', '-is_main', 'titre'],
            },
        ),
        migrations.CreateModel(
            name='Ville',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ville', models.CharField(max_length=255)),
                ('code_postale', models.CharField(max_length=255)),
                ('ref_pays', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lemka.pays')),
            ],
            options={
                'ordering': ['ville'],
            },
        ),
        migrations.CreateModel(
            name='UserMensurationMesure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mesure', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(260.0)])),
                ('ref_mensuration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Mensuration', to='lemka.mensuration')),
                ('ref_user_mensuration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lemka.usermensuration')),
            ],
            options={
                'ordering': ['ref_user_mensuration__ref_user__username', '-ref_user_mensuration__is_main', 'ref_mensuration__id'],
            },
        ),
        migrations.CreateModel(
            name='RendezVous',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start', models.TimeField(blank=True, null=True)),
                ('end', models.TimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('est_annule', models.BooleanField(default=False)),
                ('ref_devis', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='devis', to='lemka.devis')),
                ('ref_type_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lemka.typeservice', verbose_name='service')),
                ('ref_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
        ),
        migrations.CreateModel(
            name='MercerieImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpg', upload_to=lemka.utils.path_and_rename_mercerie_image)),
                ('is_main', models.BooleanField(default=False)),
                ('ref_mercerie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='lemka.mercerie')),
            ],
            options={
                'ordering': ['ref_mercerie__nom', '-is_main'],
            },
        ),
        migrations.CreateModel(
            name='MercerieCaracteristique',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valeur', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(999999999.99)])),
                ('ref_caracteristique', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lemka.caracteristique')),
                ('ref_mercerie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='catacteristiques', to='lemka.mercerie')),
            ],
            options={
                'ordering': ['ref_mercerie__nom'],
            },
        ),
        migrations.AddField(
            model_name='mercerie',
            name='ref_tva',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tva', to='lemka.tva'),
        ),
        migrations.CreateModel(
            name='EntrepriseLemka',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_societe', models.CharField(max_length=255)),
                ('rue', models.CharField(max_length=255)),
                ('numero', models.CharField(max_length=255)),
                ('numero_tva', models.CharField(max_length=255)),
                ('mail_contact', models.EmailField(max_length=254)),
                ('numero_tel', models.CharField(max_length=255)),
                ('site_web', models.CharField(max_length=255)),
                ('ref_ville', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lemka.ville')),
            ],
        ),
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(max_length=255)),
                ('prix_u_ht', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantite', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(999999999.0)])),
                ('ref_devis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='lemka.devis')),
                ('ref_tva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lemka.tva')),
            ],
        ),
        migrations.AddField(
            model_name='demandedevis',
            name='ref_mensuration',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lemka.usermensuration'),
        ),
        migrations.AddField(
            model_name='demandedevis',
            name='ref_merceries',
            field=models.ManyToManyField(blank=True, related_name='merceries', to='lemka.Mercerie'),
        ),
        migrations.AddField(
            model_name='demandedevis',
            name='ref_type_service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lemka.typeservice'),
        ),
        migrations.AddField(
            model_name='demandedevis',
            name='ref_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='DemadeDevisImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=lemka.utils.path_and_rename_demande_devis_image)),
                ('ref_demande_devis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lemka.demandedevis')),
            ],
        ),
        migrations.CreateModel(
            name='Catalogue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_rayon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lemka.rayon')),
                ('ref_section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lemka.section')),
                ('ref_type_produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lemka.typeproduit')),
            ],
            options={
                'ordering': ['ref_rayon', 'ref_section', 'ref_type_produit'],
            },
        ),
        migrations.CreateModel(
            name='ArticleImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpg', upload_to=lemka.utils.path_and_rename_article_image)),
                ('is_main', models.BooleanField(default=False)),
                ('ref_article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imgs', to='lemka.article')),
            ],
            options={
                'ordering': ['ref_article__slug', '-is_main'],
            },
        ),
        migrations.AddField(
            model_name='article',
            name='ref_catalogue',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='lemka.catalogue'),
        ),
        migrations.AddField(
            model_name='article',
            name='ref_tags',
            field=models.ManyToManyField(blank=True, related_name='tags', to='lemka.Tag'),
        ),
        migrations.AddField(
            model_name='article',
            name='ref_type_service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lemka.typeservice'),
        ),
        migrations.CreateModel(
            name='Adresse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rue', models.CharField(max_length=255)),
                ('numero', models.CharField(max_length=255)),
                ('boite', models.CharField(blank=True, max_length=255)),
                ('ref_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adresses', to=settings.AUTH_USER_MODEL)),
                ('ref_ville', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lemka.ville')),
            ],
            options={
                'ordering': ['ref_user__email', 'ref_ville__ville'],
            },
        ),
        migrations.AddField(
            model_name='user',
            name='ref_genre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lemka.genre', verbose_name='Sexe'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
