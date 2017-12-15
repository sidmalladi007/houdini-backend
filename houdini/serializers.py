from rest_framework import serializers
from houdini.models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    messages = serializers.PrimaryKeyRelatedField(many=True, queryset=Message.objects.all())

    class Meta:
        model = User
        fields = ('url', 'id', 'first_name', 'last_name', 'email', 'username', 'messages')


class ConsumerSerializer(serializers.HyperlinkedModelSerializer):
    favorites = serializers.PrimaryKeyRelatedField(many=True, queryset=Favorite.objects.all())
    projects = serializers.PrimaryKeyRelatedField(many=True, queryset=Project.objects.all())
    conversations = serializers.PrimaryKeyRelatedField(many=True, queryset=Conversation.objects.all())
    class Meta:
        model = Consumer
        fields = ('url', 'id', 'city', 'user', 'favorites', 'projects', 'conversations')


class ProSerializer(serializers.HyperlinkedModelSerializer):
    conversations = serializers.PrimaryKeyRelatedField(many=True, queryset=Conversation.objects.all())

    class Meta:
        model = Pro
        fields = ('url', 'id', 'business_name', 'city', 'state', 'phone_number',
            'description', 'services', 'conversations')


class FavoriteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Favorite
        fields = ('url', 'id', 'pro', 'consumer')


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('url', 'id', 'project_name', 'project_description',
            'completed', 'consumer', 'created_at')


class ConversationSerializer(serializers.HyperlinkedModelSerializer):
    schedules = serializers.PrimaryKeyRelatedField(many=True, queryset=Scheduling.objects.all())
    confirmed_appointments = serializers.PrimaryKeyRelatedField(many=True, queryset=ConfirmedAppointment.objects.all())
    quotes = serializers.PrimaryKeyRelatedField(many=True, queryset=Quote.objects.all())
    confirmed_prices = serializers.PrimaryKeyRelatedField(many=True, queryset=ConfirmedPrice.objects.all())

    class Meta:
        model = Conversation
        fields = ('pro', 'consumer', 'status', 'active', 'completed',
            'created_at', 'schedules', 'confirmed_appointments', 'quotes',
            'confirmed_prices')


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ('conversation', 'content', 'sender', 'created_at')


class SchedulingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Scheduling
        fields = ('name', 'expected_duration', 'time_1', 'time_2', 'time_3',
            'conversation', 'created_at')


class ConfirmedAppointmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ConfirmedAppointment
        fields = ('time', 'scheduling', 'conversation', 'created_at')


class QuoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Quote
        fields = ('quoted_price', 'conversation', 'created_at')


class ConfirmedPriceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ConfirmedPrice
        fields = ('confirmed_price', 'conversation', 'quote', 'created_at')
