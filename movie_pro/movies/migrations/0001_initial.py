# Generated by Django 2.1.7 on 2019-05-13 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TbClassification',
            fields=[
                ('id_classification', models.AutoField(primary_key=True, serialize=False)),
                ('classification', models.CharField(blank=True, max_length=128, null=True)),
            ],
            options={
                'db_table': 'tb_classification',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TbComment',
            fields=[
                ('c_id', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.TextField(blank=True, null=True)),
                ('comment_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tb_comment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TbLoginIp',
            fields=[
                ('id_ip', models.AutoField(primary_key=True, serialize=False)),
                ('ip_addr', models.CharField(blank=True, max_length=128, null=True)),
                ('login_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tb_login_ip',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TbMovie',
            fields=[
                ('m_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=128, null=True)),
                ('actor', models.CharField(blank=True, max_length=1024, null=True)),
                ('language', models.CharField(blank=True, max_length=128, null=True)),
                ('director', models.CharField(blank=True, max_length=256, null=True)),
                ('release_date', models.DateTimeField(blank=True, null=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('score', models.CharField(blank=True, max_length=128, null=True)),
                ('synopsis', models.TextField(blank=True, null=True)),
                ('main_pic', models.CharField(blank=True, max_length=256, null=True)),
                ('pic', models.CharField(blank=True, max_length=1024, null=True)),
                ('download_name', models.CharField(blank=True, max_length=1024, null=True)),
                ('download_size', models.CharField(blank=True, max_length=128, null=True)),
                ('download_thunder', models.CharField(blank=True, max_length=4096, null=True)),
            ],
            options={
                'db_table': 'tb_movie',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TbMovieClassifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'tb_movie_classifications',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TbRegion',
            fields=[
                ('id_region', models.AutoField(primary_key=True, serialize=False)),
                ('region', models.CharField(blank=True, max_length=128, null=True)),
            ],
            options={
                'db_table': 'tb_region',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TbSuggestion',
            fields=[
                ('s_id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.TextField(blank=True, null=True)),
                ('submit_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tb_suggestion',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TbUser',
            fields=[
                ('u_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, max_length=128, null=True)),
                ('password', models.CharField(blank=True, max_length=128, null=True)),
                ('email', models.CharField(blank=True, max_length=128, null=True)),
                ('phone', models.CharField(blank=True, max_length=128, null=True)),
                ('register_date', models.DateTimeField(blank=True, null=True)),
                ('register_ip', models.CharField(blank=True, max_length=64, null=True)),
                ('u_status', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tb_user',
                'managed': False,
            },
        ),
    ]