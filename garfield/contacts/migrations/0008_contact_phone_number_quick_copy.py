# Generated by Django 2.2.2 on 2019-06-25 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0007_contact_recruiter'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='phone_number_quick_copy',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
    ]