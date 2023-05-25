# Generated by Django 4.2.1 on 2023-05-14 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_alter_user_id_subscription_post_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(max_length=264, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]