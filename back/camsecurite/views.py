from asyncio.windows_events import NULL
import email
from uuid import uuid4
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template import loader
from django.template import Context
from django.template.loader import get_template
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.urls import resolve
from sqlite3 import Date
from urllib import request
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework import permissions
from camsecurite.models import caracteristique
from camsecurite.serializers import CaracteristiqueSerializer
from camsecurite.serializers import CommandenologinItems
from camsecurite.serializers import CommandenonlogSerializer
from camsecurite.serializers import DonnerAvisSerializer
from camsecurite.models import AvisProduit
from camsecurite.serializers import CommandeItems
from camsecurite.serializers import PanierSerializer
from camsecurite.models import Promo
from camsecurite.models import CommandeNonLogin, ProduitCommandeNonLogin
from camsecurite.models import ProduitPanierHistory
from camsecurite.models import Avis
from camsecurite.serializers import AvisSerializer
from camsecurite.models import Commande
from camsecurite.serializers import CommandeSerializer
from camsecurite.serializers import MessageSerializer
from camsecurite.models import Message
from camsecurite.models import Newsletter
from camsecurite.models import ProduitCaracteristique
from camsecurite.serializers import ProduitCaracteristiqueSerializer
from camsecurite.serializers import PrixLivraisonSerializer
from camsecurite.models import Livreur, PrixLivraison
from camsecurite.models import Panier, ProduitPanier
from camsecurite.serializers import UserPanierItems
from camsecurite.serializers import UserSerializer
from camsecurite.serializers import ProduitsbyCategorieSerializer, UserPanierItemsSerializer
from camsecurite.models import Produit, Profile, Categorie
from camsecurite.serializers import ProduitsSerializer
from camsecurite.serializers import CategorieSerializer
from camsecurite.serializers import CategoriesSerializer
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
import stripe
import json
import os
stripe.api_key = 'sk_test_51JYyVMEwOswPrQzdx8k2n0DD5M8xSyhTOM1FatrJTdkh9hKtTcrtjOtCPiDyR0mV7lgyOMVPRE7hLbUenFvGS0Fw00AYGIAuLt'

def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})

def ping(request):
    return JsonResponse({'result': 'OK'})


@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """
    try:
        p = Profile.objects.get(user=request.user.id)
    except Profile.DoesNotExist:
        return Response('rien trouvé')
    serializer_context = {
        'request': request,
    }
    serializer = UserSerializer(p, context=serializer_context)
    return Response(serializer.data)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        u = User.objects.get(id=user.pk)
        profile = Profile.objects.get(user=u)
        if(profile.is_active==False):
            return Response('compte pas activé')
        us = authenticate(request, username=u.username, password=request.data['password'])
        l=login(request, us, backend=None)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': u.id,
            'email': u.email,
            'username':u.username,
            'firstname':u.first_name,
            'lastname':u.last_name,
        })
        

class GoogleAuth(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer_context = {
            'request': request,
        }
        try:
            user = User.objects.get(username=request.data['googleid'])
            authenticate(request, username=user.username, password=request.data['mdp'])
            l=login(request, user, backend=None)
            return Response({
                'user_id': user.id,
                'email': user.email,
                'username':user.username,
                'firstname':user.first_name,
                'lastname':user.last_name,
            })
            
        except:
            user = User.objects.create_user(username=request.data['googleid'],first_name=request.data['prenom'],last_name=request.data['nom'],email=request.data['email'],password=request.data['mdp'])
            profile = Profile.objects.get(user = user)
            profile.isActive=True
            profile.save()
            l=login(request, user, backend=None)
            return Response({
                'user_id': user.id,
                'email': user.email,
                'username':user.username,
                'firstname':user.first_name,
                'lastname':user.last_name,
            })


class Logout(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        l=logout(request)
        return Response('bye')

class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)

@api_view(['GET', 'POST'])
def produit_list(request, format=None):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'GET':
        serializer_context = {
            'request': request,
        }
        Produits = Produit.objects.all()
        serializer = ProduitsSerializer(Produits, context=serializer_context, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProduitsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def produit_list_by_categorie(request, format=None, *args, **kwargs):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'GET':
        serializer_context = {
            'request': request,
        }
        Produits = Produit.objects.filter(categorie_id=kwargs['id'])
        serializer = ProduitsbyCategorieSerializer(Produits, context=serializer_context, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def produit_search(request, format=None, *args, **kwargs):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'GET':
        serializer_context = {
            'request': request,
        }
        Produits = Produit.objects.filter(descriptionLongue__contains=kwargs['s'])
        serializer = ProduitsbyCategorieSerializer(Produits, context=serializer_context, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def Produit_detail(request, id, format=None):
    """
    Retrieve, update or delete a code Produit.
    """
    try:
        p = Produit.objects.get(id=id)
    except Produit.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer_context = {
        'request': request,
    }

    if request.method == 'GET':
        serializer = ProduitsSerializer(p, context=serializer_context)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProduitsSerializer(p, context=serializer_context, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        p.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def users_list(request, format=None):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'GET':
        serializer_context = {
            'request': request,
        }
        p = Profile.objects.all()
        serializer = UserSerializer(p, context=serializer_context, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        d = request.data
        u = User.objects.create(username=d.get('email'), email=d.get('email'), firstname=d.get("prenom"), lastname=d.get('nom'), password=d.get('mdp'))
        p = Profile.objects.get(user=u)
        p.adresse = d.get("adresse")
        p.pays = d.get("pays")
        p.telephone = d.get("telephone")
        p.pays = d.get("pays")
        p.code_postal = d.get("cp")
        p.ville = d.get("ville")
        p.save()
        #serializer = UserSerializer(data=d)
        #if serializer.is_valid():
        #    serializer.save()
        #    return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST', 'DELETE'])
def user_detail(request, id, format=None):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'GET':
        try:
            p = Profile.objects.get(id=id)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer_context = {
                'request': request,
            }    
        if request.method == 'GET':
            serializer = UserSerializer(p, context=serializer_context)
            return Response(serializer.data)

    if request.method == 'POST':
        serializer_context = {
            'request': request,
        }

        user = User.objects.get(id=id)
        prenom = request.data['prenom']
        user.first_name = prenom
        nom = request.data['nom']
        user.last_name = nom
        email = request.data['email']
        user.email = email
        user.save()
        adresse = request.data['adresse']
        ville = request.data['ville']
        cp = request.data['cp']
        pays = request.data['pays']
        cp = request.data['cp']
        telephone = request.data['telephone']
        profile = Profile.objects.get(user=user)
        profile.adresse = adresse
        profile.code_postal = cp
        profile.ville = ville
        profile.pays = pays
        profile.telephone = telephone
        profile.save()

        return Response("update done")


class CategoriesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Categorie.objects.all().order_by('nom')
    serializer_class = CategoriesSerializer
    permission_classes = [permissions.AllowAny]

class UserList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer
    
@api_view(['GET'])
def top_produits(request, format=None, *args, **kwargs):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'GET':
        serializer_context = {
            'request': request,
        }
        produits = Produit.objects.order_by('date_ajout')[:2]
        serializer = ProduitsSerializer(produits, context=serializer_context, many=True)
        return Response(serializer.data)

@api_view(['GET','POST'])
def panierItems_list_by_user(request, format=None, *args, **kwargs):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'GET':
        serializer_context = {
            'request': request,
        }
        user= User.objects.get(id=kwargs['id'])
        profile = Profile.objects.get(user=user)
        panier = Panier.objects.get(profile=profile)
        Produits = ProduitPanier.objects.filter(panier=panier)
        serializer = UserPanierItems(Produits, context=serializer_context, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer_context = {
            'request': request,
        }
        produits = Produit.objects.filter(id__in=request.data['id'])
        serializer = ProduitsSerializer(produits, context=serializer_context, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def commandeItems_list_by_user(request, format=None, *args, **kwargs):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'GET':
        serializer_context = {
            'request': request,
        }
        commande = Commande.objects.get(id=kwargs['id'])
        Produits = ProduitPanierHistory.objects.filter(commande=commande)
        serializer = CommandeItems(Produits, context=serializer_context, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def commandeItems_non_login(request, format=None, *args, **kwargs):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'GET':
        serializer_context = {
            'request': request,
        }
        commande = CommandeNonLogin.objects.get(id=kwargs['id'])
        Produits = ProduitCommandeNonLogin.objects.filter(commande=commande)
        serializer = CommandenologinItems(Produits, context=serializer_context, many=True)
        return Response(serializer.data)


@api_view(['GET','POST'])
def panierItems_id_by_user(request, format=None, *args, **kwargs):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'GET':
        serializer_context = {
            'request': request,
        }
        user= User.objects.get(id=kwargs['id'])
        profile = Profile.objects.get(user=user)
        panier = Panier.objects.get(profile=profile)
        serializer = PanierSerializer(panier, context=serializer_context, many=False)
        return Response(serializer.data)

@api_view(['POST','DELETE'])
def item_in_panier(request, format=None):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'POST':
        serializer_context = {
            'request': request,
        }
        produit = Produit.objects.get(id=request.data['idproduit'])
        profile = Profile.objects.get(user=request.data['iduser'])
        panier = Panier.objects.get(profile=profile)
        try:
            pr = ProduitPanier.objects.get(produit=produit,panier=panier)
            panier.total = panier.total - pr.quantite*pr.produit.prix
            panier.poids = panier.poids - pr.quantite*pr.produit.poids
            pr.delete()
        except:
            print("pas ce produit dans le panier")
        qte=request.data['quantite']
        total = produit.prix * int(qte)
        panier.total = panier.total + total
        panier.poids = panier.poids + produit.poids * int(qte)
        panier.promo=False
        panier.save()
        Produits = ProduitPanier.objects.create(produit=produit, panier=panier, quantite=qte, total=total, )
        serializer = UserPanierItemsSerializer(Produits, context=serializer_context, many=False)
        return Response(serializer.data)
        
    if request.method == 'DELETE':
        serializer_context = {
            'request': request,
        }
        produit = Produit.objects.get(id=request.data['idproduit'])
        user = User.objects.get(id=request.data['iduser'])
        profile = Profile.objects.get(user=user)
        panier = Panier.objects.get(profile=profile)
        Produits = ProduitPanier.objects.get(produit=produit, panier=panier)
        panier.total = panier.total - Produits.total
        panier.poids = panier.poids - produit.poids * int(Produits.quantite)
        panier.save()
        Produits.delete()
        return Response('delete')

@api_view(['POST','DELETE'])
def update_user(request, format=None):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'POST':
        serializer_context = {
            'request': request,
        }

        prenom = request.data['prenom']
        nom = request.data['nom']
        email = request.data['email']
        adresse = request.data['adresse']
        ville = request.data['ville']
        cp = request.data['cp']
        pays = request.data['pays']
        cp = request.data['cp']
        telephone = request.data['telephone']
        user = User.objects.get(id=request.data['iduser']).update(first_name=prenom,last_name=nom,email=email)
        profile = Profile.objects.get(user=request.data['iduser']).update(adresse=adresse,ville=ville,code_postal=cp,pays=pays)

        return Response("update done")

@api_view(['POST','GET'])
def choix_livraison(request, format=None, *args, **kwargs):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'POST':
        serializer_context = {
            'request': request,
        }
        livreur = PrixLivraison.objects.get(id=request.data['livraison'])
        profile = Profile.objects.get(user=kwargs['id'])
        panier = Panier.objects.get(profile=profile)
        if(panier.freeshipping and livreur.type.id==1):
            panier.totalaveclivraison = panier.total
        else:
            panier.totalaveclivraison = panier.total + livreur.prix
        panier.livraison = livreur
        panier.save()
        return Response("update done")
    if request.method == 'GET':
        serializer_context = {
            'request': request,
        }
        profile = Profile.objects.get(user=kwargs['id'])
        panier = Panier.objects.get(profile=profile)
        if(panier.total > 100):
            panier.freeshipping = True
            panier.save()
        Livraison = PrixLivraison.objects.filter(min_poids__lte=panier.poids, max_poids__gte=panier.poids)
        serializer = PrixLivraisonSerializer(Livraison, context=serializer_context, many=True)
        return Response(serializer.data)

@api_view(['POST','GET'])
def choix_livraison_nolog(request, format=None, *args, **kwargs):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'GET':
        serializer_context = {
            'request': request,
        }
        Livraison = PrixLivraison.objects.get(id=kwargs['id'])
        serializer = PrixLivraisonSerializer(Livraison, context=serializer_context, many=False)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer_context = {
            'request': request,
        }
        produits = Produit.objects.filter(id__in=request.data['id'])
        poids = 0
        for p in produits:
            poids = poids + p.poids
        Livraison = PrixLivraison.objects.filter(min_poids__lte=poids, max_poids__gte=poids)
        serializer = PrixLivraisonSerializer(Livraison, context=serializer_context, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def caracteristiques_list_by_produit(request, format=None, *args, **kwargs):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'GET':
        serializer_context = {
            'request': request,
        }
        produit = Produit.objects.get(id=kwargs['id'])
        carac = ProduitCaracteristique.objects.filter(produit=produit)
        serializer = ProduitCaracteristiqueSerializer(carac, context=serializer_context, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def toutes_caracteristiques(request, format=None, *args, **kwargs):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'GET':
        serializer_context = {
            'request': request,
        }
        carac = caracteristique.objects.all()
        serializer = CaracteristiqueSerializer(carac, context=serializer_context, many=True)
        return Response(serializer.data)


@api_view(['POST','GET'])
def newsletter(request, format=None, *args, **kwargs):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'POST':
        serializer_context = {
            'request': request,
        }
        try:
            n = Newsletter.objects.get(email=request.data['nl_email'])
        except:
            Newsletter.objects.create(email=request.data['nl_email'])
            return Response("félicitation")
        return Response("deja abonné")


@api_view(['POST','GET'])
def sign_up(request, format=None, *args, **kwargs):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'POST':
        serializer_context = {
            'request': request,
        }
        try:
            user = User.objects.create_user(
                first_name=request.data['prenom'],
                last_name=request.data['nom'],
                password=request.data['mdp'],
                email=request.data['email'],
                username=request.data['email'],
            )
        except:
            return Response("impossible de creer un utilisateur")
        
        profile = Profile.objects.get(user=user)
        profile.sexe = request.data['sexe']
        profile.adresse = request.data['adresse']
        profile.ville = request.data['ville']
        profile.code_postal = request.data['cp']
        profile.pays = request.data['pays']
        profile.telephone = request.data['telephone']
        profile.is_active = False
        profile.save()  
        key = Token.objects.get(user=user).key
            
        subject = f'{user.first_name}, activer votre compte Cam Securite'
        html_message = loader.render_to_string('signup.html', {'key':key})
        send_mail(subject,strip_tags(html_message),settings.DEFAULT_FROM_EMAIL,[user.email],fail_silently=False,html_message=html_message,)
        return Response("felicitation")


@api_view(['GET'])
def messages(request, format=None, *args, **kwargs):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'GET':
        serializer_context = {
            'request': request,
        }
        user = User.objects.get(id=kwargs['id'])
        profile = Profile.objects.get(user=user)
        profile.notif_msg = False
        if profile.notif_msg==False & profile.notif_commande==False & profile.notif_avis==False:
            profile.notification=False
        profile.save()
        msg = Message.objects.filter(profile=profile)
        serializer = MessageSerializer(msg, context=serializer_context, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def commandes(request, format=None, *args, **kwargs):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'GET':
        serializer_context = {
            'request': request,
        }
        user = User.objects.get(id=kwargs['id'])
        profile = Profile.objects.get(user=user)
        profile.notif_commande = False
        if profile.notif_msg==False & profile.notif_commande==False & profile.notif_avis==False:
            profile.notification=False
        profile.save()
        commande = Commande.objects.filter(profile=profile).order_by('-date_payer')
        serializer = CommandeSerializer(commande, context=serializer_context, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def toutes_commandes(request, format=None, *args, **kwargs):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'GET':
        serializer_context = {
            'request': request,
        }
        commande = Commande.objects.all().order_by("-date_payer")
        serializer = CommandeSerializer(commande, context=serializer_context, many=True)
        return Response(serializer.data)
        
@api_view(['GET'])
def toutes_commandes_non_log(request, format=None, *args, **kwargs):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'GET':
        serializer_context = {
            'request': request,
        }
        commande = CommandeNonLogin.objects.all().order_by("-date_payer")
        serializer = CommandenonlogSerializer(commande, context=serializer_context, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def change_statut_commande(request, format=None, *args, **kwargs):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'POST':
        serializer_context = {
            'request': request,
        }
        commande = Commande.objects.get(id=kwargs['id'])
        commande.statut = request.data['statut']
        if(request.data['statut']=='expedié'):
            commande.numerosuivie= request.data['numerosuivie']
        commande.save()
        serializer = CommandeSerializer(commande, context=serializer_context, many=True)
        return Response(serializer.data)

@api_view(['GET','POST'])
def avis(request, format=None, *args, **kwargs):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'POST':
        serializer_context = {
            'request': request,
        }
        try:
            user = User.objects.get(id=request.data['user'])
            profile = Profile.objects.get(user=user)
            produit = Produit.objects.get(id=request.data['produit'])
            avis = Avis.objects.create(profile=profile,titre=request.data["titre"],contenu=request.data["contenu"],note=request.data['note'],produit=produit)
            avisproduit = AvisProduit.objects.get(user=user,produit=produit)
            avisproduit.delete()
            serializer = AvisSerializer(avisproduit, context=serializer_context, many=True)
            return Response(serializer.data)
        except:
            return Response("KO")
    if request.method == 'GET':
        serializer_context = {
            'request': request,
        }
        user = User.objects.get(id=kwargs['id'])
        profile = Profile.objects.get(user=user)
        avis = Avis.objects.filter(profile=profile)
        serializer = AvisSerializer(avis, context=serializer_context, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def donner_avis(request, format=None, *args, **kwargs):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'GET':
        serializer_context = {
            'request': request,
        }
        user = User.objects.get(id=kwargs['id'])
        avis = AvisProduit.objects.filter(user=user,valide=True)
        serializer = DonnerAvisSerializer(avis, context=serializer_context, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def test_payment(request):
    test_payment_intent = stripe.PaymentIntent.create(
        amount=1000, currency='eur', 
        payment_method_types=['card'],
        receipt_email='test@example.com')
    return Response(status=status.HTTP_200_OK, data=test_payment_intent)


def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return 1400


def charge_customer(customer_id):
    # Lookup the payment methods available for the customer
    payment_methods = stripe.PaymentMethod.list(
        customer=customer_id,
        type='card'
    )
    # Charge the customer and payment method immediately
    try:
        stripe.PaymentIntent.create(
            amount=1099,
            currency='eur',
            customer=customer_id,
            payment_method=payment_methods.data[0].id,
            off_session=True,
            confirm=True
        )
    except stripe.error.CardError as e:
        err = e.error
        # Error code will be authentication_required if authentication is needed
        print('Code is: %s' % err.code)
        payment_intent_id = err.payment_intent['id']
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

YOUR_DOMAIN = "localhost:3000"
@api_view(['POST'])
def create_checkout_session(request):
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'amount': "1",
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '?success=true',
            cancel_url=YOUR_DOMAIN + '?canceled=true',
        )
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK, data=checkout_session)


def makefacture(id,save):
    commande = Commande.objects.get(id=id)
    produit_list = ProduitPanierHistory.objects.filter(panier=commande.panier,commande=commande)
    gratuit = False
    totalpanier = ProduitPanierHistory.objects.filter(commande=commande).aggregate(Sum('total'))['total__sum']
    if totalpanier > 150 and commande.livraison.type.nom=='Colissimo':
        gratuit = True
    r = False
    red=0
    if commande.promo:
        r = True
        red = totalpanier*float(f'0.{commande.codepromo.reduction_pourcentage}')
    totalavecred = totalpanier - red
    ht = totalavecred / 1.2
    tva = ht*0.2
    template = get_template('facture_template.html')
    context = {
        "produit": produit_list,
        "commande": commande,
        "gratuit": gratuit,
        "r": r,
        "tva": tva,
        "ht": ht,
        "livraison": commande.livraison,
        "red":red,
        "totalpanier":totalpanier,
        "totalpanieravecred":totalavecred,
    }
    font_config = FontConfiguration()
    html_string = render_to_string('facture_template.html', context)
    html = HTML(string=html_string)
    css = CSS(string='''
@font-face{
        font-family:'Mohave';
        src:url('https://fonts.googleapis.com/css2?family=Mohave:wght@300&display=swap');
}
*{
        padding: 0;
        margin: 0;
        box-sizing:border-box;
        font-family: 'Mohave', sans-serif;
}
@page{
        margin: 1cm;
        .break{
    page-break-inside: avoid !important;

        }
  div {
    break-inside: avoid;
    page-break-inside: avoid !important;

  }

}

@media print {
  div {
    break-inside: avoid;
  }
}

body{
        background-color:white;
        padding: 0;
        display: flex;
        justify-content:center;
}
.main-fact{
        width:21cm;
        background-color:#fff;
        display: flex;
        flex-direction:column;
}
h1,h2,h3{
        margin:0cm;
        padding: 0;
        padding-bottom: 0.6cm;

}
p{
        margin: 0;
        padding: 0;
}
.head-fact{
        width:19cm;
        background-image: url('https://images.unsplash.com/photo-1565591452825-67d6b7df1d47?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1926&q=80');
        background-size:cover;
        background-repeat:no-repeat;
        background-position: 0cm -4cm;
        display: flex;
        flex-direction:column;
        align-items:center;
        justify-content:center;

}

.coordonnees-fact{
        width:18cm;
        display: flex;
        display: flex;
        align-items:center;
        padding-top:0.1cm;
        padding-bottom:0cm;
        padding-right: 0.5cm;
        padding-left: 0.5cm;

}
.exp,.dest{
        display: flex;
        flex-direction:column;
        width: 8.5cm;
}
.dest{
        padding-top: 1.5cm;
}
.textend{
        text-align:end;
}
.info-fact{
        padding-left: 0.5cm;
        padding-top: 0.8cm;
        padding-bottom: 0.8cm;
        width: 13cm;
}
.info-line-fact{
        padding-top: 10px;
        display: flex;
}
.info-line-fact span{
        width: 50%;
}
.detail-fact{
        padding-bottom: 0.2cm;
        padding-right: 0.5cm;
        padding-left: 0.5cm;
}
        width:17cm;
        margin-bottom:0.3cm;
        padding-bottom: 0cm;
}

tbody{
        padding-top: 0cm;
}

tr{
        width:17cm;
        margin-top: 0.3cm;
        margin-bottom: 0.3cm;
}
th{
        text-align:start;
        max-width: 200px;
        font-weight: 600;
}
td{
        padding-top: 10px;
        max-width: 3cm;
        padding-bottom: 21px;
}
.total-fact{
        background: #E32700;
        width:18.6cm;
        padding: 0.2cm;
        padding-bottom: 0.5cm;
        display: flex;
        justify-content:space-between;
}

.info-paiement{
        width:6.9cm;
}

.detail-total-fact{
        width:11.7cm;
}

.detail-total-fact > *{
        width:11.7cm;
        text-align:end;
        margin-bottom:0.2cm;
}


.white{
        color:white;
}
table, tr, td, th, tbody, thead, tfoot {
    page-break-inside: avoid !important;
}

    ''',font_config=font_config)
    if save==True:
        pdf = html.write_pdf(f'/home/nasser/sauron_securite_website/sauron_ecommerce/factures/FRSAURON000{id}.pdf',stylesheets=[css],font_config=font_config)
    else:
        pdf = html.write_pdf(stylesheets=[css],font_config=font_config)
    return pdf

def facture(request,id):
    commande = Commande.objects.get(id=id)
    if commande.profile != Profile.objects.get(user_id=request.user.id):
        return redirect('index')
    pdf = makefacture(id,False)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "facture_frsauron000%s.pdf" %(id)
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")



@api_view(['POST'])
def commande_valide(request):
    if (request.data['login']):
        user = User.objects.get(id=request.data['id'])
        profile = Profile.objects.get(user=user)
        profile.notification = True
        profile.notif_commande = True
        profile.notif_msg = True
        profile.save()
        panier = Panier.objects.get(profile=profile)
        promo = panier.codepromo
        gratuit = False
        if panier.total>100 and panier.livraison.type.nom == "Colissimo":
            gratuit = True
        commande = Commande(panier=panier,profile=profile,payer=True,etat="payé",total=panier.totalaveclivraison,livraison=panier.livraison)
        commande.save()
        produits = ProduitPanier.objects.filter(panier=panier)
        for p in produits:
            pt = ProduitPanier.objects.get(id=p.id)
            np = ProduitPanierHistory(panier=pt.panier,produit=pt.produit,quantite=pt.quantite,total=pt.total,commande=commande)
            np.save()
            pt.delete()
            AvisProduit.objects.create(user=user,produit=pt.produit)
        st = 0
        if panier.promo:
            st = panier.total/(1-float(f'0.{promo.reduction_pourcentage}'))
            red = st*float(f'0.{promo.reduction_pourcentage}')
            r = True
        else:
            st = panier.total
            red = False
            r = False

        produit_list = ProduitPanierHistory.objects.filter(panier=panier,commande=commande)
        ProduitPanier.objects.filter(panier=panier).delete()
        m = Message(titre=f"Félicitation votre commande n°FRSAURON000{commande.id} est en cours de préparation !",contenu=f"", profile=profile)
        m.save()
        Panier.objects.filter(id=panier.id).update(
        total=0,
        totalaveclivraison=0
        )
        Panier.objects.filter(id=panier.id).update(
            promo=False,
            codepromo="",
            poids=0,
            freeshipping=False
        )
        current_site = get_current_site(request)
        subject = f'Commande payée avec succés: CAMSEC000{commande.id}'
        html_message = loader.render_to_string('commande_email.html', {
            'user': user,'profile':profile,'panier':panier,'produit_list':produit_list,'livraison':commande.livraison, 'red':red,'promo':promo,'r':r,'gratuit':gratuit,'commande':commande,'st':st})
        send_mail(subject,strip_tags(html_message),settings.DEFAULT_FROM_EMAIL,[user.email],fail_silently=False,html_message=html_message,)

        msg = f'Voici la facture en pièce jointe liée à la commande: FRSAURON000{commande.id}'
        mail = EmailMessage('Facture',msg,settings.DEFAULT_FROM_EMAIL,[user.email])
        #mail.attach_file(f'/home/nasser/sauron_securite_website/sauron_ecommerce/factures/FRSAURON000{commande.id}.pdf')
        mail.send()


        subjectbis = f'Nouvelle commande: CAMSEC000{commande.id}'
        html_messagebis = loader.render_to_string('nouvelle_comande_email.html', {
            'user': user,'profile':profile,'panier':panier,'produit_list':produit_list,'livraison':commande.livraison, 'red':red,'promo':promo,'r':r,'gratuit':gratuit,'commande':commande,'st':st})
        send_mail(subjectbis,strip_tags(html_message),settings.DEFAULT_FROM_EMAIL,['contact@sauron-securite.com','alex_94310@hotmail.fr','nourou.nasser@gmail.com'],fail_silently=False,html_message=html_messagebis,)

        return Response(status=status.HTTP_200_OK, data=f'FRSAURON000{commande.id}')
    else:
        print('livraison')
        print(request.data)
        livreur = PrixLivraison.objects.get(id=request.data['livraison'])
        produits = Produit.objects.filter(id__in=request.data['produits'])
        total = 0
        commande = CommandeNonLogin.objects.create(
            sexe = 'O',
            prenom = request.data['prenom'],
            nom = request.data['nom'],
            email = request.data['email'],
            adresse = request.data['adresse'],
            code_postal = request.data['cp'],
            ville = request.data['ville'],
            pays = request.data['pays'],
            telephone = request.data['telephone'],
            payer = True,
            etat = 'payé',
            total = 0,
            livraison = livreur,
        )
        for p in produits:
            total = total + p.prix
            ProduitCommandeNonLogin.objects.create(
                commande = commande,
                produit = p,
                quantite = 1,
                total = p.prix
            )
        commande.total = total + livreur.prix
        commande.save()
        produit_list = ProduitCommandeNonLogin.objects.filter(commande=commande)
        soustotal = total
        subject = f'Commande payée avec succés: FRSAURON000{commande.id}'
        html_message = loader.render_to_string('commande_email_nolog.html', {
            'commande': commande,'produit_list':produit_list,'livraison':livreur, 'soustotal': soustotal})
        send_mail(subject,strip_tags(html_message),settings.DEFAULT_FROM_EMAIL,[commande.email],fail_silently=False,html_message=html_message,)

        msg = f'Voici la facture en pièce jointe liée à la commande: FRSAURON000{commande.id}'
        mail = EmailMessage('Facture',msg,settings.DEFAULT_FROM_EMAIL,[commande.email])
        #mail.attach_file(f'/home/nasser/sauron_securite_website/sauron_ecommerce/factures/FRSAURON000{commande.id}.pdf')
        mail.send()


        subjectbis = f'Nouvelle commande: FRSAURON000{commande.id}'
        html_messagebis = loader.render_to_string('nouvelle_comande_email.html', {
            'user': user,'profile':profile,'panier':panier,'produit_list':produit_list,'livraison':commande.livraison, 'red':red,'promo':promo,'r':r,'gratuit':gratuit,'commande':commande})
        send_mail(subjectbis,strip_tags(html_message),settings.DEFAULT_FROM_EMAIL,['contact@sauron-securite.com','alex_94310@hotmail.fr','nourou.nasser@gmail.com'],fail_silently=False,html_message=html_messagebis,)

        return Response(status=status.HTTP_200_OK, data=f'FRSAURON000{commande.id}')
@api_view(['GET'])
def activate_account(request, format=None, *args, **kwargs):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'GET':
        serializer_context = {
            'request': request,
        }
        try:
            token = Token.objects.get(key=kwargs['id'])
            user = token.user
            profile = Profile.objects.get(user=user)
            profile.is_active = True
            profile.save()
            return Response('OK')
        except:
            return Response('KO')

@api_view(['POST'])
def contact(request, format=None, *args, **kwargs):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'POST':
        serializer_context = {
            'request': request,
        }
        subject = request.data['objet']
        message = request.data['message']
        email = request.data['email']
        try:
            mail = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL,email])
            mail.content_subtype = "html"
            try:
                attach = request.FILES.get('file')
                mail.attach(attach.name, attach.read(), attach.content_type)
            except:
                pass
            mail.send(fail_silently=False)
            return Response("message envoyé")
        except:
            return Response('message non envoyé')


@api_view(['POST','DELETE'])
def promo(request, format=None, *args, **kwargs):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'POST':
        serializer_context = {
            'request': request,
        }
        user = User.objects.get(id=request.data['id'])
        profile = Profile.objects.get(user=user)
        panier = Panier.objects.get(profile=profile)
        try:
            p = Promo.objects.get(nom=request.data['promo'])
            if(not p.valide):
                return Response('ko')
            panier.promo=True
            panier.codepromo=p
            total = panier.total-panier.total*p.reduction_pourcentage/100
            panier.total=total
            livreur = panier.livraison
            if(panier.freeshipping and livreur.type.id==1):
                panier.totalaveclivraison=total
            else:
                panier.totalaveclivraison=total + livreur.prix
            panier.save()
            return Response(panier.total)
        except:
            return Response('ko')
    if request.method == 'DELETE':
        serializer_context = {
            'request': request,
        }
        user = User.objects.get(id=request.data['id'])
        profile = Profile.objects.get(user=user)
        panier = Panier.objects.get(profile=profile)
        livreur = panier.livraison
        try:
            panier.promo=False
            produits = ProduitPanier.objects.filter(panier=panier)
            total = 0
            for p in produits: 
                total = total + p.produit.prix*p.quantite
            panier.total=total
            if(panier.freeshipping and livreur.type.id==1):
                panier.total=total
                panier.totalaveclivraison=total
            else:
                panier.total=total
                panier.totalaveclivraison=total + livreur.prix
            panier.save()
            return Response(panier.total)
        except:
            return Response('ko')


@api_view(['POST'])
def ask_reset_mdp(request, format=None, *args, **kwargs):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'POST':
        serializer_context = {
            'request': request,
        }
        try:
            user = User.objects.get(username=request.data['email'])
            profile = Profile.objects.get(user=user)
            profile.reset_mdp = True
            profile.save()
            key = Token.objects.get(user=user).key
            subject = f'{user.first_name}, Réinitialisation mot de passe Cam Securite'
            html_message = loader.render_to_string('resset_mdp.html', {'key':key})
            send_mail(subject,strip_tags(html_message),settings.DEFAULT_FROM_EMAIL,[user.email],fail_silently=False,html_message=html_message,)
            return Response("ok")
        except:
            return Response('ko')


@api_view(['POST'])
def reset_mdp(request, format=None, *args, **kwargs):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'POST':
        serializer_context = {
            'request': request,
        }
        try:
            token = Token.objects.get(key=request.data['key'])
            user = token.user
            profile = Profile.objects.get(user=user)
            if(profile.reset_mdp == False):
                return Response('ko')
            user.set_password = request.data['mdp']
            user.save()
            profile.reset_mdp = False
            profile.save()
            return Response("ok")
        except:
            return Response('ko')
        
@api_view(['POST'])
def expedie_commande(request, format=None, *args, **kwargs):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'POST':
        serializer_context = {
            'request': request,
        }
        if(request.data['commande']=="log"):
            try:
                commande = Commande.objects.get(id=request.data['id'])
                commande.etat = 'expedié'
                commande.numerosuivie = request.data['numerosuivie']
                commande.save()
                return Response("ok")
            except:
                return Response('ko')
        else:
            try:
                commande = CommandeNonLogin.objects.get(id=request.data['id'])
                commande.etat = 'expedié'
                commande.numerosuivie = request.data['numerosuivie']
                commande.save() 
                return Response("ok")
            except:
                return Response('ko')
            
@api_view(['POST'])
def livrer_commande(request, format=None, *args, **kwargs):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'POST':
        serializer_context = {
            'request': request,
        }
        if(request.data['commande']=="log"):
            try:
                commande = Commande.objects.get(id=request.data['id'])
                commande.etat = 'livré'
                commande.date_livraison = request.data["datelivraison"]
                commande.save()
                return Response("ok")
            except:
                return Response('ko')
        else:
            try:
                commande = CommandeNonLogin.objects.get(id=request.data['id'])
                commande.etat = 'livré'
                commande.date_livraison = request.data["datelivraison"]
                commande.save()
                return Response("ok")
            except:
                return Response('ko')



@api_view(['POST'])
def maj_categorie(request, format=None, *args, **kwargs):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'POST':
        serializer_context = {
            'request': request,
        }
        print(request)
        try:
            categorie = Categorie.objects.get(id=request.data["id"])
            categorie.nom = request.data["nom"]
            categorie.sousNom = request.data["sousNom"]
            categorie.description = request.data["description"]
            categorie.imageBanniere = request.data["imgB"]
            categorie.save()
            return Response("ok")
        except:
            return Response('ko')


@api_view(['POST'])
def maj_produit(request, format=None, *args, **kwargs):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'POST':
        serializer_context = {
            'request': request,
        }
        print(request)
        if request.data["id"]=='0':
            try:
                categorie = Categorie.objects.get(id=request.data["categorie"])
            except Exception as e:
                print(e)
            produit = Produit.objects.create(
                nom=request.data["nom"],
                sousNom=request.data["sousNom"],
                descriptionCourte=request.data["descriptionCourte"],
                descriptionLongue=request.data["descriptionLongue"],
                prix=request.data["prix"],
                prixSansReduction=request.data["prixSansReduction"],
                poids=request.data["poids"],
                stock=request.data["stock"],
                image1=request.data["image1"],
                )
            try:                
                produit.image2 = request.data["image2"]           
            except Exception as e:
                print(e)
            try:                
                produit.image3 = request.data["image3"]           
            except Exception as e:
                print(e)
            try:                
                produit.image4 = request.data["image4"]           
            except Exception as e:
                print(e)
            try:                
                produit.image5 = request.data["image5"]           
            except Exception as e:
                print(e)
            return Response("ok")
        else:
            try:
                produit = Produit.objects.get(id=request.data["id"])
                print(request.data)
                try:
                    categorie = Categorie.objects.get(id=request.data["categorie"])
                    produit.categorie=categorie
                except Exception as e:
                    print(e)
                
                try:
                    produit.nom = request.data["nom"]            
                except Exception as e:
                    print(e)
                try:                
                    produit.sousNom = request.data["sousNom"]           
                except Exception as e:
                    print(e)
                try:                
                    produit.descriptionCourte = request.data["descriptionCourte"]           
                except Exception as e:
                    print(e)
                try:                
                    produit.descriptionLongue = request.data["descriptionLongue"]           
                except Exception as e:
                    print(e)
                try:                
                    produit.prix = request.data["prix"]           
                except Exception as e:
                    print(e)
                try:                
                    produit.prixSansReduction = request.data["prixSansReduction"]           
                except Exception as e:
                    print(e)
                try:                
                    produit.image1 = request.data["image1"]           
                except Exception as e:
                    print(e)
                try:                
                    produit.image2 = request.data["image2"]           
                except Exception as e:
                    print(e)
                try:                
                    produit.image3 = request.data["image3"]           
                except Exception as e:
                    print(e)
                try:                
                    produit.image4 = request.data["image4"]           
                except Exception as e:
                    print(e)
                try:                
                    produit.image5 = request.data["image5"]           
                except Exception as e:
                    print(e)
                try:                
                    produit.poids = request.data["poids"]           
                except Exception as e:
                    print(e)
                try:                
                    produit.stock = request.data["stock"]           
                except Exception as e:
                    print(e)


                produit.save()
                return Response("ok")
            except Exception as e:
                print(e)
                return Response('ko')


@api_view(['POST'])
def create_produit(request, format=None, *args, **kwargs):
    """
    List all code Produits, or create a new Produit.
    """
    if request.method == 'POST':
        serializer_context = {
            'request': request,
        }
        print(request)
        try:
            produit = Produit.objects.create(
            nom = request.data["nom"],
            sousNom = request.data["sousNom"],
            descriptionCourte = request.data["descriptionCourte"],
            descriptionLongue = request.data["descriptionLongue"],
            prix = request.data["prix"],
            prixSansReduction = request.data["prixSansReduction"],
            image1 = request.data["image1"],
            image2 = request.data["image2"],
            image3 = request.data["image3"],
            image4 = request.data["image4"],
            image5 = request.data["image5"],
            poids = request.data["poids"],
            cartesd = request.data["cartesd"],
            stock = request.data["stock"],
            )
            return Response("ok")
        except:
            return Response('ko')

