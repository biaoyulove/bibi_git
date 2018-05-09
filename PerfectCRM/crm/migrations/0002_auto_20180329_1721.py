# Generated by Django 2.0.3 on 2018-03-29 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='tags',
            field=models.ManyToManyField(to='crm.Tag'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='roles',
            field=models.ManyToManyField(to='crm.Role'),
        ),
    ]