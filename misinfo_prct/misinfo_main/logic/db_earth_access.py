from datetime import datetime
from django.db import connections, connection
from threading import Thread
from django.contrib import messages
from misinfo_main.models import Paper_SeSc


def postpone(function):
    """postpone -> connection needs to be closed in function if db connection"""
    def decorator(*args, **kwargs):
        t = Thread(target=function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()

    return decorator


def fetch_papers(request, dbquery):
    try:
        with connections['earth_semanticscholar'].cursor() as cursor:  # " title iLIKE '%misinformation%'  \OFFSET floor(random() * 20000) LIMIT 1;" corpusid = 44334635"
            loops = 0
            dbquery.is_fetching = True
            dbquery.save()
            while True:
                now = datetime.now()
                cursor.execute(dbquery.query)
                dbpapers = cursor.fetchall()
                print('time query', datetime.now() - now)
                if dbpapers:
                    for dbpaper in dbpapers:
                        corpusid, title, abstract, url_sesc = dbpaper
                        # can already be in local db since it is a random sample
                        defaults = {'dbquery_id': dbquery.pk,
                                    'title': title, 'abstract': abstract,
                                    'url_sesc': url_sesc}
                        Paper_SeSc.objects.get_or_create(corpusid=corpusid, defaults=defaults)

                    break
                if loops == 3:
                    print('loop')
                    return None
                loops += 1
    except Exception as e:
        messages.add_message(request, messages.ERROR, 'DB connection:' + str(e))
    dbquery.is_fetching = False
    dbquery.save()



@postpone
def fetch_papers_postpone(request, dbquery):
    fetch_papers(request, dbquery)
    connection.close()