from .models import Questionnaire, Question, InputType, SelectType, OptionValue, Statistics
from django.contrib import admin

admin.site.register(Questionnaire)
admin.site.register(Question)
admin.site.register(InputType)
admin.site.register(SelectType)
admin.site.register(OptionValue)
admin.site.register(Statistics)
