from django.core.management.base import BaseCommand
from cmdb.models import AssetInventory
import random

class Command(BaseCommand):
    help = 'Populates the asset inventory with random quantities'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating Asset Inventory...')

        # Standard items to populate
        items = [
            ('laptop', 'Laptop'),
            ('desktop', 'Desktop'),
            ('monitor', 'Monitor'),
            ('phone', 'Phone'),
            ('printer', 'Printer'),
            ('network', 'Network Equipment'),
            ('software', 'Software License'),
        ]

        for item_type, display_name in items:
            # Random quantity between 5 and 50
            qty = random.randint(5, 50)
            
            obj, created = AssetInventory.objects.get_or_create(
                item_type=item_type,
                defaults={
                    'display_name': display_name,
                    'quantity': qty
                }
            )
            
            if not created:
                # Update existing if needed (optional, here we just ensure it exists)
                # obj.quantity = qty 
                # obj.save()
                self.stdout.write(f'Updated {display_name}: {obj.quantity}')
            else:
                self.stdout.write(f'Created {display_name}: {obj.quantity}')

        # Ensure 'other' exists with 0 quantity
        obj, created = AssetInventory.objects.get_or_create(
            item_type='other',
            defaults={
                'display_name': 'Other',
                'quantity': 0
            }
        )
        if not created:
            obj.quantity = 0 # Force 'Other' to 0 to trigger manual approval
            obj.save()
        
        self.stdout.write(self.style.SUCCESS(f'Successfully populated Asset Inventory. "Other" set to 0.'))
