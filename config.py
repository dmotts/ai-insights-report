import os
import logging
from distutils.util import strtobool

class Config:
    # Google Sheets Configuration
    GOOGLE_SHEETS_CREDENTIALS_JSON = os.getenv('GOOGLE_SHEETS_CREDENTIALS_JSON', 'credentials.json')
    SHEET_NAME = os.getenv('SHEET_NAME', 'ReportData')
    GOOGLE_DRIVE_FOLDER_NAME = os.getenv('GOOGLE_DRIVE_FOLDER_NAME', 'AI_Reports')

    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
    logging.basicConfig(level=LOG_LEVEL)

    # LLM Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    LLM_MODEL = os.getenv('LLM_MODEL')
    USE_OPENAI_API = strtobool(os.getenv('USE_OPENAI_API', 'True'))

    # PDF.co Configuration
    PDFCO_API_KEY = os.getenv('PDFCO_API_KEY')

    # Gmail Configuration
    GMAIL_ADDRESS = os.getenv('GMAIL_ADDRESS', '')
    GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD', '')

    # Notification Email
    NOTIFICATION_EMAIL = os.getenv('NOTIFICATION_EMAIL', 'daley.mottley@hotmail.com')

    # Firestore Configuration
    FIRESTORE_CREDENTIALS_JSON = os.getenv('FIRESTORE_CREDENTIALS_JSON', 'path_to_firestore_credentials.json')
    FIRESTORE_PROJECT_ID = os.getenv('FIRESTORE_PROJECT_ID', 'your-firestore-project-id')

    # Feature Flags to enable/disable services
    ENABLE_DATABASE = strtobool(os.getenv('ENABLE_DATABASE', 'True'))
    ENABLE_EMAIL_SERVICE = strtobool(os.getenv('ENABLE_EMAIL_SERVICE', 'True'))
    ENABLE_LLM_SERVICE = strtobool(os.getenv('ENABLE_LLM_SERVICE', 'True'))
    ENABLE_PDF_SERVICE = strtobool(os.getenv('ENABLE_PDF_SERVICE', 'True'))
    ENABLE_SHEETS_SERVICE = strtobool(os.getenv('ENABLE_SHEETS_SERVICE', 'True'))
    ENABLE_INTEGRATION_SERVICE = strtobool(os.getenv('ENABLE_INTEGRATION_SERVICE', 'True'))
    ENABLE_SUBSCRIPTION_SERVICE = strtobool(os.getenv('ENABLE_SUBSCRIPTION_SERVICE', 'True'))

    @classmethod
    def validate_config(cls):
        """Raise errors if critical configurations are missing."""
        if cls.ENABLE_LLM_SERVICE and not cls.OPENAI_API_KEY:
            raise ValueError("LLM_API_KEY must be set in the environment.")
        if not cls.PDFCO_API_KEY:
            raise ValueError("PDFCO_API_KEY must be set in the environment.")
        if cls.ENABLE_EMAIL_SERVICE and (not cls.GMAIL_ADDRESS or not cls.GMAIL_APP_PASSWORD):
            raise ValueError("GMAIL_ADDRESS and GMAIL_APP_PASSWORD must be set in the environment.")
        if cls.ENABLE_DATABASE and not cls.FIRESTORE_CREDENTIALS_JSON:
            raise ValueError("FIRESTORE_CREDENTIALS_JSON must be set in the environment.")

# Validate configuration on startup
Config.validate_config()
