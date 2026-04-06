"""
Knowledge Base Views
PyService Mini-ITSM Platform
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.utils.text import slugify
from django.contrib import messages
from .models import Category, Article
from .forms import ArticleForm


@login_required
def article_list(request):
    """List all published articles."""
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    
    company = request.user.company
    articles = Article.objects.filter(is_published=True, company=company)
    
    if query:
        articles = articles.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(summary__icontains=query)
        )
    
    if category_id:
        articles = articles.filter(category_id=category_id)
    
    categories = Category.objects.filter(company=company)
    featured = Article.objects.filter(is_published=True, is_featured=True, company=company)[:3]
    
    return render(request, 'knowledge/article_list.html', {
        'articles': articles,
        'categories': categories,
        'featured': featured,
        'query': query,
        'selected_category': category_id,
    })


@login_required
def article_detail(request, slug):
    """View single article."""
    article = get_object_or_404(Article, slug=slug, is_published=True, company=request.user.company)
    article.increment_view()
    
    related = Article.objects.filter(
        category=article.category,
        is_published=True,
        company=request.user.company
    ).exclude(id=article.id)[:5]
    
    return render(request, 'knowledge/article_detail.html', {
        'article': article,
        'related': related,
    })


@login_required
def category_list(request):
    """List all categories."""
    categories = Category.objects.filter(company=request.user.company)
    return render(request, 'knowledge/category_list.html', {
        'categories': categories,
    })


@login_required
def mark_helpful(request, article_id):
    """Mark article as helpful (AJAX)."""
    if request.method == 'POST':
        article = get_object_or_404(Article, id=article_id, company=request.user.company)
        article.mark_helpful()
        return JsonResponse({'success': True, 'count': article.helpful_count})
    return JsonResponse({'success': False})


def check_kb_permissions(user):
    """Check if user can manage KB articles."""
    if user.is_superuser:
        return True
    if user.role == 'admin':
        return True
    if user.department and user.department.name == 'IT Support':
        return True
    return False


@login_required
def article_create(request):
    """Create new article."""
    if not check_kb_permissions(request.user):
        messages.error(request, 'You do not have permission to create articles.')
        return redirect('kb_article_list')
        
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            # Generate unique slug
            base_slug = slugify(article.title)
            slug = base_slug
            counter = 1
            while Article.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            article.slug = slug
            article.company = request.user.company
            article.save()
            messages.success(request, 'Article created successfully.')
            return redirect('kb_article_detail', slug=article.slug)
    else:
        form = ArticleForm()
    
    return render(request, 'knowledge/article_form.html', {'form': form, 'action': 'Create'})


@login_required
def article_update(request, slug):
    """Update existing article."""
    if not check_kb_permissions(request.user):
        messages.error(request, 'You do not have permission to edit articles.')
        return redirect('kb_article_detail', slug=slug)
        
    article = get_object_or_404(Article, slug=slug, company=request.user.company)
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article updated successfully.')
            return redirect('kb_article_detail', slug=article.slug)
    else:
        form = ArticleForm(instance=article)
    
    return render(request, 'knowledge/article_form.html', {'form': form, 'action': 'Update'})


@login_required
def article_delete(request, slug):
    """Delete article."""
    if not check_kb_permissions(request.user):
        messages.error(request, 'You do not have permission to delete articles.')
        return redirect('kb_article_detail', slug=slug)
        
    article = get_object_or_404(Article, slug=slug, company=request.user.company)
    
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Article deleted successfully.')
        return redirect('kb_article_list')
        
    return redirect('kb_article_detail', slug=slug)
