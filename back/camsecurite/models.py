from asyncio.windows_events import NULL
from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.db import models
from django.db.models.expressions import ValueRange
from django.db.models.fields import BooleanField, CharField, DateTimeField, EmailField, IntegerField
from django.urls import reverse # Cette fonction est utilisée pour formater les URL

# Create your models here.
class Profile(models.Model):    
    SEXE = (
    ("H","homme"),
    ("F","femme"),
    ("O",'Autre'),
    )
    sexe = models.TextField(choices=SEXE,default="H")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    adresse = models.CharField(max_length=200,default="")
    code_postal = models.CharField(max_length=6,default="*****")
    ville = models.CharField(max_length=50,default="")
    pays = models.CharField(max_length=50,default="")
    telephone = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=False)
    reset_mdp = models.BooleanField(default=False)
    notification = models.BooleanField(default=False)
    notif_commande = models.BooleanField(default=False)
    notif_msg = models.BooleanField(default=False)
    notif_avis = models.BooleanField(default=False)
    

from django.conf import settings
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
@receiver(post_save, sender=Profile)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Panier.objects.create(profile=instance)


class Produit(models.Model):
    """Classe qui définit un produit du site web: sauron securite"""
    #champs de formulaire    
    RESOLUTION_CHOICES = (
    ("none","none"),
    ("1080","hd"),
    ("2160",'hd+'),
    ("4320","4k"),
    ("8640","8k")
    )
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100,help_text="nom du produit",unique=True)
    sousNom = models.CharField(max_length=200,help_text="sous-nom du produit",unique=True)
    descriptionCourte = models.TextField(null=False,max_length=20000,help_text="une description attractif du produit")
    descriptionLongue = models.TextField(null=False,max_length=90000,help_text="une description attractif du produit",default="",blank=True)
    prix = models.FloatField(help_text="le prix de vente du produit en euro")
    prixSansReduction = models.FloatField(help_text="le prix avant reduction du produit en euro")
    image1 = models.ImageField(null=True, upload_to=None, height_field=None, width_field=None, max_length=100,default="null")
    image2 = models.ImageField(null=True, upload_to=None, height_field=None, width_field=None, max_length=100,default="null")
    image3 = models.ImageField(null=True, upload_to=None, height_field=None, width_field=None, max_length=100,default="null")
    image4 = models.ImageField(null=True, upload_to=None, height_field=None, width_field=None, max_length=100,default="null")
    image5 = models.ImageField(null=True, upload_to=None, height_field=None, width_field=None, max_length=100,default="null")
    image6 = models.ImageField(null=True, upload_to=None, height_field=None, width_field=None, max_length=100,default="null")
    resolution = models.TextField(choices=RESOLUTION_CHOICES,default='none')
    poids = models.FloatField(null=True,help_text="poids du produit en gramme")
    date_ajout = models.DateTimeField(auto_now_add=True)
    note = models.FloatField(null=True,default=0,blank=True)
    nb_vente = models.IntegerField(default=0,null=True)
    cartesd = models.BooleanField(default=True)
    stock = models.IntegerField(null=False, default=1)
    categorie = models.ForeignKey('Categorie', on_delete=models.SET_NULL, null=True)
    caracteristiques = models.ManyToManyField("caracteristique", null=True, blank=True, default='')

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.nom
class Categorie(models.Model):
    """Classe qui définit les differentes categories du site: sauron securite"""
    #champs de formulaire    
    id = models.AutoField(primary_key=True)
    nom = models.TextField(max_length=100,help_text="nom de la catégorie")
    sousNom = models.TextField(max_length=200,help_text="breve description de la catégorie")
    description = models.TextField(max_length=200,help_text="une description detaillé de la catégorie")
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100,default=0)
    imageBanniere = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100,default=0)

    class Meta:
        ordering = ['nom',]
    
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.nom

class AvisManager(models.Manager):
    def create_commentaire(self,user_id,produitid,titre_com,contenu_com,note_com):
        avis = self.create(profile_id=user_id,produit_id=produitid,titre=titre_com,contenu=contenu_com,note=note_com)
        return avis

class Avis(models.Model):
    id = models.AutoField(primary_key=True)
    profile = models.ForeignKey("Profile",on_delete=models.SET_NULL, null=True)
    titre = models.TextField(max_length=20,null=False,default="")
    contenu = models.TextField(max_length=500,null=False,default="")
    note = models.IntegerField(null=False,default=0)
    date = models.DateTimeField(auto_now_add=True,null=True)
    produit = models.ForeignKey("Produit",on_delete=models.SET_NULL, null=True)
    objects = AvisManager()
    class Meta:
        ordering = ['profile',]

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.titre

class PanierManager(models.Manager):
    def create_panier(self,userinfo):
        panier = self.create(profile_id=userinfo)
        return panier

class Panier(models.Model):
    """Classe qui définit les differentes categories du site: sauron securite"""
    id = models.AutoField(primary_key=True)
    profile = models.ForeignKey("Profile",on_delete=models.SET_NULL, null=True)
    produitspanier = models.ManyToManyField(Produit,through='ProduitPanier')
    total = models.FloatField(null=True,default=0)
    totaltotal = models.FloatField(null=True,default=0)
    totalaveclivraison = models.FloatField(null=True,default=0)
    poids = models.FloatField(null=True,help_text="poids du panier",default=0)
    livraison = models.ForeignKey("PrixLivraison",on_delete=models.SET_NULL,blank=True, null=True)
    promo = models.BooleanField(default=False)
    codepromo = models.ForeignKey("Promo",on_delete=models.SET_NULL,blank=True,null=True)
    objects = PanierManager()
    freeshipping = models.BooleanField(default=False)
    class Meta:
        ordering = ['total',]

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.id)

from datetime import datetime

class ProduitPanierManager(models.Manager):
    def lier_produit_panier(self,produit, panier,qte):
        panier = self.create(produit_id=produit, panier_id=panier,quantite=qte)
        return panier
class ProduitPanier(models.Model):
    id = models.AutoField(primary_key=True)
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    date_ajout = models.DateTimeField(auto_now_add=True)
    quantite = models.IntegerField(null=False,default=0)
    total = models.FloatField(null=True,default=0)
    objects = ProduitPanierManager()
    class Meta:
        ordering = ['date_ajout',]

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.id)

class CommandeManager(models.Manager):
    def create_commande(self,user_id,pay,eta):
        p=Panier.objects.get(profile_id=user_id)
        commande = self.create(profile_id=user_id,panier_id=p,payer=pay,etat=eta)
        return commande

class Commande(models.Model):
    ETAT = (
    ("none","none"),
    ("payé","payé"),
    ("non payé",'non payé'),
    ("validé: préparation en cours","validé: préparation en cours"),
    ("préparé","préparé"),
    ("expedié","expedié"),
    ("en cours de livraison","en cours de livraison"),
    ("livré","livré")
    )
    """Classe qui définit les differentes categories du site: sauron securite"""
    #champs de formulaire
    id = models.AutoField(primary_key=True)
    profile = models.ForeignKey("Profile",on_delete=models.SET_NULL, null=True)
    panier = models.ForeignKey("Panier",on_delete=models.SET_NULL, null=True)
    payer = models.BooleanField(default=False)
    date_payer = models.DateTimeField(auto_now_add=True)
    date_livraison = models.TextField(default="pas encore livré",null=True,blank=True)
    etat = models.TextField(choices=ETAT)
    total = models.FloatField(null=True,default=0)
    livraison = models.ForeignKey("PrixLivraison",on_delete=models.SET_NULL, null=True)
    numerosuivie= models.CharField(null=True, max_length=100,default="inconnu")
    promo = models.BooleanField(default=False)
    codepromo = models.ForeignKey("Promo",on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        ordering = ['date_payer',]

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.id)

class Paiement (models.Model):
    """Classe qui définit les differentes categories du site: sauron securite"""
    #champs de formulaire
    MODE_PAIEMENT = (
        ("CB","carte bancaire"),
        ("PP","paypal"),
    )
    id = models.AutoField(primary_key=True)
    profile = models.ForeignKey("Profile",on_delete=models.SET_NULL, null=True)
    commande = models.ForeignKey("Commande",on_delete=models.SET_NULL, null=True)
    etat = models.BooleanField(default=False,help_text="Paiement accepté ou pas")
    date_payer = models.DateTimeField(auto_now_add=True)
    mode = models.TextField(choices=MODE_PAIEMENT)



    class Meta:
        ordering = ['id',]

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.id

class Message (models.Model):
    """Classe qui définit les differentes categories du site: sauron securite"""
    #champs de formulaire
    id = models.AutoField(primary_key=True)
    profile = models.ForeignKey("Profile",on_delete=models.SET_NULL, null=True)
    titre = models.CharField(null=False ,max_length=100)
    contenu = models.TextField(null=False)
    expediteur = models.CharField(null=False,default="Administrateur de Sauron Securite",max_length=100)
    date = models.DateTimeField(auto_now_add=True,null=True)
    etat = models.BooleanField(default=False,help_text="état de la commande")
    lu = models.BooleanField(default=False,help_text="lu ou pas")
    
    class Meta:
        ordering = ['id',]

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.titre)

class Livreur (models.Model):
    """Classe qui définit les differentes categories du site: sauron securite"""
    #champs de formulaire
    id = models.AutoField(primary_key=True)
    nom = models.CharField(null=False ,max_length=50)
    description = models.TextField(null=False ,max_length=500)
    delai = models.CharField(null=False,default="",max_length=100)
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100,default=0)


    class Meta:
        ordering = ['id',]

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.nom)

class PrixLivraison (models.Model):
    """Classe qui définit les differentes categories du site: sauron securite"""
    #champs de formulaire
    id = models.AutoField(primary_key=True)
    min_poids = models.IntegerField(null=False ,default=0)
    max_poids = models.IntegerField(null=False ,default=0)
    description = models.CharField(max_length=500,default="prix pour un colis entre xx et xx gramme")
    prix = models.FloatField(null=False)
    type = models.ForeignKey("Livreur",on_delete=models.SET_NULL, null=True)



    class Meta:
        ordering = ['id',]

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.type.nom)


class ProduitPanierHistory(models.Model):
    id = models.AutoField(primary_key=True)
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    date_ajout = models.DateTimeField(auto_now_add=True)
    quantite = models.IntegerField(null=False,default=0)
    total = models.FloatField(null=True,default=0)
    commande = models.ForeignKey('Commande', on_delete=models.CASCADE)
    class Meta:
        ordering = ['date_ajout',]

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.produit.nom)

class Newsletter (models.Model):
    """Classe qui définit les differentes categories du site: sauron securite"""
    #champs de formulaire
    id = models.AutoField(primary_key=True)
    email = models.EmailField(null=False ,max_length=100)
    date = models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        ordering = ['email',]

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.email)

class Promo (models.Model):
    """Classe qui définit les differentes categories du site: sauron securite"""
    #champs de formulaire
    id = models.AutoField(primary_key=True)
    nom = models.CharField(null=False ,max_length=50)
    description = models.TextField(null=False,max_length=200,help_text="profiter de XX% de reduction avec le code XXX",default="")
    reduction_pourcentage = models.IntegerField(default=0,null=True)
    valide = models.BooleanField(default=False)

    class Meta:
        ordering = ['id',]

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.nom)

class caracteristique (models.Model):
    """Classe qui définit les differentes categories du site: sauron securite"""
    #champs de formulaire
    id = models.AutoField(primary_key=True)
    nom = models.CharField(null=False ,max_length=100,help_text="un nom de la caracteristique ex: Résolution")
    valeur = models.TextField(null=False,max_length=200,help_text="une valeur de la caracteristique ex: Résolution -> 4K",blank=True)
    class Meta:
        ordering = ['valeur',]

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(f'{self.nom} - {self.valeur}')

class ProduitCaracteristique(models.Model):
    id = models.AutoField(primary_key=True)
    caracteristique = models.ForeignKey(caracteristique, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    class Meta:
        ordering = ['id',]

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.caracteristique.valeur)


class CommandeNonLogin(models.Model):
    ETAT = (
    ("none","none"),
    ("payé","payé"),
    ("non payé",'non payé'),
    ("validé: préparation en cours","validé: préparation en cours"),
    ("préparé","préparé"),
    ("expedié","expedié"),
    ("en cours de livraison","en cours de livraison"),
    ("livré","livré")
    )
    """Classe qui définit les differentes categories du site: sauron securite"""
    #champs de formulaire
    SEXE = (
    ("H","homme"),
    ("F","femme"),
    ("O",'Autre'),
    )
    id = models.AutoField(primary_key=True)
    sexe = models.TextField(choices=SEXE,default="H")
    prenom = models.CharField(max_length=200,default="")
    nom = models.CharField(max_length=200,default="")
    email = models.EmailField()
    adresse = models.CharField(max_length=200,default="")
    code_postal = models.CharField(max_length=6,default="*****")
    ville = models.CharField(max_length=50,default="")
    pays = models.CharField(max_length=50,default="")
    telephone = models.CharField(max_length=15, blank=True)
    payer = models.BooleanField(default=False)
    date_livraison = models.TextField(default="pas encore livré",null=True,blank=True)
    date_payer = models.DateTimeField(auto_now_add=True)
    etat = models.TextField(choices=ETAT)
    total = models.FloatField(null=True,default=0)
    livraison = models.ForeignKey("PrixLivraison",on_delete=models.SET_NULL, null=True)
    numerosuivie= models.CharField(null=True, max_length=100,default="inconnu")
    promo = models.BooleanField(default=False)
    codepromo = models.ForeignKey("Promo",on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        ordering = ['date_payer',]

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.id)

class ProduitCommandeNonLogin(models.Model):
    id = models.AutoField(primary_key=True)
    commande = models.ForeignKey(CommandeNonLogin, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField(null=False,default=0)
    total = models.FloatField(null=True,default=0)
    class Meta:
        ordering = ['total',]

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.produit.nom)

class AvisProduit(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    valide = models.BooleanField(default=True)

    class Meta:
        ordering = ['id',]

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.produit.nom)
    
@receiver(post_save, sender=Commande)
def set_avis(sender, instance, created, **kwargs):
    if Commande.etat=="livré":
        profile = Commande.profile
        user = profile.user
        produits = ProduitPanierHistory.objects.filter(commande=Commande)
        for p in produits:
            AvisProduit.objects.create(user=user,produit=p)