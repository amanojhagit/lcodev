from django.db import migrations
from api.user.models import CustomUser


class Migration(migrations.Migration):
    def seed_data(apps,schema_editor):
        user=CustomUser(name="aman",email='aman@gmail.com',is_staff=True, is_superuser=True,phone="7894561230",gender="Male")

        user.set_password("12345")
        user.save()

    dependencies = [
    
    ]

    operations = [
        migrations.RunPython(seed_data),
    
    ]