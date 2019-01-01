from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    객체의 소유자에게만 쓰기를 허용하는 커스텀 권한
    """

    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모두에게 허용,
        # GET, HEAD, OPTION 요청은 항상 허용함
        if request.method in permissions.SAFE_METHODS:
            return True

        # 쓰기 권한은 DB에 연동된 소유자에게만 부여
        return obj.owner == request.user