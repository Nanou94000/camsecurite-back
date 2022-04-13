from django.contrib.auth.models import User, Group
from rest_framework import serializers
from camsecurite.models import ProduitCommandeNonLogin
from camsecurite.models import CommandeNonLogin
from camsecurite.models import Promo
from camsecurite.models import AvisProduit
from camsecurite.models import ProduitPanierHistory
from camsecurite.models import Avis
from camsecurite.models import Commande, Message
from camsecurite.models import ProduitCaracteristique
from camsecurite.models import caracteristique
from camsecurite.models import PrixLivraison
from camsecurite.models import Livreur
from camsecurite.models import Panier, ProduitPanier
from camsecurite.models import Profile
from camsecurite.models import Produit

from camsecurite.models import Categorie


class CaracteristiqueSerializer(serializers.ModelSerializer):

    class Meta:
        model = caracteristique
        fields = '__all__'

class LivreurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livreur
        fields = '__all__'

class PrixLivraisonSerializer(serializers.ModelSerializer):
    type = LivreurSerializer()
    class Meta:
        model = PrixLivraison
        fields = ['id','min_poids', 'max_poids','description','prix','type']

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ["id",'nom', 'sousNom','description','image','imageBanniere']


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ["id",'nom', 'sousNom','description','image','imageBanniere']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ProduitsSerializer(serializers.ModelSerializer):
    categorie = CategorieSerializer()
    caracteristiques = CaracteristiqueSerializer(read_only=True, many=True)
    class Meta:
        model = Produit
        fields = ['id','nom', 'sousNom','descriptionCourte','descriptionLongue','categorie','prix','prixSansReduction','image1','image2','image3','image4','image5','image6','resolution','poids','note','stock','date_ajout','caracteristiques','cartesd']


class ProduitsbyCategorieSerializer(serializers.ModelSerializer):
    caracteristiques = CaracteristiqueSerializer(read_only=True, many=True)
    class Meta:
        model = Produit
        fields = ['id','nom', 'sousNom','descriptionCourte','descriptionLongue','categorie','prix','prixSansReduction','image1','image2','image3','image4','image5','image6','resolution','poids','note','stock','date_ajout','caracteristiques','cartesd']

class USerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class PromoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Promo
        fields = '__all__'

class PanierSerializer(serializers.ModelSerializer):
    livraison = PrixLivraisonSerializer()
    codepromo = PromoSerializer()
    class Meta:
        model = Panier
        fields = ['id','livraison', 'total','totaltotal','totalaveclivraison','promo','codepromo','freeshipping']


class UserSerializer(serializers.ModelSerializer):

    user = USerializer()
    class Meta:
        model = Profile
        fields = ["id","sexe","adresse","code_postal","ville","pays","telephone","user",'notification','notif_commande','notif_msg','notif_avis']

class UserPanierItems(serializers.ModelSerializer):
    produit = ProduitsSerializer()
    panier = PanierSerializer()
    class Meta:
        model = ProduitPanier
        fields = ['id','produit', 'quantite','date_ajout','total','panier']
        
class UserPanierItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProduitPanier
        fields = ['id','produit', 'quantite','date_ajout','total','panier']




class ProduitCaracteristiqueSerializer(serializers.ModelSerializer):
    caracteristique = CaracteristiqueSerializer()
    produit = ProduitsSerializer()
    class Meta:
        model = ProduitCaracteristique
        fields = ['id','caracteristique', 'produit']


class MessageSerializer(serializers.ModelSerializer):
    profile = UserSerializer()
    class Meta:
        model = Message
        fields = ['id','profile', 'titre','contenu','expediteur','date','lu']


class CommandeSerializer(serializers.ModelSerializer):
    profile = UserSerializer()
    panier = PanierSerializer()
    livraison = PrixLivraisonSerializer()
    class Meta:
        model = Commande
        fields = '__all__'
    

class CommandenonlogSerializer(serializers.ModelSerializer):
    livraison = PrixLivraisonSerializer()
    class Meta:
        model = CommandeNonLogin
        fields = '__all__'
    

class AvisSerializer(serializers.ModelSerializer):
    profile = UserSerializer()
    produit = ProduitsSerializer()
    class Meta:
        model = Avis
        fields = '__all__'
        
class CommandeItems(serializers.ModelSerializer):
    produit = ProduitsSerializer()
    commande = CommandeSerializer()
    class Meta:
        model = ProduitPanierHistory
        fields = ['id','produit', 'quantite','date_ajout','total','commande']


class CommandenologinItems(serializers.ModelSerializer):
    produit = ProduitsSerializer()
    commande = CommandenonlogSerializer()
    class Meta:
        model = ProduitCommandeNonLogin
        fields = ['id','produit', 'quantite','total','commande']

        
class DonnerAvisSerializer(serializers.ModelSerializer):
    produit = ProduitsSerializer()
    user = USerializer()
    class Meta:
        model = AvisProduit
        fields = ['id','produit','valide','user']