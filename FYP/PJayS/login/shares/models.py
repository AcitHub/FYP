from django.db import models
from student.models import Member
from teacher.models import Teacher
import uuid

class Saham(models.Model):
    share_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)  # Unique identifier for each share entry
    student = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)  # Link to student, if applicable
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)  # Link to teacher, if applicable
    share_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount of shares (financial value)
    share_date = models.DateField(auto_now_add=True)  # Date when the share was issued or updated
    share_type = models.CharField(max_length=20, choices=[('Initial', 'Initial'), ('Additional', 'Additional')], default='Initial')  # Type of share

    def __str__(self):
        if self.teacher:
            return f"Share for Teacher: {self.teacher.nama} - {self.share_amount} RM"
        elif self.student:
            return f"Share for Student: {self.student.nama} - {self.share_amount} RM"
        return f"Share - {self.share_amount} RM"
