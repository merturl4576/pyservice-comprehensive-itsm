import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pyservice.settings')
django.setup()

from django.contrib.auth import get_user_model
from cmdb.models import Company, Department, Asset, AssetInventory
from incidents.models import Incident
from service_requests.models import ServiceRequest
from remote_support.models import RemoteSupportSession
from knowledge.models import Category, Article
from notifications.models import Notification

User = get_user_model()

def setup():
    print("Setting up initial tenants and superadmin...")
    
    # 1. Create Demo Company
    demo_company, created = Company.objects.get_or_create(
        name='Demo',
        defaults={'is_demo': True}
    )
    if created:
        print("Created Demo company.")
    else:
        print("Demo company already exists.")

    # 2. Create Super Admin
    try:
        super_admin = User.objects.get(username='merturl67')
        print("Super admin 'merturl67' already exists.")
        # Ensure it has super_admin flag and correct password
        super_admin.is_super_admin = True
        super_admin.set_password('Vianasec4576!')
        super_admin.save()
    except User.DoesNotExist:
        super_admin = User.objects.create_superuser(
            username='merturl67',
            email='merturl67@gmail.com',
            password='Vianasec4576!'
        )
        super_admin.is_super_admin = True
        super_admin.save()
        print("Created super admin 'merturl67'.")

    # 3. Associate all existing data with Demo company
    # Users (except superadmin)
    users_updated = User.objects.exclude(username='merturl67').update(company=demo_company)
    print(f"Assigned {users_updated} users to Demo company.")

    depts_updated = Department.objects.update(company=demo_company)
    print(f"Assigned {depts_updated} departments to Demo company.")

    assets_updated = Asset.objects.update(company=demo_company)
    print(f"Assigned {assets_updated} assets to Demo company.")

    inventory_updated = AssetInventory.objects.update(company=demo_company)
    print(f"Assigned {inventory_updated} inventory items to Demo company.")

    incidents_updated = Incident.objects.update(company=demo_company)
    print(f"Assigned {incidents_updated} incidents to Demo company.")

    requests_updated = ServiceRequest.objects.update(company=demo_company)
    print(f"Assigned {requests_updated} service requests to Demo company.")

    sessions_updated = RemoteSupportSession.objects.update(company=demo_company)
    print(f"Assigned {sessions_updated} remote sessions to Demo company.")

    categories_updated = Category.objects.update(company=demo_company)
    print(f"Assigned {categories_updated} KB categories to Demo company.")

    articles_updated = Article.objects.update(company=demo_company)
    print(f"Assigned {articles_updated} KB articles to Demo company.")

    notifications_updated = Notification.objects.update(company=demo_company)
    print(f"Assigned {notifications_updated} notifications to Demo company.")

    print("Setup complete successfully!")

if __name__ == '__main__':
    setup()
