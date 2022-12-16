from django.shortcuts import render

from misinfo_main.forms import PaperFilterForm
from misinfo_main.logic.form_routines import save_paper
from misinfo_main.logic.queries import random_paper


# Create your views here.
def home(request):
    if request.method == 'POST':
        save_paper(request)

    #update_db_form = PaperFilterForm()
    paper = random_paper()
    form = PaperFilterForm(instance=paper)
    extra_d = {'form': form, 'paper':paper}
    #extra_d.update(paper_d)
    return render(request, 'misinfo_main/base.html', extra_d)