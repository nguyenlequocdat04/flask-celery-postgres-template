# requirements.txt
#   google-api-python-client
import os
import pydash as py_
from enum import Enum

from google.oauth2 import service_account
from googleapiclient.discovery import build

from .exceptions import RespMsg


class SubscriptionState(Enum):
    """
    Docs: https://developers.google.com/android-publisher/api-ref/rest/v3/purchases.subscriptionsv2#SubscriptionState
    """
    SUBSCRIPTION_STATE_UNSPECIFIED = 'SUBSCRIPTION_STATE_UNSPECIFIED'
    SUBSCRIPTION_STATE_PENDING = 'SUBSCRIPTION_STATE_PENDING'
    SUBSCRIPTION_STATE_ACTIVE = 'SUBSCRIPTION_STATE_ACTIVE'
    SUBSCRIPTION_STATE_PAUSED = 'SUBSCRIPTION_STATE_PAUSED'
    SUBSCRIPTION_STATE_IN_GRACE_PERIOD = 'SUBSCRIPTION_STATE_IN_GRACE_PERIOD'
    SUBSCRIPTION_STATE_ON_HOLD = 'SUBSCRIPTION_STATE_ON_HOLD'
    SUBSCRIPTION_STATE_CANCELED = 'SUBSCRIPTION_STATE_CANCELED'
    SUBSCRIPTION_STATE_EXPIRED = 'SUBSCRIPTION_STATE_EXPIRED'


class SVC_GPA(object):
    """
    Docs:
    - Main: https://developer.android.com/google/play/billing
    - Purchase IAP: https://developers.google.com/android-publisher/api-ref/rest/v3/purchases.products
    - Purchase Subcriptions: https://developers.google.com/android-publisher/api-ref/rest/v3/purchases.subscriptionsv2/get
    - Service account file: https://docs.adapty.io/docs/service-account-key-file
    """

    SUBSCRIPTION_STATE_ALLOWS = [
        SubscriptionState.SUBSCRIPTION_STATE_ACTIVE,
        # SubscriptionState.SUBSCRIPTION_STATE_IN_GRACE_PERIOD, # On FirstTime only ACTIVE is APPLY
    ]

    def __init__(self, path_service_account_file='') -> None:
        # Define the service account credentials and API scope
        SCOPES = ['https://www.googleapis.com/auth/androidpublisher']

        if not path_service_account_file:
            path_service_account_file = os.getenv('GPA_SERVICE_ACCOUNT')

        if not path_service_account_file:
            raise Exception("Require service_account check here (https://docs.adapty.io/docs/service-account-key-file)")

        self.package_name = os.getenv('GPA_PACKAGE_NAME')

        self.credentials = service_account.Credentials.from_service_account_file(
            path_service_account_file,
            scopes=SCOPES
        )
        self.androidpublisher = build('androidpublisher', 'v3', credentials=self.credentials)

    def get_subscription_receipt(self, token, package_name=''):
        """
        Response Sample:
        {
            "kind": "androidpublisher#subscriptionPurchaseV2",
            "startTime": "2023-04-05T05:14:32.874Z",
            "regionCode": "VN",
            "subscriptionState": "SUBSCRIPTION_STATE_ACTIVE",
            "latestOrderId": "GPA.3349-4454-9294-38157",
            "testPurchase": {},
            "acknowledgementState": "ACKNOWLEDGEMENT_STATE_ACKNOWLEDGED",
            "lineItems": [
                {
                    "productId": "iap_sub_year",
                    "expiryTime": "2023-04-05T05:44:29.723Z",
                    "autoRenewingPlan": {
                        "autoRenewEnabled": true
                    },
                    "offerDetails": {
                        "basePlanId": "yearly"
                    }
                }
            ]
        }
        """
        if not package_name:
            package_name = self.package_name

        subcription = self.androidpublisher.purchases().subscriptionsv2().get(
            packageName=package_name,
            token=token
        ).execute()
        return subcription

    def validate_onetime_product_receipt(self, obj):
        pass
