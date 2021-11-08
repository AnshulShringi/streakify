from firebase_admin import auth
from rest_framework import status
from rest_framework.response import Response


def token_retrieve_possible(view_func):
    def wrap_func(request, *args, **kwargs):
        firebase_token = request.data.get("firebase_token")
        mobile_number = request.data.get("mobile_number")
        country_code = request.data.get("country_code")

        # Check if credentials are missing
        if (firebase_token is None) or (mobile_number is None) or (country_code is None):
            return Response(
                {
                    "detail": "Missing credentials! firebase_token, mobile_number and \
                               country_code required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            try:
                # Check if user is verified
                firebase_user = auth.verify_id_token(firebase_token)
            except Exception:
                return Response(
                    {"detail": "Firebase token invalid/expired."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Check if given credentials match with firebase account
        phone_number = country_code + mobile_number
        if phone_number != firebase_user["phone_number"]:
            return Response(
                {
                    "detail": "Invalid credentials! country_code or mobile_number \
                               doesn't match with firebase account."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return view_func(request, *args, **kwargs)

    wrap_func.__doc__ = view_func.__doc__
    return wrap_func
