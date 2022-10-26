from django.db import models

# Create your models here.
class Paper(models.Model):
    corpus_paper_id = models.PositiveIntegerField(primary_key=True)  # declared in order django does not create one
    title = models.TextField()
    year = models.FloatField()

    def save(self, *args, **kwargs):
        return

    def delete(self, *args, **kwargs):
        return

    class Meta:
        db_table = 'paper'
        managed = False