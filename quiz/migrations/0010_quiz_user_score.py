# Generated by Django 4.1.13 on 2024-03-05 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0009_alter_quiz_solved'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='user_score',
            field=models.IntegerField(null=True),
        ),
    ]
