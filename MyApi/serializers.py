from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","name","mobile_no", "gender")

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.mobile_no = validated_data.get("mobile_no", instance.mobile_no)
        instance.gender = validated_data.get("gender", instance.gender)
        instance.save()
        return instance