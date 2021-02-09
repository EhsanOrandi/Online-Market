# Generated by Django 3.1.3 on 2021-01-29 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210107_1039'),
        ('products', '0002_auto_20210107_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='category/image', verbose_name='Image'),
        ),
        migrations.AlterUniqueTogether(
            name='shopproduct',
            unique_together={('shop', 'product')},
        ),
    ]