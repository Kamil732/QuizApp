from django.shortcuts import reverse
from django.db import models
from django.utils.text import slugify

from quiz_app.images import valid_url_extension

from users.models import User

class Quiz(models.Model):
    CATEGORY = (
        ('general_knowledge', 'General knowledge'),
        ('celebrities', 'Celebrities'),
        ('for_kids', 'For kids'),
        ('movies', 'Movies'),
        ('geography', 'Geography'),
        ('history', 'History'),
        ('literature', 'Literature'),
        ('people', 'People'),
        ('music', 'Music'),
        ('science', 'Science'),
        ('policy', 'Policy'),
        ('nature', 'Nature'),
        ('psychology', 'Psychology'),
        ('religion', 'Religion'),
        ('entertainment', 'Entertainment'),
        ('sport', 'Sport'),
        ('technology', 'Technology'),
        ('television', 'Television'),
        ('funny', 'Funny'),
        ('puzzles', 'Puzzles'),
        ('health_and_beauty', 'Health and beauty'),
        ('animals', 'Animals'),
    )

    SECTION = (
        ('knowledge_quiz', 'Knowledge Quiz'),
        ('psychology_quiz', 'Psychology Quiz'),
        ('preferential_quiz', 'Preferential Quiz'),
        ('universal_quiz', 'Universal Quiz'),
    )

    IS_PUBLISHED = (
        ('True', 'Publish'),
        ('False', 'Private'),
    )

    YES_NO_CHOICE = (
        ('True', 'Yes'),
        ('False', 'No'),
    )

    DEFAULT_IMAGE_URL = 'https://cdn.pixabay.com/photo/2017/01/24/00/21/question-2004314_960_720.jpg'

    author          = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizes', blank=True, null=True)
    section         = models.CharField(max_length=17, choices=SECTION, blank=False, null=False)
    category        = models.CharField(max_length=17, choices=CATEGORY, blank=False, null=False)
    title           = models.TextField(null=False, blank=False)
    description     = models.TextField(blank=True, null=True)
    summary_text    = models.TextField(blank=True, null=True)
    image_url       = models.URLField(default=DEFAULT_IMAGE_URL, blank=True, null=True)
    solves          = models.PositiveIntegerField(default=0, editable=False)
    is_published    = models.CharField(max_length=5, choices=IS_PUBLISHED, default='True')
    is_opinions     = models.CharField(max_length=5, choices=YES_NO_CHOICE, default='True')
    show_fb_and_web = models.CharField(max_length=5, choices=YES_NO_CHOICE, default='False')
    show_time       = models.CharField(max_length=5, choices=YES_NO_CHOICE, default='True')
    password        = models.CharField(max_length=128, blank=True, null=True)
    pub_date        = models.DateTimeField(auto_now_add=True)
    slug            = models.SlugField(unique=False)

    class Meta:
        ordering = ['-solves', '-pub_date']

    def __str__(self):
        return self.title

    def get_section(self):
        return dict(self.SECTION).get(self.section)

    def get_category(self):
        return dict(self.CATEGORY).get(self.category)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.slug = self.slug[:50]

        if self.image_url == None or not(valid_url_extension(self.image_url)):
            self.image_url = self.DEFAULT_IMAGE_URL

        super(Quiz, self).save(*args, **kwargs)

class Question(models.Model):
    quiz            = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=False, blank=False, related_name='questions')
    question        = models.TextField(null=False, blank=False)
    image_url       = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.question

    def save(self, *args, **kwargs):
        if self.image_url == None or not(valid_url_extension(self.image_url)):
            self.image_url = ''

        return super(Question, self).save(*args, **kwargs)

class Answer(models.Model):
    question    = models.ForeignKey(Question, on_delete=models.CASCADE, null=False, blank=False, related_name='answers')
    answer      = models.TextField(null=False, blank=False)
    is_correct  = models.BooleanField(default=False)

    def __str__(self):
        return self.answer

class QuizOpinion(models.Model):
    quiz        = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='opinions')
    author      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='added_opinions')
    content     = models.TextField(blank=False, null=False, max_length=10000)
    likes       = models.ManyToManyField(User, blank=True, related_name='likes')
    reply       = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    pub_date    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content