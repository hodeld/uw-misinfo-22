from misinfo_main.forms import PaperFilterForm
from django.contrib import messages

from misinfo_main.models import Paper_SeSc


def save_paper(request):
    p_pk = int(request.POST.get('pk'))
    paper = Paper_SeSc.objects.get(pk=p_pk)
    form = PaperFilterForm(request.POST, instance=paper)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.INFO, 'Form saved')
    else:
        messages.add_message(request, messages.ERROR, 'Form Error')

