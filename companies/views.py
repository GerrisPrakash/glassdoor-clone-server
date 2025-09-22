from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Company, Job, Review
from .serializers import CompanySerializer, JobSerializer, ReviewSerializer


# --- Permissions ---
class IsEmployerOrReadOnly(permissions.BasePermission):
    """Employers can create/update/delete, others can only view."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == "employer"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if hasattr(obj, "created_by"):
            return obj.created_by == request.user
        if hasattr(obj, "posted_by"):
            return obj.posted_by == request.user
        return False


class IsReviewerOrReadOnly(permissions.BasePermission):
    """Only the review author can edit/delete."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


# --- Company APIs ---
class CompanyListCreateAPIView(APIView):
    permission_classes = [IsEmployerOrReadOnly]

    def get(self, request):
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyDetailAPIView(APIView):
    permission_classes = [IsEmployerOrReadOnly]

    def get_object(self, pk):
        return Company.objects.get(pk=pk)

    def get(self, request, pk):
        company = self.get_object(pk)
        serializer = CompanySerializer(company)
        return Response(serializer.data)

    def put(self, request, pk):
        company = self.get_object(pk)
        self.check_object_permissions(request, company)
        serializer = CompanySerializer(company, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        company = self.get_object(pk)
        self.check_object_permissions(request, company)
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- Job APIs ---
class JobListCreateAPIView(APIView):
    permission_classes = [IsEmployerOrReadOnly]

    def get(self, request):
        queryset = Job.objects.all()
        company_id = request.query_params.get("company")
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        serializer = JobSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(posted_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobDetailAPIView(APIView):
    permission_classes = [IsEmployerOrReadOnly]

    def get_object(self, pk):
        return Job.objects.get(pk=pk)

    def get(self, request, pk):
        job = self.get_object(pk)
        serializer = JobSerializer(job)
        return Response(serializer.data)

    def put(self, request, pk):
        job = self.get_object(pk)
        self.check_object_permissions(request, job)
        serializer = JobSerializer(job, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        job = self.get_object(pk)
        self.check_object_permissions(request, job)
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- Review APIs ---
class ReviewListCreateAPIView(APIView):
    permission_classes = [IsReviewerOrReadOnly]

    def get(self, request):
        queryset = Review.objects.all()
        company_id = request.query_params.get("company")  # check if company filter exists
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetailAPIView(APIView):
    permission_classes = [IsReviewerOrReadOnly]

    def get_object(self, pk):
        return Review.objects.get(pk=pk)

    def get(self, request, pk):
        review = self.get_object(pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    def put(self, request, pk):
        review = self.get_object(pk)
        self.check_object_permissions(request, review)
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        review = self.get_object(pk)
        self.check_object_permissions(request, review)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
