# Generated by Django 4.2 on 2023-04-05 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0002_alter_pet_sex'),
        ('traits', '0003_alter_trait_pets'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trait',
            name='pets',
            field=models.ManyToManyField(related_name='traits', to='pets.pet'),
        ),
    ]
