# Generated by Django 4.1.7 on 2023-03-14 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FirstApp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.IntegerField(unique=True)),
                ('price_dollars', models.IntegerField()),
                ('price_rubles', models.IntegerField()),
                ('delivery_time', models.DateField()),
            ],
        ),
    ]
