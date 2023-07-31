# Generated by Django 4.1.4 on 2023-07-20 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0003_alter_image_user'),
        ('tags', '0002_alter_tags_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tags',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='image.image'),
        ),
    ]