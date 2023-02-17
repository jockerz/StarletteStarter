from fastapi.requests import Request


def get_user(request: Request):
    return request.user
