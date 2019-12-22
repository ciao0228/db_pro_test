from django.db import models


# Create your models here.

class Problem(models.Model):
    no = models.IntegerField(db_column='No', primary_key=True)  # Field name made lowercase.
    userno = models.IntegerField(db_column='userNo', blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(max_length=255, blank=True, null=True)
    problem_des = models.CharField(max_length=255, blank=True, null=True)
    diff = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'problem'


class Raisepro(models.Model):
    no = models.IntegerField(db_column='No', primary_key=True)  # Field name made lowercase.
    userno = models.IntegerField(db_column='userNo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'raisepro'


class ReconRle(models.Model):
    problemtype = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recon_rle'


class Solve(models.Model):
    problemno = models.IntegerField(db_column='problemNo', primary_key=True)  # Field name made lowercase.
    solverno = models.IntegerField(db_column='solverNo', blank=True, null=True)  # Field name made lowercase.
    content = models.CharField(max_length=255, blank=True, null=True)
    mark = models.CharField(max_length=255, blank=True, null=True)
    visit_enduml = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'solve'


class TypeRefer(models.Model):
    problemno = models.IntegerField(db_column='problemNo', primary_key=True)  # Field name made lowercase.
    string = models.CharField(db_column='String', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'type_refer'


class User(models.Model):
    no = models.IntegerField(db_column='No', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=255, blank=True, null=True)
    phonenum = models.IntegerField(db_column='phoneNum', blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class Problem(models.Model):
    no = models.IntegerField(db_column="No", primary_key=True)
    name = models.CharField(db_column='type',max_length=255, blank=True, null=True)
    problemdes=models.CharField(db_column='problem_des',max_length=3000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'problem'
