import os

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.cbook as cbook
import psycopg2
from psycopg2 import extras
from MySQLdb import _mysql
#from django.conf import settings
from django.db import connections

from misinfo_prct.misinfo_server.settings import set_env_variables, BASE_DIR

set_env_variables(BASE_DIR)


def get_result(query):
    """
    cur = conn.cursor()
    cur.execute to execute query
    :return: query result
    """
    conn = psycopg2.connect(
        host='mars.lab.cip.uw.edu',  # name of the server
        database='semanticscholar',  # name of the database
        sslmode="require",
        user='hodeld',
        cursor_factory=psycopg2.extras.DictCursor,
    )
    conn.autocommit = True
    with conn.cursor() as cur:

        cur.execute(query)
        result = cur.fetchall()# all
    conn.close()
    return result


def month_cumul_d():
    query = f"select count(*) as c,  paperyear\
            from public.papers   \
            where paperyear IS NOT Null  group by paperyear \
            order by paperyear"

    result = get_result(query)

    count = 0
    m_d = {}
    for i in result:
        count += int(i[0])
        d = int(i[1])
        m_d[d] = count
    return m_d


def citation_date():
    cat = ('ND',
        'Communication',
           'Medicine',
           'Information',
           'Political Science',
           'Education',
           'Law',
           'Pediatrics',
           'Psychiatry',
           'History',
           'Computer Science',
           'Psychology',
           'Sociology',
           'Economics')
    vmax = len(cat)

    def get_cat(name):
        for ci, n in enumerate(cat, 1):
            if n in name:
                break
            else:
                ci = 0
                n = 'Various'
        return ci, n

    query = f"SELECT citationcount, paperyear, s2fieldsofstudy FROM public.papers \
    where title iLIKE '%misinformation%'  AND paperyear > 1995  order by citationcount desc limit 1000"

    result = get_result(query)
    sizes = []
    dates = []
    counts = []
    colors = []
    labels_d = {}
    m_d = month_cumul_d()
    cmap = plt.cm.Spectral
    norm = plt.Normalize(vmin=0, vmax=vmax)

    for i in result:
        sizes.append(int(i[0]))
        year = int(i[1])

        ra = i[2][0] if i[2] else 'ND'  # list of fields
        #ra_color = research_areas_c.get(ra, '0')
        ra_color, ra_cat = get_cat(ra)
        col_c = int(ra_color)
        colors.append(col_c)
        labels_d[col_c] = ra_cat
        dates.append(year)
        counts.append(m_d[year])

    colors_i = cmap(norm(colors))

    npl = np.array(colors)
    npd = np.array(dates)
    npc = np.array(counts)
    nps = np.array(sizes)
    npcolors = np.array(colors_i)

    fig, ax = plt.subplots()

    for c_i in np.unique(npl):
        ix = np.where(npl == c_i)
        cat = labels_d[c_i]
        ax.scatter(npd[ix], npc[ix], s=nps[ix], c=npcolors[ix], label=cat, alpha=0.5)
    ax.legend()

    ax.set_xlabel('Years', fontsize=15)
    ax.set_ylabel('# Publications', fontsize=15)
    ax.set_title('Misinformation Studies - Cumulative - Times Cited')
    ax.legend()

    ax.grid(True)
    fig.tight_layout()

    plt.show()


def count_misinfo_papers_text():
    query = f"select count(corpusid) \
                from public.s2orc   \
                where text iLIKE '%misinformation%' or text iLIKE '%disinformation%' "
    result = get_result(query)
    print(result)  # 19743 have in text misinformation (npr_misinfo: 20970 papers)


if __name__ == "__main__":
    #citation_date()
    #count_misinfo_papers_text()
    query = " SELECT corpusid FROM public.abstract where abstract iLIKE '%misinformation%'  \
					   ;" # OFFSET floor(random() * 2000) LIMIT 1
    res = get_result(query)
    print(res)
    ids = [row[0] for row in res]
    data_dir = os.path.join(BASE_DIR.parent.parent, 'data')
    corpus_id_dir = os.path.join(data_dir, 'semsc_corpus_id')
    queries_fp = os.path.join(data_dir, 'queries.csv')
    qdf = pd.DataFrame.read_csv(queries_fp) #columns=['query_nr', 'query', 'c_papers']
    query_nr = qdf.index
    ids_df = pd.DataFrame(ids)
    c_papers = ids_df.size
    qdf.loc[len(qdf.index)] = [query_nr, query, c_papers]
    ids_name = f'semantic_scholar_query_{query_nr}.csv'
    ids_fp = os.path.join(corpus_id_dir, ids_name)
    qdf.to_csv(queries_fp)
    ids_df.to_csv(ids_fp)


