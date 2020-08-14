from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
from .models import Event, Payment
from django.utils import  dateformat
from .forms import PaymentForm
import datetime


def test_login():
    password = "123qw456"
    user = User.objects.create_user("Test", "Test@Test.ru", password)

    return user, password

class IndexTests(TestCase):
    def test_index_without_login(self):
        response = self.client.get(reverse('index'))
        self.assertContains(response, reverse('docs'))
        self.assertContains(response,reverse('signup'))
        self.assertContains(response, reverse('login'))

    def test_index_with_login(self):
        user, password = test_login()
        self.client.post("/accounts/login/", {"username": user.username, "password": password})
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
        self.assertContains(response, reverse('events'))


class EventListViewTests(TestCase):
    def test_no_events(self):
        user, password = test_login()
        self.client.post("/accounts/login/", {"username": user.username, "password": password})
        response = self.client.get(reverse("events"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "нет событий")
        self.assertQuerysetEqual(response.context["events_list"], [])

    def test_with_events(self):
        user, password = test_login()
        Event.objects.create(name="Событие 1", description="Описание события 1", creation_date=datetime.datetime.now(),
                             event_date="2020-05-01", creator=user, uni_id=1)
        Event.objects.create(name="Событие 2", description="Описание события 2",
                             creation_date=datetime.datetime.now(),
                             event_date="2020-05-02", creator=user, uni_id=2)
        events = Event.objects.filter(creator=user)
        self.client.post("/accounts/login/", {"username": user.username, "password": password})
        response = self.client.get(reverse("events"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Событие 1")
        self.assertQuerysetEqual(list(response.context["events_list"]), [repr(event) for event in events])


class EventViewTests(TestCase):
    def test_events_url(self):
        user, password = test_login()
        self.client.post("/accounts/login/", {"username": user.username, "password": password})
        event = Event.objects.create(name="Событие 1", description="Описание события 1",
                                     creation_date=datetime.datetime.now(),
                                     event_date="2020-05-01", creator=user, uni_id=1)
        response = self.client.get(reverse("events"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["events_list"], [repr(event)])
        self.assertContains(response, reverse("event", kwargs={"uni_id": event.uni_id}))

    def test_event_detail(self):
        user, password = test_login()
        self.client.post("/accounts/login/", {"username": user.username, "password": password})
        event_create_date = datetime.datetime.now()
        event = Event.objects.create(name="Событие 1", description="Описание события 1",
                                     creation_date=event_create_date,
                                     event_date="2020-05-01", creator=user, uni_id=1)
        response = self.client.get(reverse("event", kwargs={"uni_id": event.uni_id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["event"], event)
        self.assertContains(response, "Дата события: 1 мая 2020 г.")
        #self.assertContains(response, "Дата создания: {date} г.".format(date=dateformat.format(event.creation_date, "j E Y")))

class EventCreateTests(TestCase):
    def test_custom_create(self):
        user, password = test_login()
        self.client.post("/accounts/login/", {"username": user.username, "password": password})
        name = 'Новое событие'
        desc = 'Описание нового события'
        date = '20.05.2020'
        self.client.post(reverse('create_event'), {'name': name, 'description': desc, 'event_date': date})
        event = Event.objects.get(name=name)
        self.assertEqual(event.name, name)
        self.assertEqual(event.description, desc)
        self.assertEqual(event.event_date.strftime('%d.%m.%Y'), date)
        self.assertEqual(event.creation_date.strftime('%d.%m.%Y'), datetime.datetime.now().strftime('%d.%m.%Y'))
        self.assertEqual(event.creator, user.username)


class EventDeleteTests(TestCase):
    def test_delete_event(self):
        user, password = test_login()
        self.client.post("/accounts/login/", {"username": user.username, "password": password})
        event = Event.objects.create(name="Событие 1", description="Описание события 1",
                                     creation_date=datetime.datetime.now(),
                                     event_date="2020-05-01", creator=user, uni_id=1)
        response = self.client.get(reverse("delete_event", kwargs={'uni_id': event.uni_id}))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
        self.assertNotContains(response, reverse("event", kwargs={"uni_id": event.uni_id}))

class PaymentListTects(TestCase):
    def test_empty_payment_list(self):
        user, password = test_login()
        self.client.post("/accounts/login/", {"username": user.username, "password": password})
        name = 'Новое событие'
        desc = 'Описание нового события'
        date = '20.05.2020'
        self.client.post(reverse('create_event'), {'name': name, 'description': desc, 'event_date': date})
        event = Event.objects.get(name=name)
        response = self.client.get(reverse("event", kwargs={"uni_id": event.uni_id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["payments"]), [])

    def test_payment_list(self):
        user, password = test_login()
        self.client.post("/accounts/login/", {"username": user.username, "password": password})
        name = 'Новое событие'
        desc = 'Описание нового события'
        date = '20.05.2020'
        self.client.post(reverse('create_event'), {'name': name, 'description': desc, 'event_date': date})
        event = Event.objects.get(name=name)

        Payment.objects.create(name="Платёж 1", description="Покупали кофе", participants="Андрей", creditor="Ярослав",
                               total_loan_sum=550.00, creator=user.username, event=event,
                               payment_date=datetime.datetime.strptime("01.06.2020","%d.%m.%Y"))
        Payment.objects.create(name="Платёж 2", description="Покупали чай", participants="Ярослав", creditor="Андрей",
                               total_loan_sum=1450.00, creator=user.username, event=event,
                               payment_date=datetime.datetime.strptime("02.06.2020", "%d.%m.%Y"))
        payments = Payment.objects.filter(event__uni_id=event.uni_id)
        response = self.client.get(reverse("event", kwargs={"uni_id": event.uni_id}))
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(list(response.context["payments"]), [payments])

class PaymentCreateTests(TestCase):
    def test_custom_payment_create(self):
        user, password = test_login()
        self.client.post("/accounts/login/", {"username": user.username, "password": password})
        event = Event.objects.create(name="Событие 1", description="Описание события 1",
                                     creation_date=datetime.datetime.now(),
                                     event_date="2020-05-01", creator=user, uni_id=1)
        event = Event.objects.get(name="Событие 1")
        name = "Платёж 1"
        desc = "Покупали кофе"
        part = "Андрей"
        creditor = "Ярослав"
        summ = 550.00
        creator = user.username
        payment_date = datetime.datetime.strptime("01.06.2020", "%d.%m.%Y")
        self.client.post(reverse('create_payment',kwargs={'pk':event.uni_id}),{'name':name, 'description':desc,
                            'participants':part, 'creditor':creditor,
                               'total_loan_sum':summ, 'payment_date':payment_date.strftime('%d.%m.%Y')})
        payment = Payment.objects.get(name=name, event=event)
        self.assertEqual(payment.name,name)
        self.assertEqual(payment.description,desc)
        self.assertEqual(payment.participants,part)
        self.assertEqual(payment.creditor, creditor)
        self.assertEqual(payment.event, event)
        self.assertEqual(payment.total_loan_sum, summ)
        self.assertEqual(payment.creator, creator)
        self.assertEqual(payment.payment_date.strftime('%d.%m.%Y'), payment_date.strftime('%d.%m.%Y'))

    def test_custom_payment_on_eventpage(self):
        user, password = test_login()
        self.client.post("/accounts/login/", {"username": user.username, "password": password})
        event = Event.objects.create(name="Событие 1", description="Описание события 1",
                                     creation_date=datetime.datetime.now(),
                                     event_date="2020-05-01", creator=user, uni_id=1)
        event = Event.objects.get(name="Событие 1")
        name = "Платёж 1"
        desc = "Покупали кофе"
        part = "Андрей"
        creditor = "Ярослав"
        summ = 550.00
        creator = user.username
        payment_date = datetime.datetime.strptime("01.06.2020", "%d.%m.%Y")
        Payment.objects.create(name=name, description=desc, participants=part, creditor=creditor,
                               total_loan_sum=summ, creator=creator, event=event,
                               payment_date=payment_date)
        payment = Payment.objects.get(name=name, event=event)
        response = self.client.get(reverse("event", kwargs={"uni_id": event.uni_id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, name)
        #self.assertContains(response, desc)
        self.assertContains(response, part)
        self.assertContains(response, creditor)
        self.assertContains(response, str(summ).replace('.',','))
        self.assertContains(response, creator)
        self.assertContains(response, "{date}".format(date=dateformat.format(payment_date, "j E Y")))

class PaymentDeleteTests(TestCase):
    def test_delete_event(self):
        user, password = test_login()
        self.client.post("/accounts/login/", {"username": user.username, "password": password})
        event = Event.objects.create(name="Событие 1", description="Описание события 1",
                                     creation_date=datetime.datetime.now(),
                                     event_date="2020-05-01", creator=user, uni_id=1)
        payment1 = Payment.objects.create(name="Платёж 2", description="Покупали чай", participants="Ярослав", creditor="Андрей",
                               total_loan_sum=1450.00, creator=user.username, event=event,
                               payment_date=datetime.datetime.strptime("02.06.2020", "%d.%m.%Y"))
        payment2 = Payment.objects.create(name="Платёж 1", description="Покупали кофе", participants="Андрей", creditor="Ярослав",
                               total_loan_sum=550.00, creator=user.username, event=event,
                               payment_date=datetime.datetime.strptime("01.06.2020", "%d.%m.%Y"))
        response = self.client.get(reverse("delete_payment", kwargs={'pk': payment1.pk}))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
        self.assertNotContains(response, payment1.name)
        self.assertContains(response, payment2.name)
