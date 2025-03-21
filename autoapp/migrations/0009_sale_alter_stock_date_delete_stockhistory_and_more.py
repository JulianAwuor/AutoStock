# Generated by Django 4.2 on 2025-03-20 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autoapp', '0008_stockhistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantitysold', models.PositiveIntegerField()),
                ('sellingprice', models.DecimalField(decimal_places=2, max_digits=12)),
                ('datesold', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='stock',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.DeleteModel(
            name='StockHistory',
        ),
        migrations.AddField(
            model_name='sale',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autoapp.stock'),
        ),
    ]
