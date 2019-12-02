from os import environ


class Params:

    @staticmethod
    def webdriver_url():
        return environ["WD_URL"]

    @staticmethod
    def webdriver_platform():
        return environ["WD_PLATFORM"]

    @staticmethod
    def webdriver_browser():
        return environ["WD_BROWSER"]

    @staticmethod
    def webdriver_version():
        return environ["WD_BROWSER_VERSION"]

    @staticmethod
    def gmail_url():
        return environ["GMAIL_URL"] if "GMAIL_URL" in environ else "https://gmail.com"

    @staticmethod
    def gmail_username():
        return environ["GMAIL_USERNAME"]

    @staticmethod
    def gmail_password():
        return environ["GMAIL_PASSWORD"]

    @staticmethod
    def gmail_message_to():
        return environ["GMAIL_MESSAGE_TO"] if "GMAIL_MESSAGE_TO" in environ else Params.gmail_username()

    @staticmethod
    def gmail_message_subject():
        return environ["GMAIL_MESSAGE_SUBJECT"] if "GMAIL_MESSAGE_SUBJECT" in environ else "Test Subject"

    @staticmethod
    def gmail_message_body():
        return environ["GMAIL_MESSAGE_BODY"] if "GMAIL_MESSAGE_BODY" in environ else "Test Body"
