# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Meetings(models.Model):
    mid = models.IntegerField(db_column='mID', primary_key=True)  # Field name made lowercase.
    mdate = models.DateField(db_column='mDate', blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Meetings'


class Residentsmeetings(models.Model):
    pk = models.CompositePrimaryKey('rid', 'mid')
    rid = models.IntegerField(db_column='rID')  # Field name made lowercase.
    mid = models.IntegerField(db_column='mID')  # Field name made lowercase.
    risk = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ResidentsMeetings'


class Surveillance(models.Model):
    pk = models.CompositePrimaryKey('vid', 'mid', 'rid')
    vid = models.IntegerField(db_column='vID')
    mid = models.IntegerField(db_column='mID')
    rid = models.IntegerField(db_column='rID')
    method = models.CharField(max_length=50, blank=True, null=True)
    clevel = models.IntegerField(db_column='cLevel', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Surveillance'


class Villains(models.Model):
    vid = models.IntegerField(db_column='vID', primary_key=True)  # Field name made lowercase.
    favlocation = models.CharField(db_column='favLocation', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Villains'
