# Generated by Django 5.0.3 on 2024-03-07 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phone', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
    ]
