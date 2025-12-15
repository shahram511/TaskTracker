from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('شماره تلفن الزامی است')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(phone_number, password, **extra_fields)
    
 

class User(AbstractUser):
    phone_number = models.CharField(max_length=11, unique=True,verbose_name='شماره تلفن')
    email = models.EmailField(unique=True,verbose_name='ایمیل',null=True,blank=True)
    first_name = models.CharField(max_length=100,verbose_name='نام')
    last_name = models.CharField(max_length=100,verbose_name='نام خانوادگی')
    username = models.CharField(max_length=100,null=True,blank=True,verbose_name='نام کاربری')
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username','email']
    
    objects = UserManager()
    
    def __str__(self):
        return self.phone_number
    
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
        
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/',null=True,blank=True)
    bio = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

     
@receiver(post_save, sender=User)         
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
        
