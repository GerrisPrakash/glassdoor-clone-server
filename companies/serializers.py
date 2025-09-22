from rest_framework import serializers
from .models import Company, Job, Review
from django.db.models import Avg

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"
        read_only_fields = ("created_by", "created_at")


class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField()
    company_rating = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = "__all__"
        read_only_fields = ("posted_by", "created_at")

    def get_company_name(self, obj):
        return obj.company.name if obj.company else None

    def get_company_rating(self, obj):
        avg = Review.objects.filter(company=obj.company).aggregate(avg_rating=Avg("rating"))
        return round(avg["avg_rating"], 1) if avg["avg_rating"] else None


class ReviewSerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ("user", "created_at")

    def get_company_name(self, obj):
        return obj.company.name if obj.company else None

    def get_user_name(self, obj):
        return obj.user.name if obj.user else None
