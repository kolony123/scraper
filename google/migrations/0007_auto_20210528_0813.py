# Generated by Django 3.2.3 on 2021-05-28 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('google', '0006_timelimit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scrapperresult',
            name='description_result',
        ),
        migrations.RemoveField(
            model_name='scrapperresult',
            name='title_result',
        ),
        migrations.AddField(
            model_name='scrapperresult',
            name='most_common_descriptions',
            field=models.TextField(default='dupa'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scrapperresult',
            name='most_common_titles',
            field=models.TextField(default='dupa'),
            preserve_default=False,
        ),
    ]
