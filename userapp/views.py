from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date
from django.db.models import Count

from .forms import QuestionForm
from .models import Question, Answer
from .models import Question, Tag

def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save()

            # Handle tags manually from POST (Tagify sends comma-separated)
            tags_raw = request.POST.get('tags', '')
            import json
            try:
                tags_list = [tag['value'] for tag in json.loads(tags_raw)]
                for tag_name in tags_list:
                    tag_obj, created = Tag.objects.get_or_create(name=tag_name.strip())
                    question.tags.add(tag_obj)
            except json.JSONDecodeError:
                pass

            return redirect('question_detail', question_id=question.id)
    else:
        form = QuestionForm()

    return render(request, 'ask_question.html', {'form': form})

# -----------------------------
# User Authentication Views
# -----------------------------

def register_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})

        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already exists'})

        user = User.objects.create_user(username=username, email=email, password=password1)
        auth_login(request, user)
        messages.success(request, f'Registration successful! Welcome, {username}')
        return redirect('login_user')  # Change 'dashboard' to your actual dashboard view name

    return render(request, 'register.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'login.html')

    return render(request, 'login.html')


def logout_user(request):
    auth_logout(request)
    return redirect('login_user')


# -----------------------------
# Home and Question Views
# -----------------------------


def home(request):
    filter_by = request.GET.get('filter')

    if filter_by == 'unanswered':
        questions = Question.objects.annotate(num_answers=Count('answers')) \
                                     .filter(num_answers=0).order_by('-id')
    else:
        questions = Question.objects.all().order_by('-id')

    tags = Tag.objects.values_list('name', flat=True).distinct()

    context = {
        'questions': questions,
        'tags': tags,
        'page_range': range(1, 8),
        'current_page': 1,
        'today_date': date.today().strftime("%B %d, %Y"),
    }
    return render(request, 'home.html', context)


def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    # Handle answer submission
    if request.method == "POST":
        content = request.POST.get("answer")
        if content:
            Answer.objects.create(question=question, content=content)
            return redirect('question_detail', question_id=question.id)

    answers = question.answers.all()
    context = {
        'question': question,
        'answers': answers
    }
    return render(request, 'screen3.html', context)




