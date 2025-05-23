# Generated by Django 5.2 on 2025-05-20 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserOtp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255)),
                ('otp', models.CharField(blank=True, max_length=5, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
