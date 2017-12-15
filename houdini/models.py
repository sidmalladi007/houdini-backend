from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
from django.contrib.auth.models import User

class Consumer(models.Model):
    city = models.CharField(max_length=100, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    class Meta:
        ordering = ('-created_at',)


class Pro(models.Model):
    business_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=20)
    phone_number = PhoneNumberField()
    description = models.TextField()
    services = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name

    class Meta:
        ordering = ('-created_at',)


class Favorite(models.Model):
    pro = models.ForeignKey(Pro, related_name='favorited_by', on_delete=models.CASCADE)
    consumer = models.ForeignKey(Consumer, related_name='favorites', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.consumer.user.first_name + " " + self.consumer.user.last_name + " likes " + self.pro.business_name

    class Meta:
        ordering = ('-created_at',)


class Project(models.Model):
    project_name = models.CharField(max_length=100)
    project_description = models.TextField()
    completed = models.BooleanField(default=False)
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_name

    class Meta:
        ordering = ('-created_at',)

class Conversation(models.Model):
    pro = models.ForeignKey(Pro, related_name='conversations', on_delete=models.CASCADE)
    consumer = models.ForeignKey(Consumer, related_name='conversations', on_delete=models.CASCADE)
    status = models.CharField(default='lead', max_length=100)
    active = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pro.business_name + " <> " + self.consumer.user.first_name + " " + self.consumer.user.last_name

    class Meta:
        ordering = ('-created_at',)


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ('-created_at',)


class Scheduling(models.Model):
    name = models.CharField(max_length=100)
    expected_duration = models.CharField(max_length=100)
    time_1 = models.DateTimeField()
    time_2 = models.DateTimeField()
    time_3 = models.DateTimeField()
    conversation = models.ForeignKey(Conversation, related_name='schedules', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created_at',)


class ConfirmedAppointment(models.Model):
    time = models.DateTimeField()
    scheduling = models.OneToOneField(Scheduling, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, related_name='confirmed_appointment', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.time

    class Meta:
        ordering = ('-created_at',)


class Quote(models.Model):
    quoted_price = models.DecimalField(max_digits=8, decimal_places=2)
    conversation = models.ForeignKey(Conversation, related_name='quotes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.quoted_price

    class Meta:
        ordering = ('-created_at',)


class ConfirmedPrice(models.Model):
    confirmed_price = models.DecimalField(max_digits=8, decimal_places=2)
    quote = models.OneToOneField(Quote, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, related_name='confirmed_price', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.confirmed_price

    class Meta:
        ordering = ('-created_at',)


class StripeCustomer(models.Model):
    stripe_id = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
