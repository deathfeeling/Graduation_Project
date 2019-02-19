# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TbClassification(models.Model):
    id_classification = models.AutoField(primary_key=True)
    classification = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_classification'


class TbComment(models.Model):
    c_id = models.AutoField(primary_key=True)
    comment = models.TextField(blank=True, null=True)
    id_user = models.ForeignKey('TbUser', models.DO_NOTHING, db_column='id_user', blank=True, null=True)
    m = models.ForeignKey('TbMovie', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_comment'


class TbLoginIp(models.Model):
    id_ip = models.AutoField(primary_key=True)
    ip_addr = models.CharField(max_length=128, blank=True, null=True)
    login_date = models.DateTimeField(blank=True, null=True)
    u = models.ForeignKey('TbUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_login_ip'


class TbMovie(models.Model):
    m_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128, blank=True, null=True)
    actor = models.CharField(max_length=1024, blank=True, null=True)
    language = models.CharField(max_length=128, blank=True, null=True)
    director = models.CharField(max_length=256, blank=True, null=True)
    release_date = models.DateTimeField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)
    score = models.CharField(max_length=128, blank=True, null=True)
    synopsis = models.TextField(blank=True, null=True)
    main_pic = models.CharField(max_length=256, blank=True, null=True)
    pic = models.CharField(max_length=1024, blank=True, null=True)
    download_name = models.CharField(max_length=1024, blank=True, null=True)
    download_size = models.CharField(max_length=128, blank=True, null=True)
    download_thunder = models.CharField(max_length=4096, blank=True, null=True)
    id_region = models.ForeignKey('TbRegion', models.DO_NOTHING, db_column='id_region', blank=True, null=True)
    classification = models.ManyToManyField(TbClassification, through='TbMovieClassifications')

    class Meta:
        managed = False
        db_table = 'tb_movie'


class TbMovieClassifications(models.Model):
    m = models.ForeignKey(TbMovie, models.DO_NOTHING, blank=True, null=True)
    id_classification = models.ForeignKey(TbClassification, models.DO_NOTHING, db_column='id_classification', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_movie_classifications'


class TbRegion(models.Model):
    id_region = models.AutoField(primary_key=True)
    region = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_region'


class TbUser(models.Model):
    u_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=128, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    email = models.CharField(max_length=128, blank=True, null=True)
    phone = models.CharField(max_length=128, blank=True, null=True)
    register_date = models.DateTimeField(blank=True, null=True)
    register_ip = models.CharField(max_length=64, blank=True, null=True)
    u_status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_user'
