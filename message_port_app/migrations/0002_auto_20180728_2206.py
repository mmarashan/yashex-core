# Generated by Django 2.0.7 on 2018-07-28 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message_port_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='reciever_address',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='sender_address',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
