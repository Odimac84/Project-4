# Generated by Django 3.2.8 on 2021-10-27 07:41

import blog.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_post_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=blog.models.NameField(max_length=50),
        ),
    ]
