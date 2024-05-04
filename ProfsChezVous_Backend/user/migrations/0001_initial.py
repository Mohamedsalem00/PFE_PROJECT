# Generated by Django 4.2.11 on 2024-05-01 00:32

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_resized.forms
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_parent', models.BooleanField(default=False)),
                ('is_eleve', models.BooleanField(default=False)),
                ('is_professeur', models.BooleanField(default=False)),
                ('image_profil', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[1920, 1080], upload_to=user.models.upload_to)),
                ('cree_le', models.DateTimeField(auto_now_add=True)),
                ('modifie_le', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Professeur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('prenom', models.CharField(max_length=30)),
                ('ville', models.CharField(max_length=100)),
                ('numero_telephone', models.CharField(max_length=12)),
                ('experience_enseignement', models.CharField(max_length=100)),
                ('certifications', models.CharField(max_length=100)),
                ('date_naissance', models.DateField()),
                ('matiere_a_enseigner', models.CharField(max_length=100)),
                ('niveau_etude', models.CharField(max_length=50)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='professeur', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('prenom', models.CharField(max_length=30)),
                ('ville', models.CharField(max_length=100)),
                ('date_naissance', models.DateField()),
                ('numero_telephone', models.CharField(max_length=12)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='parent', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Enfant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prenom', models.CharField(max_length=30)),
                ('nom', models.CharField(max_length=50)),
                ('date_naissance', models.DateField()),
                ('annee_scolaire', models.CharField(max_length=100)),
                ('etablissement', models.CharField(max_length=100)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enfants', to='user.parent')),
            ],
            options={
                'db_table': 'user_enfant',
            },
        ),
        migrations.CreateModel(
            name='Eleve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('prenom', models.CharField(max_length=30)),
                ('ville', models.CharField(max_length=100)),
                ('date_naissance', models.DateField()),
                ('Etablissement', models.CharField(max_length=100)),
                ('niveau_scolaire', models.CharField(max_length=100)),
                ('numero_telephone', models.CharField(max_length=12)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='eleve', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='admin', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
