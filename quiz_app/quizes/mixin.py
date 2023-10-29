from django.shortcuts import get_object_or_404
from django.http import Http404

from users.models import User
from .models import Quiz, Question

class QuizGetObjectBySlugMixin(object):
    def get_object(self):
        author_slug = self.kwargs.get('author')
        quiz_slug = self.kwargs.get('quiz')
        author = get_object_or_404(User, slug=author_slug)

        return get_object_or_404(Quiz, author=author, slug=quiz_slug)

class QuizGetObjectByIdMixin(object):
    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Quiz, id=id)

    def get_template_names(self):
        if not(self.get_object().author == self.request.user):
            raise Http404
        return self.template_name