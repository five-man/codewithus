from cProfile import label
from django.db import models

from member.models import Member

# Create your models here.

class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'tag'
        app_label = 'member'


class Algorithm(models.Model):
    algo_no = models.AutoField(primary_key=True)
    algo_update = models.DateField()
    algo_title = models.CharField(max_length=50)
    algo_detail = models.TextField()
    member_no = models.ForeignKey(Member, on_delete=models.CASCADE, db_column='member_no')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'algorithm'
        app_label = 'member'





class Solution(models.Model):
    sol_no = models.AutoField(primary_key=True)
    algo_no = models.ForeignKey(Algorithm, on_delete=models.CASCADE, db_column='algo_no')
    sol_detail = models.TextField()
    sol_like = models.IntegerField()
    member_no = models.ForeignKey(Member, on_delete=models.CASCADE, db_column='member_no')

    class Meta:
        managed = False
        db_table = 'solution'
        unique_together = (('sol_no', 'algo_no'),)



class AlgorithmImage(models.Model):
    image_no = models.AutoField(primary_key=True)
    algo_no = models.ForeignKey(Algorithm, on_delete=models.CASCADE, db_column='algo_no')
    image_root = models.CharField(max_length=1000)
    image_name = models.CharField(max_length=1000)
    # image = models.ImageField()

    class Meta:
        managed = False
        db_table = 'algorithm_image'
        unique_together = (('image_no', 'algo_no'),)
        app_label = 'member'


class Comment(models.Model):
    comment_no = models.AutoField(primary_key=True)
    sol_no = models.ForeignKey(Solution, on_delete=models.CASCADE, db_column='sol_no', related_name='cmt_rel_sol_no')
    algo_no = models.ForeignKey(Solution, on_delete=models.CASCADE, db_column='algo_no', related_name='cmt_rel_algo_no')
    comment_detail = models.TextField()
    member_no = models.ForeignKey(Member, on_delete=models.CASCADE, db_column='member_no')

    class Meta:
        managed = False
        db_table = 'comment'
        unique_together = (('comment_no', 'sol_no', 'algo_no'),)




class Likes(models.Model):
    likes_no = models.AutoField(primary_key=True)
    sol_no = models.ForeignKey(Solution, on_delete=models.CASCADE, db_column='sol_no', related_name='likes_rel_sol_no')
    algo_no = models.ForeignKey(Solution, on_delete=models.CASCADE, db_column='algo_no', related_name='likes_rel_algo_no')
    member_no = models.ForeignKey(Member, on_delete=models.CASCADE, db_column='member_no')

    class Meta:
        managed = False
        db_table = 'likes'
        unique_together = (('likes_no', 'sol_no', 'algo_no', 'member_no'),)
