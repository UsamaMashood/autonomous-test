# Generated by Django 3.2.6 on 2022-03-13 05:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('apps', '0003_app_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='last_update_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='app',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apps', to='auth.user'),
        ),
    ]
