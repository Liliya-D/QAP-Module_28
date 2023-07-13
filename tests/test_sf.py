
import pytest
from pages.auth_page import AuthPage, CodeForm
from pages.registr_page import RegistrPage
from pages.locators import AuthLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import *

def test_general_view(selenium):
    """Общий вид формы (сохранить скриншот)."""
    form = AuthPage(selenium)
    form.driver.save_screenshot('screen_01.jpg')

def test_2_screen(selenium):
    """Проверка открытия формы для получения временного кода"""
    form = CodeForm(selenium)
    form.driver.save_screenshot('screen_02.png')


def test_menu_of_type_active_autoriz(selenium):
    """Проверка выбора таба по умолчанию в Меню выбора типа авторизации."""
    page = AuthPage(selenium)
    
    assert page.active_tub_phone.text == Settings.menu_type_auth[0]


def test_elements_of_autoriz(selenium):
    """Проверка раздела "Авторизация" на наличие основных элементов."""
    page = AuthPage(selenium)

    assert page.menu_tub.text in page.card_of_auth.text
    assert page.email.text in page.card_of_auth.text
    assert page.pass_eml.text in page.card_of_auth.text
    assert page.btn_enter.text in page.card_of_auth.text
    assert page.forgot_password_link.text in page.card_of_auth.text
    assert page.register_link.text in page.card_of_auth.text


def test_menu_type_autoriz(selenium):
    """Проверка названия табов в меню выбора типа авторизации."""
    try:
        page = AuthPage(selenium)
        menu = [page.tub_phone.text, page.tub_email.text, page.tub_login.text, page.tub_ls.text]
        for i in range(len(menu)):
            assert "Номер" in menu
            assert 'Почта' in menu
            assert 'Логин' in menu
            assert 'Лицевой счёт' in menu
    except AssertionError:
        print('Ошибка в имени таба Меню типа аутентификации')


def test_placeholder_name_swap(selenium):
    """Тест смены полей ввода при смене типа авторизации."""
    page = AuthPage(selenium)
    page.tub_phone.click()

    assert page.placeholder_name.text in Settings.placeholder_name
    page.tub_email.click()
    assert page.placeholder_name.text in Settings.placeholder_name
    page.tub_login.click()
    assert page.placeholder_name.text in Settings.placeholder_name
    page.tub_ls.click()
    assert page.placeholder_name.text in Settings.placeholder_name
    
    
def test_forgot_password_link(selenium):
    """Переход к форме "Восстановление пароля"."""
    page = AuthPage(selenium)
    page.driver.execute_script("arguments[0].click();", page.forgot_password_link)

    assert page.find_other_element(*AuthLocators.password_recovery).text == 'Восстановление пароля'


def test_page_logo_registration(selenium):
    """Переход к форме "Регистрация"."""
    page = AuthPage(selenium)
    page.register_link.click()

    assert page.find_other_element(*AuthLocators.registration).text == 'Регистрация'

    """Проверка блока с логотипон/названием компании на странице "Регистрация"."""
    try:
        page_reg = RegistrPage(selenium)
        assert page_reg.page_left_registration.text != ''
    except AssertionError:
        print('Элемент отсутствует в левой части формы')


def test_elements_registration(selenium):
    """Проверка Формы "Регистрация" на наличие основных элементов."""
    try:
        page_reg = RegistrPage(selenium)
        card_of_reg = [page_reg.first_name, page_reg.last_name, page_reg.address_registration,
                       page_reg.email_registration, page_reg.password_registration,
                       page_reg.password_registration_confirm, page_reg.registration_btn]
        for i in range(len(card_of_reg)):
            assert page_reg.first_name in card_of_reg
            assert page_reg.last_name in card_of_reg
            assert page_reg.email_registration in card_of_reg
            assert page_reg.address_registration in card_of_reg
            assert page_reg.password_registration in card_of_reg
            assert page_reg.password_registration_confirm in card_of_reg
            assert page_reg.registration_btn in card_of_reg
    except AssertionError:
        print('Элемент отсутствует в форме «Регистрация»')


def test_names_elements_registration(selenium):
    """Проверка Формы "Регистрация" на соответствие названий элементов блока требованию."""
    try:
        page_reg = RegistrPage(selenium)
        assert 'Имя' in page_reg.card_of_registration.text
        assert 'Фамилия' in page_reg.card_of_registration.text
        assert 'Регион' in page_reg.card_of_registration.text
        assert 'E-mail или мобильный телефон' in page_reg.card_of_registration.text
        assert 'Пароль' in page_reg.card_of_registration.text
        assert 'Подтверждение пароля' in page_reg.card_of_registration.text
        assert 'Продолжить' in page_reg.card_of_registration.text
    except AssertionError:
        print('Название элемента в форме «Регистрация» не соответствует Требованию')


def test_autoriz_valid_email_pass(selenium):
    """Тест авторизации с валидными значениями e-mail и пароль."""
    page = AuthPage(selenium)
    page.email.send_keys(Settings.valid_email)
    page.email.clear()
    page.pass_eml.send_keys(Settings.valid_password)
    page.pass_eml.clear()
    page.btn_enter.click()

    try:
        assert page.get_relative_link() == '/account_b2c/page'
    except AssertionError:
        assert 'Неверно введен текст с картинки' in page.find_other_element(*AuthLocators.error_message).text

@pytest.mark.parametrize("incor_email", [Settings.invalid_email, Settings.empty_email],
                         ids=['invalid_email', 'empty'])
@pytest.mark.parametrize("incor_passw", [Settings.invalid_password, Settings.empty_password],
                         ids=['invalid_password', 'empty'])

def test_autoriz_invalid_email_pass(selenium, incor_email, incor_passw):
    """Проверка входа пользователя с невалидным email и паролем:
    связка Почта+Пароль валидна, но пользователь с такими данными не зарегистрирован в системе;
    пустые значения."""
    page = AuthPage(selenium)
    page.email.send_keys(incor_email)
    page.email.clear()
    page.pass_eml.send_keys(incor_passw)
    page.pass_eml.clear()
    page.btn_enter.click()

    assert page.get_relative_link() != '/account_b2c/page'


def test_registration_confirm_password_valid_data(selenium):
    """Тест поля ввода "Пароль" и "Подтвердить пароль" формы «Регистрация»
     валидными значениями(пароли совпадают)."""
    page_reg = RegistrPage(selenium)
    page_reg.password_registration.send_keys(Settings.passw1)
    page_reg.password_registration.clear()
    page_reg.password_registration_confirm.send_keys(Settings.passw1)
    page_reg.password_registration_confirm.clear()
    page_reg.registration_btn.click()

    assert 'Пароли не совпадают' not in page_reg.container_password_confirm.text


def test_user_agreement(selenium):
    """Проверка открытия пользовательского соглашения"""
    form = AuthPage(selenium)

    original_window = form.driver.current_window_handle
    # клик по надписи "Пользовательским соглашением" в подвале страницы
    form.agree.click()

    WebDriverWait(form.driver, 5).until(EC.number_of_windows_to_be(2))
    for window_handle in form.driver.window_handles:
        if window_handle != original_window:
            form.driver.switch_to.window(window_handle)
            break
    win_title = form.driver.execute_script("return window.document.title")

    assert win_title == 'User agreement'

def test_auth_vk(selenium):
    """Проверка перехода по ссылке авторизации пользователя через вконтакте"""
    form = AuthPage(selenium)
    form.vk_btn.click()

    assert form.get_base_url() == 'id.vk.com'

def test_auth_ok(selenium):
    """Проверка перехода по ссылке авторизации пользователя через одноклассники"""
    form = AuthPage(selenium)
    form.ok_btn.click()
    
    assert form.get_base_url() == 'connect.ok.ru' 


def test_auth_mailru(selenium):
    """Проверка перехода по ссылке авторизации пользователя через майлру"""
    form = AuthPage(selenium)
    form.mail_btn.click()

    assert form.get_base_url() == 'connect.mail.ru'


def test_auth_ya(selenium):
    """Проверка перехода по ссылке авторизации пользователя через яндекс"""
    form = AuthPage(selenium)
    form.ya_btn.click()

    assert form.get_base_url() == 'passport.yandex.ru'





