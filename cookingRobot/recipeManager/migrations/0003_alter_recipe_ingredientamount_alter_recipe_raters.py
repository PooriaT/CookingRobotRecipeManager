# Generated by Django 4.0.6 on 2022-08-13 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipeManager', '0002_alter_recipe_ingredientamount_alter_recipe_raters'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredientAmount',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='raters',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]