from misinfo_prct.misinfo_main.models import Paper


def get_papers():
	papers = Paper.objects.filter(year__gt=2020)