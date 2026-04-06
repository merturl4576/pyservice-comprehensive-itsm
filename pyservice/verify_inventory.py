import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pyservice.settings")
django.setup()

from cmdb.models import Asset, AssetInventory, User
from django.test import RequestFactory
from cmdb.views import asset_create
from django.urls import reverse
from django.contrib.messages.storage.fallback import FallbackStorage

def setup():
    # Ensure Other exists and has 0 quantity
    other_inv, _ = AssetInventory.objects.get_or_create(item_type='other', defaults={'quantity': 0, 'display_name': 'Other'})
    other_inv.quantity = 0
    other_inv.save()
    
    # Ensure Laptop exists and has stock
    laptop_inv, _ = AssetInventory.objects.get_or_create(item_type='laptop', defaults={'quantity': 10, 'display_name': 'Laptop'})
    laptop_inv.quantity = 5
    laptop_inv.save()
    
    # Create a user
    user, _ = User.objects.get_or_create(username='test_user', role='staff')
    return user

def test_inventory_logic():
    print("\n--- Testing Inventory Logic ---")
    user = setup()
    factory = RequestFactory()
    
    # 1. Test "Other" Asset Creation
    print("Testing 'Other' asset creation (Expect: Under Review)")
    request = factory.post(reverse('asset_create'), {
        'name': 'My Weird Device',
        'asset_type': 'other',
        'notes': 'Need this specific thing',
    })
    request.user = user
    setattr(request, 'session', 'session')
    setattr(request, '_messages', FallbackStorage(request))
    
    response = asset_create(request)
    
    asset = Asset.objects.filter(name='My Weird Device').first()
    if asset:
        print(f"Asset created: {asset.name}, Type: {asset.asset_type}, Status: {asset.status}")
        if asset.status == 'under_review':
            print("SUCCESS: 'Other' asset is under review.")
        else:
            print(f"FAILURE: 'Other' asset status is {asset.status}")
    else:
        print("FAILURE: Asset not created.")

    # 2. Test "Laptop" Asset Creation (In Stock)
    print("\nTesting 'Laptop' asset creation (Expect: Assigned)")
    request = factory.post(reverse('asset_create'), {
        'name': 'My Laptop',
        'asset_type': 'laptop',
    })
    request.user = user
    setattr(request, 'session', 'session')
    setattr(request, '_messages', FallbackStorage(request))
    
    response = asset_create(request)
    
    asset = Asset.objects.filter(name='My Laptop').first()
    if asset:
        print(f"Asset created: {asset.name}, Type: {asset.asset_type}, Status: {asset.status}")
        if asset.status == 'assigned':
            print("SUCCESS: Laptop is assigned.")
        else:
            print(f"FAILURE: Laptop status is {asset.status}")
    else:
        print("FAILURE: Asset not created.")

if __name__ == "__main__":
    try:
        test_inventory_logic()
    except Exception as e:
        print(f"Error: {e}")
