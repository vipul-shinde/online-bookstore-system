# Generated by Django 3.2.4 on 2021-07-22 05:01

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_cryptography.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0004_alter_user_card_four'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('status', models.CharField(default='Confirmed', max_length=20)),
                ('total', models.DecimalField(decimal_places=2, max_digits=5)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=11)),
                ('street', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
                ('zip_code', models.CharField(max_length=5)),
                ('county', models.CharField(max_length=10)),
                ('country', models.CharField(max_length=10)),
                ('card_name', django_cryptography.fields.encrypt(models.CharField(max_length=100))),
                ('card_num', django_cryptography.fields.encrypt(models.CharField(max_length=16))),
                ('card_exp', django_cryptography.fields.encrypt(models.CharField(max_length=5))),
                ('card_cvv', django_cryptography.fields.encrypt(models.CharField(max_length=3))),
                ('card_four', models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('percentage', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.RenameField(
            model_name='user',
            old_name='card_cvv',
            new_name='card_cvv1',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='card_exp',
            new_name='card_exp1',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='card_four',
            new_name='card_four1',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='card_name',
            new_name='card_name1',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='card_num',
            new_name='card_num1',
        ),
        migrations.AddField(
            model_name='user',
            name='card_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='card_cvv2',
            field=django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=3, null=True)),
        ),
        migrations.AddField(
            model_name='user',
            name='card_cvv3',
            field=django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=3, null=True)),
        ),
        migrations.AddField(
            model_name='user',
            name='card_exp2',
            field=django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=5, null=True)),
        ),
        migrations.AddField(
            model_name='user',
            name='card_exp3',
            field=django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=5, null=True)),
        ),
        migrations.AddField(
            model_name='user',
            name='card_four2',
            field=models.CharField(blank=True, default='', max_length=4),
        ),
        migrations.AddField(
            model_name='user',
            name='card_four3',
            field=models.CharField(blank=True, default='', max_length=4),
        ),
        migrations.AddField(
            model_name='user',
            name='card_name2',
            field=django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=100, null=True)),
        ),
        migrations.AddField(
            model_name='user',
            name='card_name3',
            field=django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=100, null=True)),
        ),
        migrations.AddField(
            model_name='user',
            name='card_num2',
            field=django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=16, null=True)),
        ),
        migrations.AddField(
            model_name='user',
            name='card_num3',
            field=django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=16, null=True)),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookstore.book')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookstore.order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='promotion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bookstore.promotion'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookstore.book')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookstore.cart')),
            ],
        ),
    ]
