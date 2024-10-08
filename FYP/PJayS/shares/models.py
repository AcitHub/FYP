from django.db import models
from teacher.models import Teacher
from django.utils.timezone import now

class SahamTeacher(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_saham_added = models.DateField(default=now, editable=False)

    def __str__(self):
        return f"{self.teacher.nama} - {self.amount}"
