import datetime
from math import ceil
from django.contrib import auth
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Payment, Event
from .forms import PaymentForm, EventForm, MyForm
from random import randint
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings


def index(request):
    """
    Функция, возвращающая главную страницу, в случае если вы не авторизированы, иначе возвращает страницу событий
    """
    if request.user.is_authenticated:
        return redirect(reverse('events'))
    return render(request, 'pages/index.html')


def docs(request):
    """
    Функция документации
    """
    return render(request,'build/html/index.html')


def signin(request):
    """
    Функция авторизации
    """
    username = request.POST.get('login')
    password = request.POST.get('password')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect(reverse('events'))
        else:
            return render(request, 'registration/login.html')
    else:
        return render(request, 'registration/login.html')


def logout(request):
    """
    Функция выхода
    """
    auth.logout(request)
    return redirect(reverse('index'))


def signup(request):
    """
    Функция регистрации
    """
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            return redirect(reverse('login'))
        else:
            return render(request, 'registration/register.html')
    else:
        return render(request, 'registration/register.html')


@login_required
def create_event(request):
    """
    Функция создания события
    """
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.uni_id = randint(0, 1000)
            event.save()
            return redirect(reverse('event', args=[event.uni_id]))
    return render(request, 'pages/add_event.html')


@login_required
def delete_event(request, uni_id):
    """
    Функция удаления события
    """
    event = Event.objects.filter(uni_id=uni_id)
    event.delete()
    return redirect('/events/')


@login_required
def create_payment(request, pk):
    """
    Функция создания платежа
    """
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        event = Event.objects.filter(uni_id=pk)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.event = event[0]
            payment.creator = request.user
            payment.save()
            return redirect(reverse('event', args=[payment.event.uni_id]))
    else:
        form = PaymentForm()
    return render(request, 'pages/add_payment.html', {'form': form})


@login_required
def delete_payment(request, pk):
    """
    Страница удаления платежа
    """
    payment = Payment.objects.filter(id=pk)
    event = payment[0].event
    if request.method == 'GET':
        payment.delete()
    return redirect(reverse('event', kwargs={'uni_id': event.uni_id}))


@login_required
def events_list(request, events=0):
    """
    Функция возвращающая список событий пользователя
    """
    if events == 0:
        events = Event.objects.filter(creator=request.user).order_by('id')
    return render(request, 'pages/events.html', {'events_list': reversed(events)})


def view_event(request, uni_id, payments=0):
    """
    Функция просмотра события
    """
    event = Event.objects.filter(uni_id=uni_id)
    if payments == 0:
        payments = Payment.objects.filter(event__uni_id=event[0].uni_id).order_by('id')
    for payment in payments:
        if payment.percents_type == 1 or payment.period == 0 or payment.percents == 0:
            payment.sum_with_percents = payment.total_loan_sum
        else:
            delta = (datetime.date.today() - payment.payment_date).days // payment.period
            if payment.percents_type == 2:
                payment.sum_with_percents = payment.total_loan_sum * (1 + payment.percents * delta/100)
            if payment.percents_type == 3:
                payment.sum_with_percents = payment.total_loan_sum * ((1 + 0.01 * payment.percents) ** delta)
        payment.sum_with_percents = ceil(payment.sum_with_percents)
    return render(request, 'pages/event.html', {'event': event[0], 'payments': reversed(payments)})


def event_date_sort(request):
    """
    Функция сортировки событий по их дате
    """
    events = Event.objects.filter(creator=request.user).order_by('event_date')
    return events_list(request, events)


def pay_date_sort(request, uni_id):
    """
    Функция сортировки платежей по их дате
    """
    event = Event.objects.filter(uni_id=uni_id)
    payments = Payment.objects.filter(event__uni_id=event[0].uni_id).order_by('payment_date')
    return view_event(request, event[0].uni_id, payments)


def pay_sum_sort(request, uni_id):
    """
    Функция сортировки платежей по их сумме
    """
    event = Event.objects.filter(uni_id=uni_id)
    payments = Payment.objects.filter(event__uni_id=event[0].uni_id).order_by('total_loan_sum')
    return view_event(request, event[0].uni_id, payments)
