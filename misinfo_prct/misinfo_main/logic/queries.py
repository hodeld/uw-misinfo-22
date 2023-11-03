from misinfo_main.logic.db_earth_access import fetch_papers, fetch_papers_postpone
from misinfo_main.models import Papers, Abstract, Paper_SeSc, DBQuery, PaperClassification

PAPERCLASS_INSCOPE_ID = 1
def get_papers():
	papers = Abstract.objects.using('earth_semanticscholar').filter(
		abstract__icontains='misinformation')

def transfer_papers():
	papers = Papers.objects.using('earth_semanticscholar').filter(
		paperyear__gt=2020).prefetch_related('authors', 'citations') # all foreignkeys

	# save all on local default -> save related first
		#object.save(using='the_db')
def get_dbquery():
	tbl = 'public.papers'
	query_list = [
		('title', ('misinformation', 'disinformation', ('fake', 'news'))),
		('abstract', ('misinformation', 'disinformation', ('fake', 'news'))),
	]
	q_base = "{chapter} iLIKE '%{key_word}%'"  # misinformation
	q_where = ""
	for i, (chapt, key_words) in enumerate(query_list):
		for j, key_word in enumerate(key_words):
			if type(key_word) == tuple:
				q_where += '( '
				for k, kw in enumerate(key_word):
					q_where += q_base.format(chapter=chapt, key_word=kw)
					if k < len(key_word) - 1:
						q_where += ' AND '
				q_where += ' )'
			else:
				q_where += q_base.format(chapter=chapt, key_word=key_word)
			if j < len(key_words) - 1:
				q_where += ' OR '

		if i < len(query_list) - 1:
			q_where += ' OR '

	# only papers with abstract, otherwise left join
	query = f'SELECT t1.corpusid, t1.title, t2.abstract, t3.url FROM {tbl} as t1 tablesample system (1) ' \
			f'JOIN public.abstract as t2 on t1.corpusid = t2.corpusid ' \
			f'JOIN public.papers_openaccessinfo as t3 on t1.corpusid = t3.corpusid ' \
			f'where {q_where}  limit 30;'  # samples first 1% of table
	query = " ".join(query.split())  # remove duplicate spaces
	print(query)
	dbquery, cr = DBQuery.objects.get_or_create(query=query)
	return dbquery
def random_paper(request):
	dbqueries = DBQuery.objects.filter(active=True).order_by('-updated_at')
	if len(dbqueries) == 0:
		dbqueries = [get_dbquery()]
	filter_d = {'dbquery__in': dbqueries, 'paperclass': None}
	papers = Paper_SeSc.objects.filter(**filter_d)
	dbquery = dbqueries[0]  # fetch of the newest query
	if len(papers) == 0:
		fetch_papers(request, dbquery)
		papers = Paper_SeSc.objects.filter(**filter_d)
	elif len(papers) < 15 and dbquery.is_fetching is False:  # can take up to 3 minutes to fetch papers
		fetch_papers_postpone(request, dbquery)
	paper = papers.first()
	return paper


if __name__ == "__main__":
	#from misinfo_prct.misinfo_server import settings
	#DJANGO_SETTINGS_MODULE = settings.__init__
	#settings.configure()
	#settings.set_env_variables(settings.BASE_DIR)
	get_dbquery()
	#random_paper()