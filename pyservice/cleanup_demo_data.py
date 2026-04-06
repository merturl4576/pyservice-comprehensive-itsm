import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pyservice.settings")
django.setup()

from django.contrib.auth import get_user_model
from cmdb.models import Department

User = get_user_model()

def cleanup_demo_data():
    print("Cleaning up demo data...")
    
    # The pattern used was {dept_code}_user_{i}
    # We can find them by checking if they end with _user_1, _user_2 etc.
    # Or iterate departments exactly as we did in creation
    
    departments = Department.objects.all()
    deleted_count = 0
    
    for dept in departments:
        dept_code = dept.name.lower().replace(' ', '_')[:10]
        for i in range(1, 3): # We created up to 2
            username = f"{dept_code}_user_{i}"
            try:
                user = User.objects.get(username=username)
                print(f"Deleting user: {username} (this will cascade delete their incidents/requests)")
                user.delete()
                deleted_count += 1
            except User.DoesNotExist:
                pass
                
    print(f"Cleanup complete. Deleted {deleted_count} users and their related data.")

if __name__ == "__main__":
    cleanup_demo_data()
