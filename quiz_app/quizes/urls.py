from django.urls import path, include

from django.contrib.auth.decorators import login_required

from .models import Quiz
from . import views

app_name = 'quizes'
urlpatterns = (
    path('', views.QuizListView.as_view(), name='quiz-list'),
    path('quiz/', include([
        path('page/<int:page>', views.QuizPageView.as_view(), name='page'),
        path('search/', include([
            path('', views.QuizSearchView.as_view(), name='search-quiz'),
            path('<slug:slug>/<int:page>', views.QuizSortView.as_view(), name='quiz-sort'),
        ])),
        path('my-quizes/', include([
            path('', login_required(views.MyQuizesListView.as_view(), login_url='users:login'), name='my-quiz-list'),
            path('create/', login_required(views.CreateQuizView.as_view(), login_url='users:login'), name='create-quiz'),
            path('<int:id>/', include([
                path('summary', login_required(views.QuizSummaryView.as_view(), login_url='users:login'), name='quiz-summary'),
                path('edit/', include([
                    path('settings', login_required(views.QuizEditSettingsView.as_view(), login_url='users:login'), name='quiz-edit-settings'),
                    path('privacy', login_required(views.QuizEditPrivacyView.as_view(), login_url='users:login'), name='quiz-edit-privacy'),
                ])),
                path('questions/', include([
                    path('show', login_required(views.QuizShowQuestionsView.as_view(), login_url='users:login'), name='quiz-show-questions'),
                    path('add', login_required(views.QuizAddQuestionView.as_view(), login_url='users:login'), name='quiz-add-question'),
                    path('<int:question_id>/', include([
                        path('delete', login_required(views.QuestionDeleteView.as_view(), login_url='users:login'), name='delete-question'),
                    ])),
                ])),
                path('show-opinions', login_required(views.QuizShowOpinionsView.as_view(), login_url='users:login'), name='quiz-show-opinions'),
                path('delete', login_required(views.QuizDeleteView.as_view(), login_url='users:login'), name='quiz-delete'),
            ])),
        ])),
        path('<slug:author>/', include([
            path('<slug:quiz>/', include([
                path('', views.QuizDetailView.as_view(), name='quiz-detail'),
                path('start', views.QuizStartView.as_view(), name='quiz-start'),
                path('results', views.QuizResultsView.as_view(), name='quiz-end'),
            ])),
        ])),
        path('<int:id>/', include([
            path('opinions/', include([
                path('add', login_required(views.CreateQuizOpinion.as_view(), login_url='users:login'), name='opinion-add'),
                path('<int:opinion_id>/', include([
                    path('like', login_required(views.LikeOpinionView.as_view(), login_url='users:login'), name='opinion-like'),
                    path('add-reply', login_required(views.ReplyOpinionView.as_view(), login_url='users:login'), name='opinion-add-reply'),
                    path('get-replies', views.GetOpinionRepliesView.as_view(), name='opinion-get-replies'),
                ])),
            ])),
        ])),
    ])),
)