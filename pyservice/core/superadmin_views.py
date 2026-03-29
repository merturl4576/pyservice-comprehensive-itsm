from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count
from cmdb.models import Company, User, Department

def is_super_admin(user):
    return getattr(user, 'is_super_admin', False)

@login_required
@user_passes_test(is_super_admin)
def superadmin_dashboard(request):
    """Dashboard for the global super admin to manage companies."""
    companies = Company.objects.annotate(
        user_count=Count('users', distinct=True)
    ).order_by('-created_at')
    
    context = {
        'companies': companies,
        'total_companies': companies.count(),
        'total_users': User.objects.count()
    }
    return render(request, 'superadmin/dashboard.html', context)

@login_required
@user_passes_test(is_super_admin)
def company_create(request):
    """Create a new company tenant."""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()

        if name:
            if Company.objects.filter(name__iexact=name).exists():
                messages.error(request, 'A company with this name already exists.')
            else:
                company = Company.objects.create(
                    name=name
                )
                
                # Create a default "IT Department" for the new company
                Department.objects.create(
                    name='IT Department',
                    code='IT_DEPT',
                    description='Central IT Support for ' + name,
                    company=company
                )
                
                messages.success(request, f'Company {name} created successfully.')
                return redirect('superadmin_company_detail', pk=company.pk)
        else:
            messages.error(request, 'Company name is required.')
    
    return render(request, 'superadmin/company_form.html')

@login_required
@user_passes_test(is_super_admin)
def company_detail(request, pk):
    """View details of a company and its admins."""
    company = get_object_or_404(Company, pk=pk)
    admins = User.objects.filter(company=company, role='admin')
    all_users = User.objects.filter(company=company).order_by('-date_joined')[:10]
    
    if request.method == 'POST':
        # Create a new admin for this company
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        
        if username and email and password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists globally.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already in use.')
            else:
                admin_user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    role='admin',
                    company=company
                )
                messages.success(request, f'Admin user {username} created for {company.name}.')
                return redirect('superadmin_company_detail', pk=company.pk)
        else:
            messages.error(request, 'All fields are required to create an admin.')
            
    context = {
        'company': company,
        'admins': admins,
        'recent_users': all_users,
        'user_count': User.objects.filter(company=company).count()
    }
    return render(request, 'superadmin/company_detail.html', context)
