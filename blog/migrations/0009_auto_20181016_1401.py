# Generated by Django 2.0.5 on 2018-10-16 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_indentx'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='indentx',
            name='how_many',
        ),
        migrations.AddField(
            model_name='indentx',
            name='how_many_even',
            field=models.IntegerField(default=10, verbose_name='Indent even'),
        ),
        migrations.AddField(
            model_name='indentx',
            name='how_many_odd',
            field=models.IntegerField(default=20, verbose_name='Indent odd'),
        ),
    ]
