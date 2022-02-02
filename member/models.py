from django.db import models


class Member(models.Model):
    member_no = models.AutoField(primary_key=True)
    member_email = models.CharField(max_length=50)
    member_name = models.CharField(max_length=10)
    member_password = models.CharField(max_length=20)
    member_joindate = models.DateTimeField()
    admin_flag = models.IntegerField(default=0)
    member_status = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'member'
        