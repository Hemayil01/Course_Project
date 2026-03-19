from django.contrib.auth import get_user_model

User = get_user_model()


def has_role(user, role):
    if not user or not user.is_authenticated:
        return False
    return user.role == role


def has_any_role(user, roles):
    if not user or not user.is_authenticated:
        return False
    return user.role in roles


def is_admin(user):
    return has_role(user, 'admin')


def is_instructor(user):
    return has_role(user, 'instructor')


def is_student(user):
    return has_role(user, 'student')


def is_instructor_or_admin(user):
    return has_any_role(user, ['instructor', 'admin'])



def can_manage_courses(user):
    if not user or not user.is_authenticated:
        return False

    if user.role in ['admin', 'instructor']:
        return True
    elif user.role == 'student':
        return False

    return False


def can_manage_lessons(user):
    if not user or not user.is_authenticated:
        return False

    if user.role in ['admin', 'instructor']:
        return True
    elif user.role == 'student':
        return False

    return False


def can_manage_enrollments(user):
    if not user or not user.is_authenticated:
        return False

    if user.role in ['admin', 'instructor']:
        return True
    elif user.role == 'student':
        return False

    return False


def can_manage_progress(user):
    if not user or not user.is_authenticated:
        return False
    
    if user.role == 'student':
        return True
    elif user.role in ['instructor', 'admin']:
        return True

    return False



def get_user_permissions(user):
    if not user or not user.is_authenticated:
        return {
            'can_view_courses': False,
            'can_create_courses': False,
            'can_update_courses': False,
            'can_delete_courses': False,
            'can_manage_lessons': False,
            'can_manage_enrollments': False,
            'can_manage_progress': False,
        }

    return {
        'can_view_courses': True,
        'can_create_courses': can_manage_courses(user),
        'can_update_courses': can_manage_courses(user),
        'can_delete_courses': can_manage_courses(user),
        'can_manage_lessons': can_manage_lessons(user),
        'can_manage_enrollments': can_manage_enrollments(user),
        'can_manage_progress': can_manage_progress(user),
    }