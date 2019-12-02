from selenium.webdriver import Remote
from pytest import fixture
from tests.pages import *
from tests.params import *


@step("Открыть Gmail")
def open_gmail(webdriver):
    webdriver.get(Params.gmail_url())
    return LoginPage(webdriver)


@fixture
def remote_webdriver(request):
    wd = Remote(Params.webdriver_url(), desired_capabilities = {
        'platform': Params.webdriver_platform(),
        'browserName': Params.webdriver_browser(),
        'version': Params.webdriver_version(),
    })
    request.addfinalizer(wd.close)
    return wd


@step("Сообщение отправляется успешно")
def test_mail_send_success(remote_webdriver):
    main_page = open_gmail(remote_webdriver) \
        .login(Params.gmail_username(), Params.gmail_password())
    main_page \
        .open_write_message() \
        .fill_message(Params.gmail_message_to(), Params.gmail_message_subject(), Params.gmail_message_body()) \
        .send_message()
    main_page.get_notification().check_message_send()


@step("Отправка сообщение падает с ошибкой, если не задать невалидный адрес получателя")
def test_mail_send_with_invalid_recipient_fail(remote_webdriver):
    invalid_recipient = "124567"

    main_page = open_gmail(remote_webdriver) \
        .login(Params.gmail_username(), Params.gmail_password())

    main_page \
        .open_write_message() \
        .fill_message(invalid_recipient, Params.gmail_message_subject(), Params.gmail_message_body()) \
        .send_message()
    main_page.get_alert().check_error_message("Адрес " + invalid_recipient + " в поле Кому не распознан. Проверьте правильность ввода всех адресов.")


@step("Отправка сообщение падает с ошибкой, если не задать пустой адрес получателя")
def test_mail_send_with_empty_recipient_fail(remote_webdriver):
    main_page = open_gmail(remote_webdriver) \
        .login(Params.gmail_username(), Params.gmail_password())

    main_page \
        .open_write_message() \
        .fill_message("", Params.gmail_message_subject(), Params.gmail_message_body()) \
        .send_message()
    main_page.get_alert().check_error_message("Укажите как минимум одного получателя.")
