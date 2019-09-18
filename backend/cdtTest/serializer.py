import datetime
from rest_framework import serializers


class CdtTestSerializer(serializers.Serializer):
    class Meta:
        # model = CdtTest
        # fields = ("test_time", "hand_time", "person")
        test_time = serializers.SerializerMethodField()
        hand_time = serializers.SerializerMethodField()
        person = serializers.CharField()

    @staticmethod
    def get_test_time(row):
        test_time = row.test_time
        test_time = test_time + datetime.timedelta(hours=8)
        test_time = datetime.datetime.strftime(test_time, '%Y-%m-%d %H:%M:%S')
        return test_time

    @staticmethod
    def get_hand_time(row):
        hand_time = row.hand_time
        hand_time = hand_time + datetime.timedelta(hours=8)
        hand_time = datetime.datetime.strftime(hand_time, '%Y-%m-%d %H:%M:%S')
        return hand_time

# from rest_framework.serializers import ModelSerializer
# from .models import CdtTest
#
#
# class CdtTestSerializer(ModelSerializer):
#     class Meta:
#         model = CdtTest
#         fields = '__all__'

