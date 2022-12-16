from datetime import datetime

from django.db import connections
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

def random_paper():
	def fetch_papers():
		with connections['earth_semanticscholar'].cursor() as cursor: # " title iLIKE '%misinformation%'  \OFFSET floor(random() * 20000) LIMIT 1;" corpusid = 44334635"
			loops = 0
			while True:
				now = datetime.now()
				cursor.execute(dbquery.query)
				dbpapers = cursor.fetchall()
				print('time query', datetime.now() - now)
				if dbpapers:
					for dbpaper in dbpapers:
						corpusid, title, abstract, url_sesc = dbpaper
						# can already be in local db since it is a random sample
						defaults = {'dbquery_id':dbquery.pk,
									'title':title, 'abstract':abstract,
									'url_sesc':url_sesc}
						Paper_SeSc.objects.get_or_create(corpusid=corpusid, defaults=defaults)

					break
				if loops == 3:
					print('loop')
					return None
				loops += 1

	dbquery = DBQuery.objects.filter(active=True).order_by('-updated_at').first()
	if dbquery is None:
		tbl = 'public.papers'
		q_where = "title iLIKE '%misinformation%'" #misinformation
		# only papers with abstract
		query = f'SELECT t1.corpusid, t1.title, t2.abstract, t3.url FROM {tbl} as t1 tablesample system (1) ' \
				f'JOIN public.abstract as t2 on t1.corpusid = t2.corpusid ' \
				f'JOIN public.papers_openaccessinfo as t3 on t1.corpusid = t3.corpusid ' \
				f'where {q_where}  limit 10;' # samples first 1% of table
		query = " ".join(query.split())  # remove duplicate spaces
		dbquery, cr = DBQuery.objects.get_or_create(query=query)
	filter_d = {'dbquery': dbquery, 'paperclass': None}
	paper = Paper_SeSc.objects.filter(**filter_d).first()
	if paper is None:
		fetch_papers()
		paper = Paper_SeSc.objects.filter(**filter_d).first()
	return paper


if __name__ == "__main__":
	random_paper()