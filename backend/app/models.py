from django.db import models


class User(models.Model):

    name=models.CharField(max_length=15)
    joining_code=models.CharField(max_length=32)


    def __str__(self):
        return self.name

class JoinCode(models.Model):
    creater=models.ForeignKey(User,max_length=10,related_name="creater",on_delete=models.CASCADE)
    joiner=models.ForeignKey(User,max_length=10,related_name="joiner",blank=True,on_delete=models.CASCADE)



    


