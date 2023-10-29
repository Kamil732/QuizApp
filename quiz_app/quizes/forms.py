from django import forms

from .models import Quiz

class CreateQuizForm(forms.ModelForm):
    title = forms.CharField(
        label = 'Title',
        required = True,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': 'Pass the title...',
            }
        )
    )

    section = forms.ChoiceField(
        label = 'Section',
        required = True,
        choices = Quiz.SECTION,
        widget = forms.Select(
            attrs = {
                'class': 'form-control',
            }
        )
    )

    category = forms.ChoiceField(
        label = 'Category',
        required = True,
        choices = Quiz.CATEGORY,
        widget = forms.Select(
            attrs = {
                'class': 'form-control',
            }
        )
    )

    description = forms.CharField(
        label = 'Description',
        required = False,
        widget = forms.Textarea(
            attrs = {
                'class': 'form-control',
                'rows': 9,
            }
        )
    )

    summary_text = forms.CharField(
        label = 'Summary text',
        required = False,
        widget = forms.Textarea(
            attrs = {
                'class': 'form-control',
                'placeholder': 'The summery text will be displayed on the screen after finished the quiz...',
                'rows': 4,
            }
        )
    )

    image_url = forms.URLField(
        label = 'Quiz logo url',
        required = False,
        widget = forms.URLInput(
            attrs = {
                'class': 'form-control',
            }
        )
    )

    is_published = forms.ChoiceField(
        required = True,
        choices = Quiz.IS_PUBLISHED,
        widget = forms.RadioSelect(
            attrs = {
                'autocomplete': 'off',
            }
        )
    )

    class Meta:
        model = Quiz
        fields = (
            'title',
            'section',
            'category',
            'description',
            'summary_text',
            'image_url',
            'is_published',
        )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CreateQuizForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        if self.is_valid():
            title = self.cleaned_data.get('title')
            try:
                Quiz.objects.get(title=title, author=self.user)
            except Quiz.DoesNotExist:
                return title
            raise forms.ValidationError('You have already created quiz named this title')

class QuizEditSettingsForm(forms.ModelForm):
    title = forms.CharField(
        label = 'Title',
        required = True,
        help_text = 'Give your quiz an interesting title',
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': 'Pass the title...',
            }
        )
    )

    section = forms.ChoiceField(
        label = 'Section',
        required = True,
        choices = Quiz.SECTION,
        widget = forms.Select(
            attrs = {
                'class': 'form-control',
            }
        )
    )

    category = forms.ChoiceField(
        label = 'Category',
        required = True,
        choices = Quiz.CATEGORY,
        widget = forms.Select(
            attrs = {
                'class': 'form-control',
            }
        )
    )

    description = forms.CharField(
        label = 'Description',
        required = False,
        widget = forms.Textarea(
            attrs = {
                'class': 'form-control',
                'rows': 5,
            }
        )
    )

    summary_text = forms.CharField(
        label = 'Summary text',
        required = False,
        widget = forms.Textarea(
            attrs = {
                'class': 'form-control',
                'placeholder': 'The summery text will be displayed on the screen after finished the quiz...',
                'rows': 4,
            }
        )
    )

    image_url = forms.URLField(
        label = 'Quiz logo url',
        required = False,
        widget = forms.URLInput(
            attrs = {
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = Quiz
        fields = (
            'title',
            'section',
            'category',
            'description',
            'image_url',
        )

class QuizEditPrivacyForm(forms.ModelForm):
    is_published = forms.ChoiceField(
        required = True,
        choices = Quiz.IS_PUBLISHED,
        widget = forms.RadioSelect(
            attrs = {
                'class': 'form-check-input',
                'autocomplete': 'off',
            }
        )
    )

    is_opinions = forms.ChoiceField(
        required = True,
        choices = Quiz.YES_NO_CHOICE,
        widget = forms.RadioSelect(
            attrs = {
                'class': 'form-check-input',
                'autocomplete': 'off',
            }
        )
    )

    show_fb_and_web = forms.ChoiceField(
        required = True,
        choices = Quiz.YES_NO_CHOICE,
        widget = forms.RadioSelect(
            attrs = {
                'class': 'form-check-input',
                'autocomplete': 'off',
            }
        )
    )

    show_time = forms.ChoiceField(
        required = True,
        choices = Quiz.YES_NO_CHOICE,
        widget = forms.RadioSelect(
            attrs = {
                'class': 'form-check-input',
                'autocomplete': 'off',
            }
        )
    )

    password = forms.CharField(
        label = 'Quiz password',
        required = False,
        help_text = 'If you add the password to your quiz, people will have to pass the passowrd to solve it.',
        widget = forms.PasswordInput(
            render_value = True,
            attrs = {
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = Quiz
        fields = (
            'is_published',
            'is_opinions',
            'show_fb_and_web',
            'show_time',
            'password',
        )