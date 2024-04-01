# Generated by Django 4.2.11 on 2024-04-01 05:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TextData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('race', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='VideoData',
            fields=[
                ('text_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='lipReadingDataset.textdata')),
                ('video_link', models.URLField()),
                ('duration', models.DurationField()),
            ],
        ),
        migrations.CreateModel(
            name='WordDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=50)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('text_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lipReadingDataset.textdata')),
            ],
        ),
    ]
