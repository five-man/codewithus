from django.db import models

from member.models import Member

# Create your models here.


class File(models.Model):
    file_no = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=50)
    file_date = models.DateTimeField()
    file_volume = models.BigIntegerField()
    file_root = models.CharField(max_length=1000)
    member_no = models.ForeignKey(Member, on_delete=models.CASCADE, db_column='member_no')

    class Meta:
        managed = False
        app_label = 'member'
        db_table = 'file'


class FileList(models.Model):
    file_file = models.AutoField(primary_key=True)
    file_no = models.ForeignKey(File, on_delete=models.CASCADE, db_column='file_no')
    file_root = models.CharField(max_length=1000)
    file_name = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'file_list'
        unique_together = (('file_file', 'file_no'),)