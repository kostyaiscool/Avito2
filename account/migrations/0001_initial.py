# Generated by Django 5.0.6 on 2024-06-16 08:09

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ach',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Achname')),
                ('description', models.CharField(blank=True, max_length=200, null=True, verbose_name='Description')),
                ('icon', models.ImageField(upload_to='achicons')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='Email address')),
                ('number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=20, null=True, region=None, unique=True, verbose_name='Phone number')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='Username')),
                ('avatar', models.ImageField(default='default.png', upload_to='icons')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_email_confirmed', models.BooleanField(default=False)),
                ('is_phone_confirmed', models.BooleanField(default=False)),
                ('is_email_2fa_enabled', models.BooleanField(default=False)),
                ('is_phone_2fa_enabled', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('achs', models.ManyToManyField(blank=True, to='account.ach')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
