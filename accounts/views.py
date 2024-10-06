from django.shortcuts import render, redirect
from .models import Connection, Application
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib import messages
from .forms import ConnectionForm


@login_required
def connection_list(request):
  # Get the connections associated with the logged-in user
  connections = Connection.objects.filter(user=request.user)

  return render(request, 'accounts/connection_list.html',
                {'connections': connections})


@login_required
def create_connection(request):
  applications = None
  country_selected = None
  connection_form = None

  if request.method == 'POST':
    # Check if country selection has been made
    if 'country' in request.POST:
      country_selected = request.POST.get('country')
      applications = Application.objects.filter(country=country_selected)
      connection_form = ConnectionForm(country=country_selected)
    else:
      # Creating a connection
      country_selected = request.POST.get('country')
      connection_form = ConnectionForm(request.POST, country=country_selected)

      if connection_form.is_valid():
        connection = connection_form.save(commit=False)
        connection.user = request.user
        try:
          connection.clean()  # Validate the connection logic
          connection.save()  # Save the connection
          return redirect('accounts:connection_list'
                          )  # Redirect to a success page or connections list
        except ValidationError as e:
          return render(
              request, 'create_connections.html', {
                  'connection_form': connection_form,
                  'country_selected': country_selected,
                  'error_message': str(e),
              })

  return render(request, 'accounts/create_connections.html', {
      'connection_form': connection_form,
      'country_selected': country_selected,
  })
