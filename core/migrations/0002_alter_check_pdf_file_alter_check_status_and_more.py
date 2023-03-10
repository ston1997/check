# Generated by Django 4.1.5 on 2023-02-18 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='core',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='core',
            name='status',
            field=models.CharField(choices=[('NEW', 'New'), ('RENDERED', 'Rendered'), ('PRINTED', 'Printed')], default='NEW', max_length=200, verbose_name='Статус чеку'),
        ),
        migrations.AlterField(
            model_name='printer',
            name='point_id',
            field=models.IntegerField(verbose_name='ID точки'),
        ),
    ]
