# Generated by Django 4.2 on 2025-04-21 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoapp', '0014_activitylog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeprofile',
            name='email',
            field=models.EmailField(default='temp@example.com', max_length=254),
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='password',
            field=models.CharField(default='password123', max_length=100),
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='phone',
            field=models.CharField(default='0000000000', max_length=50),
        ),
    ]
