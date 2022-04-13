from django.contrib import admin
from camsecurite.views import Logout
from camsecurite.views import CustomAuthToken
from camsecurite import views
from django.urls import include, path
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
router = routers.DefaultRouter()
router.register(r'categories', views.CategoriesViewSet)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from camsecurite import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('test-payment/', views.test_payment),
    path('create_checkout_session/', views.create_checkout_session),
    path('commande-success/', views.commande_valide),
    path('', include(router.urls)),
    path('current_user/', views.current_user),
    path('admin/', admin.site.urls),
    path('produits/', views.produit_list),
    path('google-auth/', views.GoogleAuth.as_view()),
    path('newsletter/', views.newsletter),
    path('compte/<int:id>/messages', views.messages),
    path('compte/<int:id>/commandes', views.commandes),
    path('compte/<int:id>/avis', views.avis),
    path('post-avis', views.avis),
    path('compte/<int:id>/donner-avis', views.donner_avis),
    path('produits/<str:s>/', views.produit_search),
    path('categorie/<int:id>/produits', views.produit_list_by_categorie),
    path('maj-categorie/<int:id>/', views.maj_categorie),
    path('maj-produit/<int:id>/', views.maj_produit),
    path('panier/<int:id>/', views.panierItems_list_by_user),
    path('expedier-commande/<int:id>/', views.expedie_commande),
    path('livrer-commande/<int:id>/', views.livrer_commande),
    path('commande/<int:id>/', views.commandeItems_list_by_user),
    path('commandenonlogin/<int:id>/', views.commandeItems_non_login),
    path('commandes/', views.toutes_commandes),
    path('commandesnonlogin/', views.toutes_commandes_non_log),
    path('commande/<int:id>/change-statut', views.change_statut_commande),
    path('panierid/<int:id>/', views.panierItems_id_by_user),
    path('caracteristiques/<int:id>/', views.caracteristiques_list_by_produit),
    path('caracteristiques/', views.toutes_caracteristiques),
    path('choix-livraison/<int:id>/', views.choix_livraison),
    path('choix-livraison-nolog/', views.choix_livraison_nolog),
    path('choix-livraison-nolog/<int:id>/', views.choix_livraison_nolog),
    path('ajouter_produit/', views.item_in_panier),
    path('produits/', views.top_produits),
    path('contact/', views.contact),
    path('promo/', views.promo),
    path('supprimer_produit/', views.item_in_panier),
    path('produit/<int:id>', views.Produit_detail),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('users/', views.users_list),
    path('signup/', views.sign_up),
    path('activate/<str:id>/', views.activate_account),
    path('ask-reset-mdp/', views.ask_reset_mdp),
    path('reset-mdp/<str:id>/', views.reset_mdp),
    path('users/<int:id>/', views.user_detail),
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('api-token-auth/logout', Logout.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('csrf/', views.csrf),
    path('ping/', views.ping),
    path('summernote/',include('django_summernote.urls')),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)