# Generated by Django 3.2.7 on 2021-10-07 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gallery', '0005_posts_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='post',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
