from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Client
from .forms import ClientForm


@login_required
def client_list(request):
    """
    Display all clients with optional search functionality.
    Searches across name, business name, phone, and email.
    """
    clients = Client.objects.all()

    # Get search query from URL params e.g. ?q=john
    query = request.GET.get('q', '')

    if query:
        # Use Q objects to search across multiple fields simultaneously
        clients = clients.filter(
            Q(name__icontains=query) |
            Q(business_name__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(email__icontains=query)
        )

    return render(request, 'clients/client_list.html', {
        'clients': clients,
        'query': query,  # Pass query back to keep search box filled
    })


@login_required
def client_detail(request, pk):
    """
    Show a single client's details and all their subscriptions.
    """
    # Return 404 if client not found
    client = get_object_or_404(Client, pk=pk)

    # Fetch all subscriptions linked to this client
    subscriptions = client.subscriptions.all()

    return render(request, 'clients/client_detail.html', {
        'client': client,
        'subscriptions': subscriptions,
    })


@login_required
def client_create(request):
    """
    Handle creating a new client.
    GET — show empty form
    POST — validate and save
    """
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to client list after successful creation
            return redirect('client_list')
    else:
        # Show blank form for GET request
        form = ClientForm()

    return render(request, 'clients/client_form.html', {
        'form': form,
        'title': 'Add New Client',
    })


@login_required
def client_edit(request, pk):
    """
    Handle editing an existing client.
    GET — show form pre-filled with current data
    POST — validate and update
    """
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        # Pass instance to update existing record instead of creating new
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_detail', pk=client.pk)
    else:
        form = ClientForm(instance=client)

    return render(request, 'clients/client_form.html', {
        'form': form,
        'title': 'Edit Client',
        'client': client,
    })


@login_required
def client_delete(request, pk):
    """
    Confirm and delete a client record.
    GET — show confirmation page
    POST — perform deletion
    """
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        client.delete()
        return redirect('client_list')

    return render(request, 'clients/client_confirm_delete.html', {
        'client': client,
    })