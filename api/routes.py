from rest_framework.routers import DefaultRouter

from authentication.views import UserViewSet
from datasets.views.views_answer import AnswerViewSet
from datasets.views.views_datasets import DatasetsViewSet
from questionnaire.views.views_quesionnaire import QuestionnaireViewSet
from questionnaire.views.views_question import QuestionViewSet
from upload.views import UploadViewSet

router = DefaultRouter()
router.register("auth", UserViewSet, basename="auth")
router.register(
    "questionnaire", QuestionnaireViewSet, basename="questionnaire"
)
router.register("question", QuestionViewSet, basename="question")
router.register("answer", AnswerViewSet, basename="answer")
router.register("datasets", DatasetsViewSet, basename="datasets")
router.register("upload", UploadViewSet, basename="upload")

urlpatterns = router.urls
