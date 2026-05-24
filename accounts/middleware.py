from django.utils import timezone


class RequestLoggerMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        path = request.path

        username = (
            request.user.username
            if request.user.is_authenticated
            else "AnonymousUser"
        )

        ip = request.META.get("REMOTE_ADDR")

        current_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

        log_message = (
            f"[{current_time}]\n"
            f"User: {username}\n"
            f"IP: {ip}\n"
            f"Path: {path}\n"
            f"{'-' * 40}\n"
        )

        with open("requests.log", "a", encoding="utf-8") as file:
            file.write(log_message)

        response = self.get_response(request)

        return response