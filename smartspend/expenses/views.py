from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Expense, Budget, UserProfile

def login_view(request):
    error = ''
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            error = 'Invalid username or password'
    return render(request, 'login.html', {'error': error})

def register_view(request):
    error = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            error = 'Username already taken'
        else:
            user = User.objects.create_user(username=username, password=password)
            user.is_active = False
            user.save()
            UserProfile.objects.create(user=user, status='pending')
            return render(request, 'register.html', {'pending': True})
    return render(request, 'register.html', {'error': error})

@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user)
    total = sum(e.amount for e in expenses)
    budget, _ = Budget.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        budget.monthly_limit = request.POST['monthly_limit']
        budget.save()
    budget_alert = ''
    if budget.monthly_limit and float(budget.monthly_limit) > 0:
        percent = (float(total) / float(budget.monthly_limit)) * 100
        if percent >= 100:
            budget_alert = 'danger'
        elif percent >= 90:
            budget_alert = 'critical'
        elif percent >= 80:
            budget_alert = 'warning'

    ai_insight = ''
    if expenses:
        category_totals = {}
        for e in expenses:
            cat = e.category
            category_totals[cat] = category_totals.get(cat, 0) + float(e.amount)
        top_category = max(category_totals, key=category_totals.get)
        top_amount = category_totals[top_category]
        top_percent = round((top_amount / float(total)) * 100)
        tips = {
            'Food': 'Try cooking at home more often to save money.',
            'Travel': 'Consider public transport or carpooling to cut travel costs.',
            'Education': 'Great investment! Look for free online resources too.',
            'Bills': 'Review subscriptions and cancel ones you rarely use.',
            'Entertainment': 'Look for free or discounted entertainment options.',
            'Other': 'Track miscellaneous expenses carefully to find patterns.',
        }
        tip = tips.get(top_category, 'Try to save at least 20% of your monthly income.')
        ai_insight = f"Your highest spending is on {top_category} — ₹{round(top_amount, 2)} ({top_percent}% of total). 💡 Tip: {tip}"

    remaining = float(budget.monthly_limit) - float(total) if budget.monthly_limit else 0

    return render(request, 'dashboard.html', {
        'expenses': expenses,
        'total': total,
        'budget': budget,
        'budget_alert': budget_alert,
        'ai_insight': ai_insight,
        'remaining': remaining,
    })

@login_required
def add_expense(request):
    budget, _ = Budget.objects.get_or_create(user=request.user)
    expenses = Expense.objects.filter(user=request.user)
    total = sum(e.amount for e in expenses)

    budget_exceeded = False
    budget_limit = None
    if budget.monthly_limit:
        try:
            budget_limit = float(budget.monthly_limit)
        except (TypeError, ValueError):
            budget_limit = None
        if budget_limit is not None and budget_limit > 0:
            if float(total) >= budget_limit:
                budget_exceeded = True

    if request.method == 'POST':
        try:
            new_amount = float(request.POST.get('amount', 0))
        except (TypeError, ValueError):
            new_amount = 0

        if budget_limit is not None and budget_limit > 0 and (float(total) + new_amount) > budget_limit:
            budget_exceeded = True

        if budget_exceeded:
            return render(request, 'add_expense.html', {
                'budget_exceeded': True,
                'budget': budget,
                'total': total
            })
        Expense.objects.create(
            user=request.user,
            title=request.POST['title'],
            amount=request.POST['amount'],
            category=request.POST['category'],
            date=request.POST['date'],
            note=request.POST.get('note', '')
        )
        return redirect('dashboard')

    return render(request, 'add_expense.html', {
        'budget_exceeded': budget_exceeded,
        'budget': budget,
        'total': total
    })

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def delete_expense(request, id):
    expense = Expense.objects.get(id=id, user=request.user)
    expense.delete()
    return redirect('dashboard')

@login_required
def edit_expense(request, id):
    expense = Expense.objects.get(id=id, user=request.user)
    if request.method == 'POST':
        expense.title = request.POST['title']
        expense.amount = request.POST['amount']
        expense.category = request.POST['category']
        expense.date = request.POST['date']
        expense.note = request.POST.get('note', '')
        expense.save()
        return redirect('dashboard')
    return render(request, 'edit_expense.html', {'expense': expense})

@login_required
def ai_summary(request):
    expenses = Expense.objects.filter(user=request.user)
    if not expenses:
        summary = "No expenses found. Add some expenses first!"
        return render(request, 'ai_summary.html', {'summary': summary})

    category_totals = {}
    for e in expenses:
        cat = e.category
        if cat in category_totals:
            category_totals[cat] += float(e.amount)
        else:
            category_totals[cat] = float(e.amount)

    total = sum(category_totals.values())
    top_category = max(category_totals, key=category_totals.get)
    top_amount = category_totals[top_category]
    top_percent = round((top_amount / total) * 100)

    tips = {
        'Food': 'Try cooking at home more often to reduce food expenses.',
        'Travel': 'Consider using public transport or carpooling to save on travel costs.',
        'Education': 'Great investment! Look for free online resources to supplement learning.',
        'Bills': 'Review your subscriptions and cancel ones you rarely use.',
        'Entertainment': 'Look for free or discounted entertainment options in your area.',
        'Other': 'Track miscellaneous expenses carefully to identify patterns.',
    }
    tip = tips.get(top_category, 'Try to save at least 20% of your monthly income.')

    summary = f"""📊 Spending Analysis for {request.user.username.capitalize()}:

You have recorded {expenses.count()} expenses with a total spending of ₹{round(total, 2)}.

🔴 Highest Spending Category: {top_category} — ₹{round(top_amount, 2)} ({top_percent}% of total spending).

📂 Category Breakdown:
"""
    for cat, amt in category_totals.items():
        percent = round((amt / total) * 100)
        summary += f"• {cat}: ₹{round(amt, 2)} ({percent}%)\n"

    summary += f"\n💡 Smart Tip: {tip}"

    return render(request, 'ai_summary.html', {'summary': summary})  
# yaha se change kiya hai~>

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required(login_url='/login/')
def manage_panel(request):
    pending = UserProfile.objects.filter(status='pending').select_related('user')
    approved = UserProfile.objects.filter(status='approved').select_related('user')
    declined = UserProfile.objects.filter(status='declined').select_related('user')

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        try:
            profile = UserProfile.objects.get(user__id=user_id)
            if action == 'approve':
                profile.status = 'approved'
                profile.save()
                profile.user.is_active = True
                profile.user.save()
            elif action == 'decline':
                profile.status = 'declined'
                profile.save()
                profile.user.is_active = False
                profile.user.save()
        except UserProfile.DoesNotExist:
            pass
        return redirect('manage_panel')

    return render(request, 'manage_panel.html', {
        'pending': pending,
        'approved': approved,
        'declined': declined,
    })