# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-27 00:21
from __future__ import unicode_literals

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
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='post_pics')),
                ('textpost', models.CharField(max_length=400)),
                ('posted_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=True, default='user_pics/user_default.png', upload_to='user_pics')),
                ('age', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('self_description', models.CharField(blank=True, max_length=400)),
                ('followers', models.ManyToManyField(blank=True, related_name='following', to='socialnetwork.Profile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='message',
            field=models.ManyToManyField(blank=True, default='', to='socialnetwork.Profile'),
        ),
        migrations.AddField(
            model_name='post',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_profile', to='socialnetwork.Profile'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='socialnetwork.Post'),
        ),
        migrations.AddField(
            model_name='comment',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialnetwork.Profile'),
        ),
    ]
