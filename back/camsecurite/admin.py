from django.contrib import admin
from camsecurite.models import CommandeNonLogin
from camsecurite.models import Promo
from camsecurite.models import ProduitPanierHistory
from camsecurite.models import AvisProduit
from camsecurite.models import Categorie, Produit, Profile, Panier, ProduitPanier, Livreur, PrixLivraison, caracteristique, ProduitCaracteristique, Newsletter, Commande, Message
from django_summernote.admin import SummernoteModelAdmin



# Register your models here.

class CategorieAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom')

admin.site.register(Categorie,CategorieAdmin)

class ProduitAdmin(SummernoteModelAdmin):
    js = (
        '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js', # jquery
        'js/myscript.js',       # project static folder
        'app/js/myscript.js',   # app static folder
    )
    summernote_fields = ['descriptionLongue']
    filter_horizontal = ('caracteristiques',)


admin.site.register(Produit,ProduitAdmin)

class ProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(Profile,ProfileAdmin)


class PromoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Promo,PromoAdmin)

class PanierAdmin(admin.ModelAdmin):
    pass

admin.site.register(Panier,PanierAdmin)


class ProduitpanierAdmin(SummernoteModelAdmin):
    pass
admin.site.register(ProduitPanier,ProduitpanierAdmin)


class ProduitpanierhistoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(ProduitPanierHistory,ProduitpanierhistoryAdmin)


class LivreurAdmin(admin.ModelAdmin):
    pass

admin.site.register(Livreur,LivreurAdmin)

class PrixLivraisonAdmin(admin.ModelAdmin):
    pass

admin.site.register(PrixLivraison,PrixLivraisonAdmin)


class caracteristiqueAdmin(admin.ModelAdmin):
    pass

admin.site.register(caracteristique,caracteristiqueAdmin)


class AvisProduitAdmin(admin.ModelAdmin):
    pass

admin.site.register(AvisProduit,AvisProduitAdmin)


class ProduitCaracteristiqueAdmin(admin.ModelAdmin):
    list_display = ('produit', 'caracteristique')

admin.site.register(ProduitCaracteristique,ProduitCaracteristiqueAdmin)


class NewsletterAdmin(admin.ModelAdmin):
    pass

admin.site.register(Newsletter,NewsletterAdmin)

class CommandeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Commande,CommandeAdmin)


class MessageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Message,MessageAdmin)

class CommandeNonLoginAdmin(admin.ModelAdmin):
    pass

admin.site.register(CommandeNonLogin,CommandeNonLoginAdmin)
