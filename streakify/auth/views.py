import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import firebase_admin


firebase_config = os.environ['firebase_config']
firebase = firebase_admin.initializeApp(firebaseConfig)
auth = firebase.auth().useDeviceLanguage()


class GetOtpView(APIView):
    pass


class VerifyOtpView(APIView):
    pass
