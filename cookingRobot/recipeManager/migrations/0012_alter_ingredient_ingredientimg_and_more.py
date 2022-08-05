# Generated by Django 4.0.6 on 2022-08-03 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipeManager', '0011_alter_ingredient_ingredientname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='ingredientImg',
            field=models.ImageField(blank=True, default='default/noImage.jpeg', null=True, upload_to='ingredient/'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='recipeImg',
            field=models.ImageField(blank=True, default='default/noImage.jpeg', null=True, upload_to='recipe/'),
        ),
        migrations.AlterField(
            model_name='utensil',
            name='utensilImg',
            field=models.ImageField(blank=True, default='default/noImage.jpeg', null=True, upload_to='utensil'),
        ),
    ]