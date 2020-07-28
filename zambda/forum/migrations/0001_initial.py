# Generated by Django 3.0.4 on 2020-07-27 22:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(blank=True, default='0d9c33f646', max_length=100, null=True)),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('reported', models.BooleanField(default=False)),
                ('public', models.BooleanField(default=False)),
                ('modified_on', models.DateField(auto_now=True)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='msg_receiver', to=settings.AUTH_USER_MODEL)),
                ('receivers', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='msg_sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PrivateMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, null=True)),
                ('message_html', models.TextField(blank=True, null=True)),
                ('message_contents', models.TextField(blank=True, null=True)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_html', models.TextField(blank=True, null=True)),
                ('message_contents', models.TextField(blank=True, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('email', models.BooleanField(default=False)),
                ('thread', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='forum.Thread')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
