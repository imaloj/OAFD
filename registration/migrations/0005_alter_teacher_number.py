# Generated by Django 5.0.1 on 2024-01-29 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_alter_teacher_number_alter_teacher_teacher_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='number',
            field=models.IntegerField(default='9800000000', help_text='Enter Your Number', unique=True),
        ),
    ]
