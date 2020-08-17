from django.shortcuts import render
from django.http import HttpResponseRedirect

from apps.contacts.forms import ContactUsModelForm


def contact_us(request):
    context = {}
    form = ContactUsModelForm(request.POST)

    if request.method == 'POST':
        form = ContactUsModelForm(request.POST)
        if form.is_valid():
            objc = form.save(commit=False)
            objc.name = request.user.name
            objc.email = request.user
            objc.phone = request.user.phone
            objc.save()
            return HttpResponseRedirect('/')
    else:
        context['form'] = form
        return render(request, 'contacts/contact_us.html', context)
