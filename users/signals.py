from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from users.models import Profile

# createProfile when user is created
def createProfile(sender, created, instance, **kwargs):
    if created:
        user= instance
        user_profile = Profile.objects.create(
            user= user,
            name= user.first_name,
            username= user.username,
            email= user.email,
            )

# update user when profile is updated
def updateProfile(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

# delete user when profile is deleted
def deleteProfile(sender, instance, **kwargs):
    instance.user.delete()

post_save.connect(createProfile, sender=User)
post_save.connect(updateProfile, sender=Profile)
post_delete.connect(deleteProfile, sender=Profile)