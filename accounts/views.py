from django.shortcuts import render, redirect
from .models import Connection, Application
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib import messages


@login_required
def create_connection(request):
  if request.method == 'POST':
    try:
      # Get the selected sender and receiver from the POST data
      sender_app = Application.objects.get(pk=request.POST['sender_app'])
      receiver_app = Application.objects.get(pk=request.POST['receiver_app'])

      # Create a new Connection with the logged-in user
      connection = Connection.objects.create(
          sender=sender_app,
          receiver=receiver_app,
          user=request.user  # Associate the connection with the logged-in user
      )

      # Save the connection (it will automatically validate and update is_active)
      connection.save()

      # Show success message and redirect
      messages.success(request, 'Connection created successfully!')
      return redirect(
          'connection_list')  # Replace with your connection list view

    except Application.DoesNotExist:
      messages.error(request, 'Invalid sender or receiver application.')
    except ValidationError as e:
      messages.error(request, e.message)

  # If the request is GET or POST fails, display the form again
  applications = Application.objects.all()
  return render(request, 'accounts/create_connection.html',
                {'applications': applications})


@login_required
def connection_list(request):
  # Get the connections associated with the logged-in user
  connections = Connection.objects.filter(user=request.user)

  return render(request, 'accounts/connection_list.html',
                {'connections': connections})
