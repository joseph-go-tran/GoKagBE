from rest_framework import permissions


class IsAuthorQuestionnaireOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(obj)
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return obj.author == request.user
        return True


class IsAuthorQuestionOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.questionnaire.author == request.user
