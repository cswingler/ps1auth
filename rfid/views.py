from .models import Resource, RFIDNumber
from .forms import KeyForm
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def check(request, resource_name, tag_number):
    try:
        tag = RFIDNumber.objects.get(ASCII_125khz=tag_number)
        resource = Resource.objects.get(name=resource_name)
    except (RFIDNumber.DoesNotExist, Resource.DoesNotExist):
        return HttpResponse(content="No", status=404, reason="Resource or Tag not Found")
    if resource.is_allowed(tag):
        return HttpResponse(content="Yes", status=200, reason="Access Allowed")
    else:
        return HttpResponse(content="No", status=403, reason="Access Denied")


@login_required()
def configure_rfid(request):
    try:
        tag = request.user.rfidnumber
    except RFIDNumber.DoesNotExist:
        tag = RFIDNumber(user=request.user)
    if request.method == 'POST':
        form = KeyForm(request.POST, instance=tag)
        if form.is_valid():
            foo = form.save(commit=False)
            foo.save()
            messages.success(request, "RFID tag number updated")
    else:
        request.user.rfidnumber
        form = KeyForm(instance=tag)

    data = {}
    data['form'] = form
    data['title'] = 'Configure RFID'
    return render(request, "ps1auth/form.html", data)

