# Generated by Django 4.2.8 on 2023-12-04 13:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('book_catalog', '0003_remove_book_genre_book_genres'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.TextField(default=django.utils.timezone.now, max_length=5000),
            preserve_default=False,
        ),
    ]