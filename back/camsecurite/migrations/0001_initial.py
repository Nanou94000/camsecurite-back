# Generated by Django 4.0.2 on 2022-04-05 23:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='caracteristique',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(help_text='un nom de la caracteristique ex: Résolution', max_length=100)),
                ('valeur', models.TextField(blank=True, help_text='une valeur de la caracteristique ex: Résolution -> 4K', max_length=200)),
            ],
            options={
                'ordering': ['valeur'],
            },
        ),
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.TextField(help_text='nom de la catégorie', max_length=100)),
                ('sousNom', models.TextField(help_text='breve description de la catégorie', max_length=200)),
                ('description', models.TextField(help_text='une description detaillé de la catégorie', max_length=200)),
                ('image', models.ImageField(default=0, upload_to=None)),
                ('imageBanniere', models.ImageField(default=0, upload_to=None)),
            ],
            options={
                'ordering': ['nom'],
            },
        ),
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('payer', models.BooleanField(default=False)),
                ('date_payer', models.DateTimeField(auto_now_add=True)),
                ('etat', models.TextField(choices=[('none', 'none'), ('payé', 'payé'), ('non payé', 'non payé'), ('validé: préparation en cours', 'validé: préparation en cours'), ('préparé', 'préparé'), ('expedié', 'expedié'), ('en cours de livraison', 'en cours de livraison'), ('livré', 'livré')])),
                ('total', models.FloatField(default=0, null=True)),
                ('numerosuivie', models.CharField(default='inconnu', max_length=100, null=True)),
                ('promo', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['date_payer'],
            },
        ),
        migrations.CreateModel(
            name='CommandeNonLogin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sexe', models.TextField(choices=[('H', 'homme'), ('F', 'femme'), ('O', 'Autre')], default='H')),
                ('prenom', models.CharField(default='', max_length=200)),
                ('nom', models.CharField(default='', max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('adresse', models.CharField(default='', max_length=200)),
                ('code_postal', models.CharField(default='*****', max_length=6)),
                ('ville', models.CharField(default='', max_length=50)),
                ('pays', models.CharField(default='', max_length=50)),
                ('telephone', models.CharField(blank=True, max_length=15)),
                ('payer', models.BooleanField(default=False)),
                ('date_payer', models.DateTimeField(auto_now_add=True)),
                ('etat', models.TextField(choices=[('none', 'none'), ('payé', 'payé'), ('non payé', 'non payé'), ('validé: préparation en cours', 'validé: préparation en cours'), ('préparé', 'préparé'), ('expedié', 'expedié'), ('en cours de livraison', 'en cours de livraison'), ('livré', 'livré')])),
                ('total', models.FloatField(default=0, null=True)),
                ('numerosuivie', models.CharField(default='inconnu', max_length=100, null=True)),
                ('promo', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['date_payer'],
            },
        ),
        migrations.CreateModel(
            name='Livreur',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=500)),
                ('delai', models.CharField(default='', max_length=100)),
                ('image', models.ImageField(default=0, upload_to=None)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'ordering': ['email'],
            },
        ),
        migrations.CreateModel(
            name='Panier',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('total', models.FloatField(default=0, null=True)),
                ('totaltotal', models.FloatField(default=0, null=True)),
                ('totalaveclivraison', models.FloatField(default=0, null=True)),
                ('poids', models.FloatField(default=0, help_text='poids du panier', null=True)),
                ('promo', models.BooleanField(default=False)),
                ('freeshipping', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['total'],
            },
        ),
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(help_text='nom du produit', max_length=100, unique=True)),
                ('sousNom', models.CharField(help_text='sous-nom du produit', max_length=200, unique=True)),
                ('descriptionCourte', models.TextField(help_text='une description attractif du produit', max_length=20000)),
                ('descriptionLongue', models.TextField(blank=True, default='', help_text='une description attractif du produit', max_length=90000)),
                ('prix', models.FloatField(help_text='le prix de vente du produit en euro')),
                ('prixSansReduction', models.FloatField(help_text='le prix avant reduction du produit en euro')),
                ('image1', models.ImageField(default='null', null=True, upload_to=None)),
                ('image2', models.ImageField(default='null', null=True, upload_to=None)),
                ('image3', models.ImageField(default='null', null=True, upload_to=None)),
                ('image4', models.ImageField(default='null', null=True, upload_to=None)),
                ('image5', models.ImageField(default='null', null=True, upload_to=None)),
                ('image6', models.ImageField(default='null', null=True, upload_to=None)),
                ('resolution', models.TextField(choices=[('none', 'none'), ('1080', 'hd'), ('2160', 'hd+'), ('4320', '4k'), ('8640', '8k')])),
                ('poids', models.FloatField(help_text='poids du produit en gramme', null=True)),
                ('date_ajout', models.DateTimeField()),
                ('note', models.FloatField(blank=True, default=0, null=True)),
                ('nb_vente', models.IntegerField(default=0, null=True)),
                ('cartesd', models.BooleanField(default=True)),
                ('stock', models.IntegerField(default=1)),
                ('caracteristiques', models.ManyToManyField(blank=True, default='', null=True, to='camsecurite.caracteristique')),
                ('categorie', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='camsecurite.categorie')),
            ],
        ),
        migrations.CreateModel(
            name='Promo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=50)),
                ('description', models.TextField(default='', help_text='profiter de XX% de reduction avec le code XXX', max_length=200)),
                ('reduction_pourcentage', models.IntegerField(default=0, null=True)),
                ('valide', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sexe', models.TextField(choices=[('H', 'homme'), ('F', 'femme'), ('O', 'Autre')], default='H')),
                ('adresse', models.CharField(default='', max_length=200)),
                ('code_postal', models.CharField(default='*****', max_length=6)),
                ('ville', models.CharField(default='', max_length=50)),
                ('pays', models.CharField(default='', max_length=50)),
                ('telephone', models.CharField(blank=True, max_length=15)),
                ('is_active', models.BooleanField(default=False)),
                ('reset_mdp', models.BooleanField(default=False)),
                ('notification', models.BooleanField(default=False)),
                ('notif_commande', models.BooleanField(default=False)),
                ('notif_msg', models.BooleanField(default=False)),
                ('notif_avis', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProduitPanierHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_ajout', models.DateTimeField(auto_now_add=True)),
                ('quantite', models.IntegerField(default=0)),
                ('total', models.FloatField(default=0, null=True)),
                ('commande', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='camsecurite.commande')),
                ('panier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='camsecurite.panier')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='camsecurite.produit')),
            ],
            options={
                'ordering': ['date_ajout'],
            },
        ),
        migrations.CreateModel(
            name='ProduitPanier',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_ajout', models.DateTimeField(auto_now_add=True)),
                ('quantite', models.IntegerField(default=0)),
                ('total', models.FloatField(default=0, null=True)),
                ('panier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='camsecurite.panier')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='camsecurite.produit')),
            ],
            options={
                'ordering': ['date_ajout'],
            },
        ),
        migrations.CreateModel(
            name='ProduitCommandeNonLogin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantite', models.IntegerField(default=0)),
                ('total', models.FloatField(default=0, null=True)),
                ('commande', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='camsecurite.commandenonlogin')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='camsecurite.produit')),
            ],
            options={
                'ordering': ['total'],
            },
        ),
        migrations.CreateModel(
            name='ProduitCaracteristique',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('caracteristique', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='camsecurite.caracteristique')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='camsecurite.produit')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='PrixLivraison',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('min_poids', models.IntegerField(default=0)),
                ('max_poids', models.IntegerField(default=0)),
                ('description', models.CharField(default='prix pour un colis entre xx et xx gramme', max_length=500)),
                ('prix', models.FloatField()),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='camsecurite.livreur')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='panier',
            name='codepromo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='camsecurite.promo'),
        ),
        migrations.AddField(
            model_name='panier',
            name='livraison',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='camsecurite.prixlivraison'),
        ),
        migrations.AddField(
            model_name='panier',
            name='produitspanier',
            field=models.ManyToManyField(through='camsecurite.ProduitPanier', to='camsecurite.Produit'),
        ),
        migrations.AddField(
            model_name='panier',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='camsecurite.profile'),
        ),
        migrations.CreateModel(
            name='Paiement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('etat', models.BooleanField(default=False, help_text='Paiement accepté ou pas')),
                ('date_payer', models.DateTimeField(auto_now_add=True)),
                ('mode', models.TextField(choices=[('CB', 'carte bancaire'), ('PP', 'paypal')])),
                ('commande', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='camsecurite.commande')),
                ('profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='camsecurite.profile')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('titre', models.CharField(max_length=100)),
                ('contenu', models.TextField()),
                ('expediteur', models.CharField(default='Administrateur de Sauron Securite', max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('etat', models.BooleanField(default=False, help_text='état de la commande')),
                ('lu', models.BooleanField(default=False, help_text='lu ou pas')),
                ('profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='camsecurite.profile')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='commandenonlogin',
            name='codepromo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='camsecurite.promo'),
        ),
        migrations.AddField(
            model_name='commandenonlogin',
            name='livraison',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='camsecurite.prixlivraison'),
        ),
        migrations.AddField(
            model_name='commande',
            name='codepromo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='camsecurite.promo'),
        ),
        migrations.AddField(
            model_name='commande',
            name='livraison',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='camsecurite.prixlivraison'),
        ),
        migrations.AddField(
            model_name='commande',
            name='panier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='camsecurite.panier'),
        ),
        migrations.AddField(
            model_name='commande',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='camsecurite.profile'),
        ),
        migrations.CreateModel(
            name='AvisProduit',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('valide', models.BooleanField(default=True)),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='camsecurite.produit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Avis',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('titre', models.TextField(default='', max_length=20)),
                ('contenu', models.TextField(default='', max_length=500)),
                ('note', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('produit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='camsecurite.produit')),
                ('profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='camsecurite.profile')),
            ],
            options={
                'ordering': ['profile'],
            },
        ),
    ]
