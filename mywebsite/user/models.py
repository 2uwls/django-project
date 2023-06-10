from django.db import models

class Member(models.Model):
    memberID = models.CharField(max_length=15, verbose_name='아이디')
    password = models.CharField(max_length=15, verbose_name='비밀번호')
    name = models.CharField(max_length=30, verbose_name='사용자명')
    email = models.EmailField(max_length=30, verbose_name='이메일')
    register_dttm = models.DateTimeField(auto_now_add=True, verbose_name='회원가입일자')
    
    class Meta:
        db_table='MEMBER'