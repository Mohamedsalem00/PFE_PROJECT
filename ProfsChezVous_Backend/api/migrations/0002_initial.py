# Generated by Django 5.0.3 on 2024-04-26 10:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0001_initial'),
        ('user', '0003_alter_enfant_table_transaction'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Matiere',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_complet', models.CharField(help_text='Nom complet de la matière', max_length=150)),
                ('symbole', models.CharField(help_text='Symbole de la matière', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Activite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=200)),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField()),
                ('lieu', models.CharField(max_length=200)),
                ('participants', models.ManyToManyField(related_name='activites', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ActiviteBloquee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raison', models.CharField(max_length=200)),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField()),
                ('activite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.activite')),
            ],
        ),
        migrations.CreateModel(
            name='Cours_Unite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sujet', models.TextField(max_length=100)),
                ('date', models.DateField()),
                ('heure_debut', models.TimeField(default='00:00')),
                ('duree', models.PositiveIntegerField(choices=[(60, '1 hour'), (120, '2 hours'), (180, '3 hours'), (240, '4 hours')])),
                ('statut', models.CharField(choices=[('R', 'Réservé'), ('C', 'Confirmé'), ('A', 'Annulé')], default='R', max_length=1)),
                ('lieu_des_cours', models.CharField(choices=[('la_maison', 'La maison'), ('a_distance', 'À distance')], max_length=50)),
                ('professeur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cours_unite', to='user.professeur')),
                ('matiere', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.matiere')),
            ],
        ),
        migrations.CreateModel(
            name='Cours_Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('duree', models.PositiveIntegerField(help_text='Durée du forfait en jours')),
                ('date_debut', models.DateField(help_text='Date de début de la validité du forfait')),
                ('date_fin', models.DateField(help_text='Date de fin de la validité du forfait')),
                ('est_actif', models.BooleanField(default=True, help_text='Le forfait est-il actuellement actif ?')),
                ('nombre_semaines', models.PositiveIntegerField(choices=[(1, '1 semaine'), (2, '2 semaines'), (3, '3 semaines'), (4, '4 semaines'), (5, '5 semaines'), (6, '6 semaines'), (7, '7 semaines'), (8, '8 semaines')], help_text='Nombre de semaines')),
                ('nombre_eleves', models.PositiveIntegerField(choices=[(1, '1 élève'), (2, '2 élèves'), (3, '3 élèves'), (4, '4 élèves'), (5, '5 élèves')], help_text="Nombre d'élèves")),
                ('heures_par_semaine', models.CharField(choices=[('2h', '2 heures'), ('4h', '4 heures'), ('6h', '6 heures'), ('8h', '8 heures'), ('10h', '10 heures'), ('12h', '12 heures'), ('14h', '14 heures')], help_text="Nombre d'heures par semaine", max_length=10)),
                ('prix', models.DecimalField(decimal_places=2, max_digits=10)),
                ('matiere', models.ForeignKey(help_text='Matière du cours', on_delete=django.db.models.deletion.PROTECT, to='api.matiere')),
            ],
        ),
        migrations.CreateModel(
            name='CommentaireCours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenu', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentaires_parent', to='user.parent')),
                ('professeur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentaires_professeur', to='user.professeur')),
                ('Cours_Package', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='commentaires', to='api.cours_package')),
                ('Cours_Unite', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='commentaires', to='api.cours_unite')),
                ('matiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentaires', to='api.matiere')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenu', models.TextField()),
                ('date_envoi', models.DateTimeField(auto_now_add=True)),
                ('lu', models.BooleanField(default=False)),
                ('sujet', models.CharField(max_length=255)),
                ('destinataire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_received', to=settings.AUTH_USER_MODEL)),
                ('expediteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_sent', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DiscussionProfAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sujet', models.CharField(max_length=200)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('derniere_activite', models.DateTimeField(auto_now=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discussions_avec_prof', to='user.admin')),
                ('professeur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discussions_avec_admin', to='user.professeur')),
                ('messages', models.ManyToManyField(related_name='messages_prof_admin', to='api.message')),
            ],
        ),
        migrations.CreateModel(
            name='DiscussionParentAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sujet', models.CharField(max_length=200)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('derniere_activite', models.DateTimeField(auto_now=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discussions_avec_parent', to='user.admin')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discussions_avec_admin', to='user.parent')),
                ('messages', models.ManyToManyField(related_name='messages_parent_admin', to='api.message')),
            ],
        ),
    ]
