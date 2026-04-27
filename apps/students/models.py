from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class StudentProfile(models.Model):
    STATUS_CHOICES = (('pending', 'Pending'), ('done', 'Done'))
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True)
    real_name = models.CharField(max_length=50, blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')
    dorm_info = models.CharField(max_length=100, blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    report_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'student_profiles'
        verbose_name = 'Student Profile'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.student_id} - {self.real_name}'

@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(user=instance, student_id=instance.username)

@receiver(post_save, sender=User)
def save_student_profile(sender, instance, **kwargs):
    try:
        instance.student_profile.save()
    except StudentProfile.DoesNotExist:
        StudentProfile.objects.create(user=instance, student_id=instance.username)
