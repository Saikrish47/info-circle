# Generated by Django 2.2.1 on 2020-02-02 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SearchQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(max_length=220)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
