# Generated by Django 3.2.4 on 2021-07-20 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0003_auto_20210720_2337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='card_four',
            field=models.CharField(blank=True, default='', max_length=4),
        ),
    ]
