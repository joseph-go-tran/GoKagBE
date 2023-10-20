from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data["status_code"] = response.status_code

    return response


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = "Service temporarily unavailable, try again later."
    default_code = "service_unavailable"


class AvatarRequireExcepion(APIException):
    status_code = 400
    default_detail = "Avatar image is required!"
    default_code = "avatar_required"


class ThumbRequireExcepion(APIException):
    status_code = 400
    default_detail = "Thumb image is required!"
    default_code = "thumb_required"


class FileUploadRequireExcepion(APIException):
    status_code = 400
    default_detail = "File upload is required!"
    default_code = "file_upload_required"


class QuestionnaireIdRequireExcepion(APIException):
    status_code = 400
    default_detail = "Questionnaire id query params is required!"
    default_code = "questionnaire_id_required"


class RefreshTokenRequireExcepion(APIException):
    status_code = 400
    default_detail = "Refresh token is required."
    default_code = "refresh_token_required"


class EmailAndPasswordRequireExcepion(APIException):
    status_code = 400
    default_detail = "Email and password are required fields!"
    default_code = "email_password_required"


class LoginFailedExcepion(APIException):
    status_code = 401
    default_detail = "Authentication failed. Invalid email or password."
    default_code = "login_failed"


class SendEmailExcepion(APIException):
    status_code = 400
    default_detail = """Can not send an email verification to your email address!
    Please check and try again!"""
    default_code = "email_send_failed"


class PermissionDeniedException(APIException):
    status_code = 403
    default_detail = "You don't have permission to update this questionnaire."
    default_code = "permission_denied"


class AnswerNotEnoughException(APIException):
    status_code = 400
    default_detail = "Answer not enough number of questions."
    default_code = "answer_not_enough"
