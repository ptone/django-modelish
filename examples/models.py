class Poll(models.Model):
    """This is the poll model"""

    pub_date = models.DateTimeField(
        'date published')
    question = models.CharField(
        max_length=200,
        blank=True)

class Choice(models.Model):
    choice_text = models.CharField(
        max_length=200,
        blank=True)
    poll = models.ForeignKey(
        'Poll')
    votes = models.IntegerField()


