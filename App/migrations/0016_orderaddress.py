# Generated by Django 3.0.5 on 2020-05-14 23:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0015_order_o_remarks'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a_detail', models.CharField(max_length=256)),
                ('a_phone', models.CharField(max_length=32)),
                ('a_nickname', models.CharField(max_length=64)),
                ('a_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.Order', unique=True)),
            ],
            options={
                'db_table': 'axf_order_address',
            },
        ),
    ]
