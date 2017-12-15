from django.shortcuts import render

# Create your views here.
from houdini.models import User, Consumer, Pro, Favorite, Project, Conversation, Message, Scheduling, ConfirmedAppointment, Quote, ConfirmedPrice
from houdini.serializers import UserSerializer, ConsumerSerializer, ProSerializer, FavoriteSerializer, ProjectSerializer, ConversationSerializer, MessageSerializer, SchedulingSerializer, ConfirmedAppointmentSerializer, QuoteSerializer, ConfirmedPriceSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from houdini.permissions import IsOwnerOrNotAllowed
from django.http import JsonResponse
import requests
from rest_framework.decorators import api_view
import stripe
import os

stripe.api_key = os.environ.get('STRIPE_KEY')

@api_view(['POST'])
def twilio_sms(request):
    phone_number = request.POST.get('phone_number')
    url = 'https://api.authy.com/protected/json/phones/verification/start'
    data = {'api_key': os.environ.get('TWILIO_KEY'), 'via': 'sms', 'phone_number': phone_number, 'country_code': '1'}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return JsonResponse({'message': 'Success'}, status=201)
    else:
        return JsonResponse(response.status_code, safe=False)

@api_view(['POST'])
def twilio_verify(request):
    verification_code = request.POST.get('verification_code')
    phone_number = request.POST.get('phone_number')
    url = 'https://api.authy.com/protected/json/phones/verification/check'
    data = {'api_key': os.environ.get('TWILIO_KEY'), 'verification_code': verification_code, 'phone_number': phone_number, 'country_code': '1'}
    response = requests.get(url, data=data)
    if response.status_code == 200:
        print(response.json())
        return JsonResponse({'message': 'Success'}, status=201)
    else:
        JsonResponse({'message': 'Failed'}, status=response.status_code)

@api_view(['POST'])
def issue_key(request):
    api_version = "2017-12-15"
    stripe_customer_count = StripeCustomer.objects.filter(user=request.user).count()
    if stripe_customer_count == 0:
        # Create Stripe customer
        stripe_response = stripe.Customer.create(email=request.user.email)
        stripe_customer = StripeCustomer.objects.create(stripe_id=stripe_response.id, user=request.user)
        customerId = stripe_customer.stripe_id
    else:
        customerId = stripe_customer_count[0].stripe_id
    key = stripe.EphemeralKey.create(customer=customerId, api_version="2017-05-25")
    return JsonResponse(key)

class UserList(APIView):
    """
    List all users, or create a new user.
    """
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ConsumerList(APIView):
    """
    List all consumers, or create a new consumer.
    """
    def get(self, request, format=None):
        consumers = Consumer.objects.all()
        serializer = ConsumerSerializer(consumerss, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ConsumerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ConsumerDetail(APIView):
    """
    Retrieve, update or delete a consumer instance.
    """
    def get_object(self, pk):
        try:
            return Consumer.objects.get(pk=pk)
        except Consumer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        consumer = self.get_object(pk)
        serializer = ConsumerSerializer(consumer)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        consumer = self.get_object(pk)
        serializer = ConsumerSerializer(consumer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        consumer = self.get_object(pk)
        consumer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProList(APIView):
    """
    List all pros, or create a new pro.
    """
    def get(self, request, format=None):
        pros = Pro.objects.all()
        serializer = ProSerializer(pros, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProDetail(APIView):
    """
    Retrieve, update or delete a pro instance.
    """
    def get_object(self, pk):
        try:
            return Pro.objects.get(pk=pk)
        except Pro.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        pro = self.get_object(pk)
        serializer = ProSerializer(pro)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        pro = self.get_object(pk)
        serializer = ProSerializer(pro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        pro = self.get_object(pk)
        pro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FavoriteList(APIView):
    """
    List all favorites, or create a new favorite.
    """
    permission_classes = (IsOwnerOrNotAllowed,)

    def get(self, request, format=None):
        favorites = Favorite.objects.all()
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FavoriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(consumer=self.request.user.consumer)


class FavoriteDetail(APIView):
    """
    Retrieve, update or delete a favorite instance.
    """
    permission_classes = (IsOwnerOrNotAllowed,)

    def get_object(self, pk):
        try:
            return Favorite.objects.get(pk=pk)
        except Favorite.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        favorite = self.get_object(pk)
        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        favorite = self.get_object(pk)
        serializer = FavoriteSerializer(favorite, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        favorite = self.get_object(pk)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectList(APIView):
    """
    List all projects, or create a new project.
    """
    def get(self, request, format=None):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(consumer=self.request.user.consumer)


class ProjectDetail(APIView):
    """
    Retrieve, update or delete a project instance.
    """
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ConversationList(APIView):
    """
    List all conversations, or create a new conversation.
    """
    permission_classes = (IsOwnerOrNotAllowed,)

    def get(self, request, format=None):
        conversations = Conversation.objects.all()
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ConversationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(consumer=self.request.user.consumer)


class ConversationDetail(APIView):
    """
    Retrieve, update or delete a conversatoin instance.
    """
    permission_classes = (IsOwnerOrNotAllowed,)

    def get_object(self, pk):
        try:
            return Conversation.objects.get(pk=pk)
        except Conversation.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        conversation = self.get_object(pk)
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        conversation = self.get_object(pk)
        serializer = ConversationSerializer(conversation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        conversation = self.get_object(pk)
        conversation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MessageList(APIView):
    """
    List all messages, or create a new message.
    """
    def get(self, request, format=None):
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(consumer=self.request.user.consumer)


class MessageDetail(APIView):
    """
    Retrieve, update or delete a message instance.
    """
    def get_object(self, pk):
        try:
            return Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        message = self.get_object(pk)
        serializer = MessageSerializer(message)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        message = self.get_object(pk)
        serializer = MessageSerializer(message, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        message = self.get_object(pk)
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SchedulingList(APIView):
    """
    List all schedulings, or create a new scheduling.
    """
    def get(self, request, format=None):
        schedulings = Schedulings.objects.all()
        serializer = SchedulingSerializer(schedulings, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SchedulingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SchedulingDetail(APIView):
    """
    Retrieve, update or delete a scheduling instance.
    """
    def get_object(self, pk):
        try:
            return Scheduling.objects.get(pk=pk)
        except Scheduling.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        scheduling = self.get_object(pk)
        serializer = SchedulingSerializer(scheduling)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        scheduling = self.get_object(pk)
        serializer = SchedulingSerializer(scheduling, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        scheduling = self.get_object(pk)
        scheduling.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ConfirmedAppointmentList(APIView):
    """
    List all confirmed appointments, or create a new confirmed appointment.
    """
    def get(self, request, format=None):
        confirmed_appointments = ConfirmedAppointment.objects.all()
        serializer = ConfirmedAppointmentSerializer(confirmed_appointments, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ConfirmedAppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmedAppointmentDetail(APIView):
    """
    Retrieve, update or delete a confirmed appointment instance.
    """
    def get_object(self, pk):
        try:
            return ConfirmedAppointment.objects.get(pk=pk)
        except ConfirmedAppointment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        confirmed_appointment = self.get_object(pk)
        serializer = ConfirmedAppointmentSerializer(confirmed_appointment)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        confirmed_appointment = self.get_object(pk)
        serializer = ConfirmedAppointmentSerializer(confirmed_appointment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        confirmed_appointment = self.get_object(pk)
        confirmed_appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuoteList(APIView):
    """
    List all quotes, or create a new quote.
    """
    def get(self, request, format=None):
        quotes = Quote.objects.all()
        serializer = QuoteSerializer(quotes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = QuoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuoteDetail(APIView):
    """
    Retrieve, update or delete a quote instance.
    """
    def get_object(self, pk):
        try:
            return Quote.objects.get(pk=pk)
        except Quote.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        quote = self.get_object(pk)
        serializer = QuoteSerializer(quote)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        quote = self.get_object(pk)
        serializer = QuoteSerializer(quote, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        quote = self.get_object(pk)
        quote.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ConfirmedPriceList(APIView):
    """
    List all confirmed prices, or create a new confirmed price.
    """
    def get(self, request, format=None):
        confirmed_prices = ConfirmedPrice.objects.all()
        serializer = ConfirmedPriceSerializer(confirmed_prices, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ConfirmedPriceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmedPriceDetail(APIView):
    """
    Retrieve, update or delete a confirmed price instance.
    """
    def get_object(self, pk):
        try:
            return ConfirmedPrice.objects.get(pk=pk)
        except ConfirmedPrice.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        confirmed_price = self.get_object(pk)
        serializer = ConfirmedPriceSerializer(confirmed_price)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        confirmed_price = self.get_object(pk)
        serializer = ConfirmedPriceSerializer(confirmed_price, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        confirmed_price = self.get_object(pk)
        confirmed_price.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
