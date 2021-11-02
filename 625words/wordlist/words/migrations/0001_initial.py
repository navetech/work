# Generated by Django 3.1.5 on 2021-11-01 23:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('phrases', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grouping_key', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Thema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('sort_number', models.FloatField(blank=True, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_number', models.FloatField(blank=True, default=0)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group_Word_related', to='words.group')),
                ('meaning', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meaning_Word_related', to='phrases.meaning')),
                ('thema', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='thema_Word_related', to='words.thema')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='base_word',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='base_word_Group_related', to='words.word'),
        ),
    ]
