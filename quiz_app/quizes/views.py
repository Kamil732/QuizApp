import json

from math import ceil

from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.views import generic
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q

from users.models import User
from .models import Quiz, Question, Answer, QuizOpinion

from . import forms
from . import mixin
from .templatetags.time import get_time_difference

class QuizListView(generic.ListView):
    template_name = 'quizes/quiz_list.html'
    context_object_name = 'quizes'
    queryset = Quiz.objects.filter(is_published='True')[:10]

    def get_context_data(self, *args, **kwargs):
        context = super(QuizListView, self).get_context_data(*args, **kwargs)

        # Page count
        quizes = Quiz.objects.filter(is_published='True').count()
        context['page_items'] = ceil(quizes/10)

        context['quiz_sections'] = Quiz.SECTION
        context['quiz_categories'] = Quiz.CATEGORY

        return context

class QuizPageView(QuizListView):
    def get_queryset(self):
        page = self.kwargs.get('page')
        queryset = Quiz.objects.filter(is_published='True')[page*10-10:page*10]
        return queryset

class QuizSearchView(QuizListView):
    def post(self, *args, **kwargs):
        search = self.request.POST.get('search-quiz')
        self.queryset = Quiz.objects.filter(Q(title__icontains=search) | Q(category__icontains=search) | Q(section__icontains=search) | Q(description__icontains=search), is_published='True')

        return super(QuizSearchView, self).get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(QuizSearchView, self).get_context_data(*args, **kwargs)

        context['page_items'] = None

        return context

class QuizSortView(QuizListView):
    def get_context_data(self, *args, **kwargs):
        context = super(QuizSortView, self).get_context_data(*args, **kwargs)
        page = self.kwargs.get('page')
        search = self.kwargs.get('slug')

        quizes = Quiz.objects.filter(Q(category=search) | Q(section=search), is_published='True').count()
        context['page_items'] = ceil(quizes/10)

        context['search_slug'] = search
        context['quiz_sort_url'] = reverse('quizes:quiz-sort', args=[search, page])
        # context['quiz_sort_url'] = reverse('quizes:quiz-sort', args=[search])

        return context

    def get_queryset(self):
        search = self.kwargs.get('slug')
        page = self.kwargs.get('page')
        queryset = Quiz.objects.filter(Q(category=search) | Q(section=search), is_published='True')[page*10-10:page*10]

        return queryset

class MyQuizesListView(generic.ListView):
    template_name = 'quizes/my_quiz_list.html'
    context_object_name = 'quizes'

    def get_queryset(self):
        queryset = Quiz.objects.order_by('-pub_date').filter(author=self.request.user)
        return queryset

class QuizDetailView(mixin.QuizGetObjectBySlugMixin, generic.DetailView):
    template_name = 'quizes/quiz_detail.html'
    context_object_name = 'quiz'

    def get_context_data(self, **kwargs):
        context = super(QuizDetailView, self).get_context_data(**kwargs)
        quiz = self.get_object()

        similar_quizes = Quiz.objects.filter(is_published='True', category=quiz.category).exclude(id=quiz.id)[:10]
        context['similar_quizes'] = similar_quizes

        opinions = QuizOpinion.objects.order_by('-pub_date').filter(quiz=quiz, reply=None)
        context['opinions'] = opinions

        return context

class QuizSummaryView(mixin.QuizGetObjectByIdMixin, generic.DetailView):
    template_name = 'quizes/quiz_summary.html'
    context_object_name = 'quiz'

class QuizShowOpinionsView(mixin.QuizGetObjectByIdMixin, generic.DetailView):
    template_name = 'quizes/quiz_show_opinions.html'
    context_object_name = 'quiz'

    def get_context_data(self, *args, **kwargs):
        context = super(QuizShowOpinionsView, self).get_context_data(*args, **kwargs)

        opinions = QuizOpinion.objects.order_by('-pub_date').filter(quiz=self.get_object(), reply=None)
        context['opinions'] = opinions

        return context

class QuizStartView(mixin.QuizGetObjectBySlugMixin, generic.DetailView):
    template_name = 'quizes/quiz_start.html'
    context_object_name = 'quiz'

    def post(self, request, *args, **kwargs):
        quiz = self.get_object()
        if quiz.password:
            password = self.request.POST.get('password')
            # if not(quiz.password == password):
            if not(check_password(password, quiz.password)):
                messages.error(request, 'No quiz access. Wrong password')
                return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', '/'))
        return super(QuizStartView, self).get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        quiz = self.get_object()
        if not(quiz.password):
            return super(QuizStartView, self).get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('quizes:quiz-detail', args=[quiz.author, quiz.slug]))

class QuizEditSettingsView(mixin.QuizGetObjectByIdMixin, generic.UpdateView):
    template_name = 'quizes/quiz_edit_settings.html'
    context_object_name = 'quiz'
    form_class = forms.QuizEditSettingsForm

    def get_success_url(self):
        return self.request.path

    def get_initial(self, *args, **kwargs):
        initial = super(QuizEditSettingsView, self).get_initial(*args, **kwargs)
        if self.get_object().image_url == Quiz.DEFAULT_IMAGE_URL:
            initial['image_url'] = ''

        return initial

    def form_valid(self, form):
        messages.success(self.request, 'You have successfully saved your quiz settings')
        return super(QuizEditSettingsView, self).form_valid(form)

class QuizResultsView(mixin.QuizGetObjectBySlugMixin, generic.DetailView):
    template_name = 'quizes/quiz_results.html'
    context_object_name = 'quiz'

    def post(self, request, *args, **kwargs):
        quiz = self.get_object()
        context = {}

        # Get points
        points = 0
        for question in quiz.questions.all():
            choosen_answer = request.POST.get('answer' + str(question.id))

            for answer in question.answers.all():
                if answer.answer == choosen_answer:
                    if answer.is_correct:
                        points += 1

        # Add SOLVES COUNT to the quiz
        if request.user.is_authenticated and not(request.user == quiz.author):
            user = request.user
            user.solves += 1
            user.save()

            quiz.solves += 1
            quiz.save()

        # Set context data
        context['points'] = points
        context['quiz'] = quiz

        # Get minutes and seconds of stopwatch
        if quiz.show_time:
            try:
                time = int(request.POST.get('timer'))
                minutes = str(time//60)
                seconds = str(time-(time//60 * 60))
            except:
                minutes = '59'
                seconds = '59'

            context['minutes'] = minutes
            context['seconds'] = seconds

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return redirect('/')

class QuizEditPrivacyView(mixin.QuizGetObjectByIdMixin, generic.UpdateView):
    template_name = 'quizes/quiz_edit_privacy.html'
    context_object_name = 'quiz'
    form_class = forms.QuizEditPrivacyForm

    def form_valid(self, form):
        quiz = form.save(commit=False)

        password = form.cleaned_data.get('password')

        if password:
            quiz.password = make_password(password)

            if quiz.is_published == 'True':
                quiz.is_published = 'False'
                messages.info(self.request, "You've added password so the quiz's available has changed to private")
        else:
            quiz.password = None
        quiz.save()

        messages.success(self.request, 'You have successfully saved your quiz privacy')
        return super(QuizEditPrivacyView, self).form_valid(form)

    def get_initial(self, *args, **kwargs):
        initial = super(QuizEditPrivacyView, self).get_initial(*args, **kwargs)
        initial['password'] = ''

        return initial

    def get_success_url(self):
        return self.request.path

class QuizDeleteView(mixin.QuizGetObjectByIdMixin, generic.View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            quiz = self.get_object()
            quiz.delete()

            return HttpResponse(json.dumps({ 'message': 'success' }), content_type='application/json')
        raise Http404

class CreateQuizOpinion(generic.View):
    def post(self, request, id):
        quiz = get_object_or_404(Quiz, id=id)

        if request.is_ajax() and request.POST:
            content = request.POST.get('opinion-content')
            if content.strip() == '':
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            opinion = QuizOpinion.objects.create(quiz=quiz, author=request.user, content=content)
            data = {
                'message': 'Your opinions has been successfully added',
                'content': content,
                'author': request.user.username,
                'author_image_url': request.user.image_url,
                'opinion_id': opinion.id,
                'like_opinion_url': reverse('quizes:opinion-like', args=[quiz.id, opinion.id]),
                'reply_opinion_url': reverse('quizes:opinion-add-reply', args=[quiz.id, opinion.id]),
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            raise Http404

class ReplyOpinionView(generic.View):
    def post(self, request, id, opinion_id):
        quiz = get_object_or_404(Quiz, id=id)
        opinion = get_object_or_404(QuizOpinion, id=opinion_id)

        if request.is_ajax() and request.POST:
            reply_content = request.POST.get('reply-content')
            if reply_content.strip() == '':
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            QuizOpinion.objects.create(quiz=quiz, author=request.user, content=reply_content, reply=opinion)

            data = {
                'content': reply_content,
            }

            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            raise Http404

class GetOpinionRepliesView(generic.View):
    def get(self, request, id, opinion_id):
        quiz = get_object_or_404(Quiz, id=id)
        opinion = get_object_or_404(QuizOpinion, id=opinion_id)

        if request.is_ajax():
            replies = opinion.replies.order_by('pub_date').values_list('id', 'content', 'author__username', 'author__image_url',)
            data = {}

            try:
                data['replies'] = list(replies)
                for reply in data['replies']:
                    opinion_reply = QuizOpinion.objects.get(id=reply[0])
                    data['get_time_difference_' + str(reply[0])] = get_time_difference(opinion_reply.pub_date)

                data['get_replies_url'] = reverse('quizes:opinion-get-replies', args=[quiz.id, opinion.id])
                data['replies_count'] = opinion.replies.count()
            except:
                data['replies'] = 'Error'

            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            raise Http404

class LikeOpinionView(generic.View):
    def get(self, request, id, opinion_id):
        quiz = get_object_or_404(Quiz, id=id)
        opinion = get_object_or_404(QuizOpinion, id=opinion_id)

        if request.is_ajax():
            user = request.user
            data = {}
            if opinion.likes.filter(id=user.id).exists():
                opinion.likes.remove(user)
                data['image'] = 'like'
            else:
                opinion.likes.add(user)
                data['image'] = 'liked'

            data['opinion_id'] = opinion.id
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            raise Http404

class CreateQuizView(generic.CreateView):
    template_name = 'quizes/quiz_create.html'

    def get_form(self):
        user = self.request.user
        form = forms.CreateQuizForm(user, self.request.POST)
        if self.request.method == 'GET':
            form = forms.CreateQuizForm(user, initial=self.get_initial())
        return form

    def form_valid(self, form):
        self.quiz = form.save(commit=False)
        self.quiz.author = self.request.user
        self.quiz.save()

        return super(CreateQuizView, self).form_valid(form)


    def get_initial(self, *args, **kwargs):
        initial = super(CreateQuizView, self).get_initial(*args, **kwargs)

        initial['description'] = 'Welcome to my quiz!'
        initial['is_published'] = 'True'

        return initial

    def get_success_url(self):
        return reverse('quizes:quiz-add-question', args=[self.quiz.id])

class QuizAddQuestionView(mixin.QuizGetObjectByIdMixin, generic.DetailView):
    template_name = 'quizes/quiz_add_questions.html'
    context_object_name = 'quiz'

    def post(self, request, *args, **kwargs):
        quiz = self.get_object()
        question_text = request.POST.get('question')
        image_url = request.POST.get('image_url')
        answer_count = int(request.POST.get('answer_count'))
        answers = [request.POST.get('answer'+ str(i)) for i in range(1, answer_count+1)]
        correct_answer_id = int(request.POST.get('is_correct'))

        # Check if entried values are not empty
        for answer in answers:
            if answer == '' or question_text == '':
                messages.error(request, "Not valid question's options or question field")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        # Create question and answers
        question = Question.objects.create(quiz=quiz, question=question_text, image_url=image_url)
        for answer_text in answers:
            answer = Answer.objects.create(question=question, answer=answer_text)
            if answer.answer == answers[correct_answer_id-1]:
                answer.is_correct = True
                answer.save()
        messages.success(request, 'The question has been successfully added')

        return super(QuizAddQuestionView, self).get(request, *args, **kwargs)

class QuizShowQuestionsView(mixin.QuizGetObjectByIdMixin, generic.ListView):
    template_name = 'quizes/quiz_show_questions.html'
    context_object_name = 'questions'

    def get_context_data(self, *args, **kwargs):
        context = super(QuizShowQuestionsView, self).get_context_data(*args, **kwargs)
        context['quiz'] = self.get_object()

        return context

    def get_queryset(self):
        quiz = self.get_object()
        questions = quiz.questions.all()

        return questions

class QuestionDeleteView(mixin.QuizGetObjectByIdMixin, generic.View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            question_id = self.kwargs.get('question_id')
            question = get_object_or_404(Question, id=question_id)

            question.delete()

            return HttpResponse(json.dumps({ 'message': 'success' }), content_type='application/json')
        raise Http404