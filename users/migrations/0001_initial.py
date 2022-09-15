# Generated by Django 4.0.6 on 2022-09-14 03:54

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admins', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('fname', models.CharField(blank=True, max_length=50, null=True)),
                ('lname', models.CharField(blank=True, max_length=50, null=True)),
                ('phone', models.CharField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator(message='Up to 15 digits allowed.', regex='^\\+?1?\\d{9,15}$')])),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('address', models.TextField(blank=True, max_length=500, null=True)),
                ('postcode', models.CharField(blank=True, max_length=50, null=True)),
                ('password', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('email_otp', models.CharField(blank=True, max_length=9, null=True)),
                ('phone_otp', models.CharField(blank=True, max_length=9, null=True)),
                ('count_otp', models.IntegerField(default=0, help_text='Number of otp sent')),
                ('is_verified', models.BooleanField(default=False)),
                ('verified_chioce', models.CharField(choices=[('phone', 'phone'), ('email', 'email')], default='phone', help_text='If otp verification got successful', max_length=100)),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('super', models.BooleanField(default=False)),
                ('is_del', models.BooleanField(default=False)),
                ('is_blocked', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='area', to='admins.location')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city', to='admins.location')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=100)),
                ('is_del', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TempData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(choices=[('registration', 'registration'), ('edit_profile', 'edit_profile'), ('login', 'login')], max_length=100, null=True)),
                ('phone_or_email', models.CharField(choices=[('phone', 'phone'), ('email', 'email')], default='phone', max_length=100)),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('phone', models.CharField(max_length=15, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Up to 15 digits allowed.', regex='^\\+?1?\\d{9,15}$')])),
                ('phone_otp', models.CharField(blank=True, max_length=9, null=True)),
                ('email_otp', models.CharField(blank=True, max_length=9, null=True)),
                ('phone_verified', models.BooleanField(default=False)),
                ('email_verified', models.BooleanField(default=False)),
                ('is_del', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.roles'),
        ),
        migrations.AddField(
            model_name='user',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='state', to='admins.location'),
        ),
    ]
