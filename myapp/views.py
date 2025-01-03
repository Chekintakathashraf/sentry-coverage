from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer

class ProjectAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            project = get_object_or_404(Project, pk=pk)
            serializer = ProjectSerializer(project)
            return Response(serializer.data)
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class TaskAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            task = get_object_or_404(Task, pk=pk)
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from django.http import HttpResponse, HttpResponseForbidden
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

def trigger_error(request):
    try:
        division_by_zero = 1 / 0
    except ZeroDivisionError as e:
        logger.error(f"Division by zero triggered: {str(e)}")
        raise e
    return Response("This won't be reached")

def trigger_permission_denied(request):
    return HttpResponseForbidden("You do not have permission to access this resource.")

def trigger_value_error(request):
    try:
        raise ValueError("This is a simulated ValueError for Sentry testing.")
    except ValueError as e:
        logger.error(f"ValueError triggered: {str(e)}")
        raise e

def trigger_logging_error(request):
    try:
        logger.error("This is a simulated logging error for Sentry testing.")
        return HttpResponse("Logging error triggered!", status=500)
    except Exception as e:
        logger.error(f"Error logging message: {str(e)}")
        return HttpResponse("An error occurred while logging.", status=500)
