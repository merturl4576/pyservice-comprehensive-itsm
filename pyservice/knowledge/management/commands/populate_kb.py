from django.core.management.base import BaseCommand
from django.utils.text import slugify
from knowledge.models import Category, Article
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the knowledge base with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating Knowledge Base...')

        # get admin user
        admin = User.objects.filter(is_superuser=True).first()
        if not admin:
            admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin')

        # Categories
        categories_data = [
            {'name': 'Hardware', 'icon': 'bi-laptop', 'desc': 'Hardware troubleshooting and guides'},
            {'name': 'Software', 'icon': 'bi-code-square', 'desc': 'Software installation and usage'},
            {'name': 'Network', 'icon': 'bi-wifi', 'desc': 'Network connectivity and VPN'},
            {'name': 'Security', 'icon': 'bi-shield-lock', 'desc': 'Security policies and best practices'},
        ]

        categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['desc'], 'icon': cat_data['icon']}
            )
            categories[cat_data['name']] = cat

        # Articles
        articles_data = [
            {
                'title': 'How to Request a New Laptop',
                'category': 'Hardware',
                'summary': 'Step-by-step guide to requesting a new laptop from IT.',
                'content': """
<h3>Laptop Request Process</h3>
<p>If your current laptop is outdated or broken, you can request a replacement through the Self-Service Portal.</p>
<ol>
    <li>Go to <strong>Service Requests</strong> in the sidebar.</li>
    <li>Click on <strong>New Request</strong>.</li>
    <li>Select <strong>Hardware Request</strong> from the dropdown.</li>
    <li>Fill in the justification field explaining why a replacement is needed.</li>
</ol>
<div class="alert alert-info">
    <strong>Note:</strong> Requests need manager approval before they are processed by IT.
</div>
                """,
                'is_featured': True
            },
            {
                'title': 'VPN Connection Issues',
                'category': 'Network',
                'summary': 'Common solutions for VPN connectivity problems.',
                'content': """
<h3>Troubleshooting VPN</h3>
<p>If you are unable to connect to the corporate VPN, try the following steps:</p>
<ul>
    <li>Check your internet connection.</li>
    <li>Verify your MFA token code is correct.</li>
    <li>Restart the VPN client.</li>
</ul>
<p>If the issue persists, please submit an <strong>Incident</strong> ticket with the error code displayed.</p>
                """,
                'is_featured': True
            },
            {
                'title': 'Password Reset Guidelines',
                'category': 'Security',
                'summary': 'How to reset your password and security policies.',
                'content': """
<h3>Password Policy</h3>
<p>Passwords must be updated every 90 days. A valid password must contain:</p>
<ul>
    <li>At least 12 characters</li>
    <li>One uppercase letter</li>
    <li>One number</li>
    <li>One special character</li>
</ul>
<p>To reset your password, click on your profile icon and select <strong>Role: Admin</strong> > <strong>Change Password</strong> (if applicable) or contact the Service Desk.</p>
                """,
                'is_featured': False
            },
             {
                'title': 'Installing Office 365',
                'category': 'Software',
                'summary': 'Guide to installing Office 365 apps on your workstation.',
                'content': """
<h3>Office 365 Installation</h3>
<p>All employees are licensed for Office 365. To install:</p>
<ol>
    <li>Login to <a href="https://portal.office.com" target="_blank">portal.office.com</a> with your company email.</li>
    <li>Click "Install Office" in the top right corner.</li>
    <li>Run the downloaded installer.</li>
</ol>
                """,
                'is_featured': False
            }
        ]

        for art_data in articles_data:
            cat = categories[art_data['category']]
            slug = slugify(art_data['title'])
            
            Article.objects.get_or_create(
                slug=slug,
                defaults={
                    'title': art_data['title'],
                    'category': cat,
                    'summary': art_data['summary'],
                    'content': art_data['content'],
                    'author': admin,
                    'is_published': True,
                    'is_featured': art_data['is_featured']
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated Knowledge Base'))
