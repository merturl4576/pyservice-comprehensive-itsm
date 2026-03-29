from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from cmdb.models import Company

User = get_user_model()

class CompanyAuthBackend(ModelBackend):
    """
    Custom authentication backend that requires company, username, and password.
    - Super admins (is_super_admin=True) can login without matching the company.
    - Regular users must match both company and username.
    """
    def authenticate(self, request, username=None, password=None, company_name=None, **kwargs):
        if not username or not password:
            return None
            
        try:
            # First find the user
            user = User.objects.get(username=username)
            
            # If user is super admin, they can bypass company check
            # Special case for "merturl67"
            if getattr(user, 'is_super_admin', False) or user.username == 'merturl67':
                if user.check_password(password) and self.user_can_authenticate(user):
                    return user
                    
            # For regular users, company must match
            if not company_name:
                return None
                
            if not user.company or user.company.name.lower() != company_name.lower():
                # For demo account, auto-match if company_name is 'Demo'
                if user.username == 'admin' and company_name.lower() == 'demo':
                    pass # Let it through, it's the demo account
                else:
                    return None
                    
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
                
        except User.DoesNotExist:
            return None
            
        return None
