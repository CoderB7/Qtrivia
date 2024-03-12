from django import forms
from .models import Quiz

CATEGORY_CHOICES_2 = [
                 ("", "Any Category"), (9, "General Knowledge"), (10, "Entertainment: Books"), (11, "Entertainment: Film"),
                 (12, "Entertainment: Music"), (13, "Entertainment: Musicals & Theatres"),
                 (14, "Entertainment: Television"), (15, "Entertainment: Video Games"),
                 (16, "Entertainment: Board Games"), (17, "Science & Nature"),
                 (18, "Science: Computers"), (19, "Science: Mathematics"), (20, "Mythology"), (21, "Sports"),
                 (22, "Geography"), (23, "History"), (24, "Politics"),
                 (25, "Art"), (26, "Celebrities"), (27, "Animals"), (28, "Vehicles"), (29, "Entertainment: Comics"),
                 (30, "Science: Gadgets"),
                 (31, "Entertainment: Japanese Anime & Manga"), (32, "Entertainment: Cartoon & Animations")
]

DIFFICULTY_CHOICES_2 = [
    ("", "Any Difficulty"), ("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")
]

TYPE_CHOICES_2 = [
    ("", "Any Type"), ("multiple", "Multiple Choice"), ("boolean", "True / False")
]

CATEGORY_CHOICES_1 = [
    ("music", "Music"), ("sport_and_leisure", "Sport and Leisure"), ("film_and_tv", "Film and TV"),
    ("arts_and_literature", "Arts and Literature"), ("history", "History"),
    ("society_and_culture", "Society and Culture"), ("science", "Science"),
    ("geography", "Geography"), ("food_and_drink", "Food and Drink"),
    ("general_knowledge", "General Knowledge")
]

DIFFICULTY_CHOICES_1 = [
    ("", "Any Difficulty"), ("easy", "Easy"), ("medium", "Medium"),
    ("hard", "Hard")
]

TYPE_CHOICES_1 = [
    ("", "Any Type"), ("text_choice", "Text Choice")
]


class ConfigForm1(forms.ModelForm):  # TheTriviaAPI
    amount = forms.IntegerField(
        label='Number of Questions:',
        widget=forms.NumberInput(
            attrs={
                'class': "form-control",
                'style': 'max-width: 300px',
            }
        )
    )
    category = forms.ChoiceField(
        label='Select Category:',
        choices=CATEGORY_CHOICES_1,
        widget=forms.Select(
            attrs={
                'class': "form-control",
                'style': 'max-width: 300px',
            }
        )
    )
    difficulty = forms.ChoiceField(
        label='Select Difficulty:',
        choices=DIFFICULTY_CHOICES_1,
        widget=forms.Select(
            attrs={
                'class': "form-control",
                'style': 'max-width: 300px',
            }
        )
    )
    type = forms.ChoiceField(
        label='Select Type:',
        choices=TYPE_CHOICES_1,
        widget=forms.Select(
            attrs={
                'class': "form-control",
                'style': 'max-width: 300px',
            }
        )
    )

    class Meta:
        model = Quiz
        fields = ['amount', 'category', 'difficulty', 'type']


class ConfigForm2(forms.ModelForm):  # OpenTDAPI
    amount = forms.IntegerField(
        label='Number of Questions:',
        widget=forms.NumberInput(
            attrs={
                'class': "form-control",
                'style': 'max-width: 300px',
            }
        )
    )
    category = forms.ChoiceField(
        label='Select Category:',
        choices=CATEGORY_CHOICES_2,
        widget=forms.Select(
            attrs={
                'class': "form-control",
                'style': 'max-width: 300px',
            }
        )
    )
    difficulty = forms.ChoiceField(
        label='Select Difficulty:',
        choices=DIFFICULTY_CHOICES_2,
        widget=forms.Select(
            attrs={
                'class': "form-control",
                'style': 'max-width: 300px',
            }
        )
    )
    type = forms.ChoiceField(
        label='Select Type:',
        choices=TYPE_CHOICES_2,
        widget=forms.Select(
            attrs={
                'class': "form-control",
                'style': 'max-width: 300px',
            }
        )
    )

    class Meta:
        model = Quiz
        fields = ['amount', 'category', 'difficulty', 'type']
