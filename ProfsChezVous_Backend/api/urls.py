from django.urls import path, re_path
from . import views
from .views import *
from rest_framework.routers import DefaultRouter

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('matieres/', views.MatiereList.as_view(), name='matiere-list'),
    path('matieres/<int:pk>/', views.MatiereDetail.as_view(), name='matiere-detail'),
    path('commentaires/', views.CommentaireCoursList.as_view(), name='commentaire-list'),
    path('commentaires/<int:pk>/', views.CommentaireCoursDetail.as_view(), name='commentaire-detail'),
    path('cours-unite/', CoursUniteViewSet.as_view({'get': 'list', 'post': 'create'}), name='cours-unite-list'),
    path('cours-unite/<int:pk>/', CoursUniteViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='cours-unite-detail'),
    path('cours-package/', CoursPackageViewSet.as_view({'get': 'list', 'post': 'create'}), name='cours-package-list'),
    path('cours-reserves/', VueCoursReservesUtilisateur.as_view(), name='cours-reserves-utilisateur'),
    path('professeur/cours-package-non-confirmes/', CoursPackageNonConfirmesView.as_view(), name='cours-package-non-confirmes'),
    path('professeur/confirmer-cours-package/<int:pk>/', ConfirmerCoursPackageView.as_view(), name='confirmer-cours-package'),
    path('professeur/<int:professeur_id>/matieres/', MatieresProfesseurView.as_view(), name='matieres-professeur'),
    #path('discussion-parent-admin/', DiscussionParentAdminViewSet.as_view({'get': 'list', 'post': 'create'}), name='discussion-parent-admin-list'),
   # path('discussion-parent-admin/<int:pk>/', DiscussionParentAdminViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='discussion-parent-admin-detail'),
    path('messages/', MessageViewSet.as_view({'get': 'list', 'post': 'create'}), name='message-list'),
    path('messages/<int:pk>/', MessageViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='message-detail'),
    path('transactions/', views.TransactionListView.as_view(), name='transaction-list'),
    path('transactions/<int:pk>/', views.TransactionDetailView.as_view(), name='transaction-detail'),
    path('evaluations/', views.EvaluationListAPIView.as_view(), name='evaluation-list-create'),
    path('evaluations/<int:pk>/', views.EvaluationRetrieveUpdateDestroyAPIView.as_view(), name='evaluation-detail'),
   # path('diplomes/', views.DiplomeListCreateAPIView.as_view(), name='diplome-list-create'),
   # path('diplomes/<int:pk>/', views.DiplomeRetrieveUpdateDestroyAPIView.as_view(), name='diplome-detail'),
    path('cours/', views.CoursListCreateAPIView.as_view(), name='cours-list-create'),
    path('cours/<int:pk>/', views.CoursRetrieveUpdateDestroyAPIView.as_view(), name='cours-detail'),
    
    path('suivi-professeur/<int:pk>/', views.SuiviProfesseurRetrieveUpdateAPIView.as_view(), name='suivi-professeur-detail'),
    path('suivi-professeur/', views.SuiviProfesseurListAPIView.as_view(), name='suivi-professeur-list'),
    # path('disponibilites/', views.DisponibiliteListCreateAPIView.as_view(), name='disponibilite_list_create'),
    # path('disponibilites/<int:pk>/', views.DisponibiliteRetrieveUpdateDestroyAPIView.as_view(), name='disponibilite_detail'),

    path('cours/', views.CoursReserveListCreateAPIView.as_view(), name='cours_reserve_list_create'),
    path('cours/<int:pk>/',views. CoursReserveRetrieveUpdateDestroyAPIView.as_view(), name='cours_reserve_detail'),
    path('reserver-cours/', views.reserver_cours, name='reserver_cours'),
    path('signaler-absence/', views.signaler_absence, name='signaler_absence'),
    path('demander-remboursement/', views.demander_remboursement, name='demander_remboursement'),
    path('planifier-rattrapage/', views.planifier_rattrapage, name='planifier_rattrapage'),
    path('creer/notification/', views.NotificationListCreateAPIView.as_view(), name='notification-list-create'),
    path('notifications/<int:pk>/', views.NotificationRetrieveUpdateDestroyAPIView.as_view(), name='notification-detail'),
    path('notifications/', obtenir_notifications, name='obtenir_notifications'),
    path('notification/<int:notification_id>/', update_notification_status, name='update_notification_status'),
    path('notifications/nombre_non_lues/', nombre_notifications_non_lues, name='nombre_notifications_non_lues'),
    path('ajouter_disponibilite/', ajouter_disponibilite, name='ajouter_disponibilite'),
    path('obtenir_disponibilites/<int:professeur_id>/', obtenir_disponibilites, name='obtenir_disponibilites'),
    path('reserver_disponibilite/', reserver_disponibilite, name='reserver_disponibilite'),
    path('supprimer_disponibilite/', views.supprimer_disponibilite, name='supprimer_disponibilite'),
    # path('reserver_cours_package/', views.reserver_cours_package, name='reserver_cours_package'),
    path('obtenir_categories_et_matieres/', obtenir_categories_et_matieres, name='obtenir_categories_et_matieres'),


    # re_path("product/((?P<pk>\d+)/)?", csrf_exempt(ParentView.as_view())),


]
