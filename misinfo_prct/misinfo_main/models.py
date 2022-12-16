from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.

#use this table as check
class Paper(models.Model):
    corpus_paper_id = models.PositiveIntegerField(primary_key=True)  # declared in order django does not create one
    title = models.TextField()
    year = models.FloatField()

    def save(self, *args, **kwargs):
        return

    def delete(self, *args, **kwargs):
        return

    class Meta:
        db_table = 'paper' # npr_main db
        managed = False

class DBQuery(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    query = models.CharField(max_length=500)
    def __str__(self):
        return self.query[:15]


class PaperClassification(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100) # in Scope
    comment = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.name


class Paper_SeSc(models.Model):
    corpusid = models.PositiveIntegerField()
    paperclass = models.ForeignKey(PaperClassification, models.SET_NULL, null=True, blank=True, related_name='query_paper_sesc')
    dbquery = models.ForeignKey(DBQuery, models.SET_NULL, null=True, blank=True)
    comment = models.CharField(max_length=200, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=500)
    abstract = models.TextField()
    url_sesc = models.URLField()

    def __str__(self):
        return self.title


class Abstract(models.Model):
    corpusid = models.PositiveIntegerField(primary_key=True)
    abstract = models.CharField(max_length=500)
    updated = models.DateTimeField()
    def save(self, *args, **kwargs):
        return

    def delete(self, *args, **kwargs):
        return
    class Meta:
        db_table = 'public.abstract'
        managed = False
    
class Papers(models.Model):
    corpusid = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=500)
    referencecount = models.PositiveIntegerField()
    citationcount = models.PositiveIntegerField()
    influentialcitationcount = models.PositiveIntegerField()
    isopenaccess = models.BooleanField()
    venue = models.CharField(max_length=500)
    s2fieldsofstudy = ArrayField(models.CharField(max_length=200))
    publicationtypes = ArrayField(models.CharField(max_length=200))
    publicationdate = models.DateField()
    paperyear = models.PositiveIntegerField()
    updated = models.DateTimeField()


    def save(self, *args, **kwargs):
        return

    def delete(self, *args, **kwargs):
        return

    class Meta:
        db_table = 'public.papers'
        managed = False

"""

class authors (
    authorid bigint primary key,
    url = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    aliases = ArrayField(models.CharField(max_length=200))
    affiliations = models.CharField(max_length=500)
    homepage = models.CharField(max_length=500)
    papercount = models.PositiveIntegerField()
    citationcount = models.PositiveIntegerField()
    hindex = models.PositiveIntegerField()
    updated timestamp with time zone not null
);

class citations (
    citingcorpusid = models.PositiveIntegerField()
    citedcorpusid = models.PositiveIntegerField()
    isinfluential = models.BooleanField()
    contexts = ArrayField(models.CharField(max_length=200))
    intents = ArrayField(models.CharField(max_length=200))
    updated timestamp with time zone not null
);

/* authors and access info in separate tables */


class author2paper (
    corpusid int not null,
    authorid big= models.PositiveIntegerField()
    name = models.CharField(max_length=500)
);

class papers_openaccessinfo (
    corpusid = models.PositiveIntegerField(primary_key=True)
    ACL = models.CharField(max_length=500)
    DBLP = models.CharField(max_length=500)
    Arxiv = models.CharField(max_length=500)
    MAG = models.CharField(max_length=500)
    PubMed = models.CharField(max_length=500)
    DOI = models.CharField(max_length=500)
    PubMedCentral = models.CharField(max_length=500)
    license = models.CharField(max_length=500)
    status = models.CharField(max_length=500)
    url text
);

/* "text" is in the content dictionary: content["text"] */
/* "source" is in the content dictionary: content["text"] */
class s2orc (
    corpusid = models.PositiveIntegerField(primary_key=True)
    source = models.CharField(max_length=500)
    text = models.CharField(max_length=500)
    annotations = models.CharField(max_length=500)
    updated timestamp with time zone not null
);


class paper-ids (
    corpusid = models.PositiveIntegerField(primary_key=True)
    sha = models.CharField(max_length=500)
);

class embeddings (
    corpusid = models.PositiveIntegerField(primary_key=True)
    model = models.CharField(max_length=500)
    vector = models.CharField(max_length=500)
);


class tldrs (
    corpusid = models.PositiveIntegerField(primary_key=True)
    model = models.CharField(max_length=500)
    text = models.CharField(max_length=500)
);




"""