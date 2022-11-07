from .firebase_admin import auth

def get_user_count():
    count = 0
    for _ in auth.list_users().iterate_all():
        count += 1
    return count

def get_admin_count():
    count = 0
    for user in auth.list_users().iterate_all():
        try:
            _ = user.custom_claims["admin"]
            count += 1
        except TypeError:
            pass
    return count

def get_blocked_user_count():
    count = 0
    for user in auth.list_users().iterate_all():
        if user.disabled:
            count += 1
    return count
