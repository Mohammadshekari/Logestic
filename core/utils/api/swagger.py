from functools import wraps

def handle_swagger_fake_view(view_func):
    @wraps(view_func)
    def wrapper(self, *args, **kwargs):
        if getattr(self, "swagger_fake_view", False):
            # Return None for schema generation metadata
            return None
        return view_func(self, *args, **kwargs)
    return wrapper