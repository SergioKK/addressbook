from django.shortcuts import render, redirect
from rest_framework import viewsets

from contacts.contacts_form import ContactForm
from contacts.models import Contact
from django.db.models import Q
from contacts.serializer import ContactSerializer


class ContactsView(viewsets.ModelViewSet):
    queryset = Contact.get_all()
    serializer_class = ContactSerializer


def contacts_list(request):
    context = {}
    search_input = request.GET.get('search-area')

    if search_input:
        lookups = Q(first_name__icontains=search_input) | Q(last_name__icontains=search_input) | Q(
            phone_number__icontains=search_input) | Q(contact_url__icontains=search_input) | Q(
            first_name__icontains=search_input)
        contacts = Contact.objects.filter(lookups)
    else:
        contacts = Contact.objects.all()
        search_input = ''
    context.update({'contacts': contacts, 'search_input': search_input})
    return render(request, 'all_contacts.html', context)


def contact_form(request, id=0):
    if request.method == 'GET':
        if id == 0:
            form = ContactForm()
        else:
            contact = Contact.get_by_id(id)
            form = ContactForm(instance=contact)
        return render(request, 'contact_form.html', {'form': form})
    else:
        if id == 0:
            form = ContactForm(request.POST, request.FILES)
        else:
            contact = Contact.get_by_id(id)
            form = ContactForm(request.POST, request.FILES, instance=contact)
        if form.is_valid():
            form.save()
        return redirect('contacts:contacts_list')


def contact_delete(request, id):
    Contact.delete_by_id(id)
    return redirect('contacts:contacts_list')
