import os

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.color import Color
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from faker import Faker
from random import randint

TEST_DATA = {
    'name': 'Dmitriy',
    'surname': 'Lebed',
    'email': 'up2dmas@gmail.com',
    'phone': '+380637997707',
    'year': '1990',
    'month': '12',
    'day': '18',
    'resume error message': 'неверный формат файла',
    'submit error message': 'Все поля являются обязательными для заполнения',
    'hex color': '#ff0000'
}

driver = webdriver.Chrome()
actions = ActionChains(driver)
fake = Faker()
main_page_url = 'https://netpeak.ua/'


def find_element_by_text(driver, text, tag_name='div'):
    return driver.find_element_by_xpath(f'//{tag_name}[contains(., "{text}")]')


def personal_data_generator():
    full_name = fake.name()
    name_and_surname = full_name.split()
    name = name_and_surname[0]
    surname = name_and_surname[1]
    email = ''.join(name_and_surname) + '@gmail.com'
    phone = '+380' + str(randint(630000000, 950000000))

    name_field = driver.find_element_by_css_selector('#inputName')
    name_field.send_keys(name)

    surname_field = driver.find_element_by_css_selector('#inputLastname')
    surname_field.send_keys(surname)

    email_field = driver.find_element_by_css_selector('#inputEmail')
    email_field.send_keys(email)

    phone_field = driver.find_element_by_css_selector('#inputPhone')
    phone_field.send_keys(phone)


def netpeak_test_task():
    print('\nТестовое задание для Netpeak на позицию Intern Automation QA [Dmitriy Lebed]\n')

    driver.maximize_window()
    driver.implicitly_wait(5)

    driver.get(main_page_url)
    print('1. Перейти по ссылке на главную страницу сайта Netpeak (https://netpeak.ua/) [SUCCESS]')

    career_link = find_element_by_text(driver, "Карьера", "a")
    career_link.click()
    print('2. Перейдите на страницу "Работа в Netpeak", нажав на кнопку "Карьера" [SUCCESS]')

    want_to_work_button = driver.find_element_by_css_selector(".btn.green-btn")
    want_to_work_button.click()
    print('3. Перейти на страницу заполнения анкеты, нажав кнопку - "Я хочу работать в Netpeak" [SUCCESS]')

    upload_resume_button = driver.find_element_by_css_selector('[name="up_file"]')
    upload_resume_button.send_keys(os.getcwd() + "/picture.png")
    sleep(2)
    assert TEST_DATA['resume error message'] in driver.find_element_by_css_selector('#up_file_name > label').text
    print('4. Загрузить файл с недопустимым форматом в блоке "Резюме", например png, и проверить что на странице '
          'появилось сообщение, о том что формат изображения неверный [SUCCESS]')  # неверный формат файла

    personal_data_generator()

    year_dropdown = Select(driver.find_element_by_css_selector('[data-error-name="Birth year"]'))
    year_dropdown.select_by_value(TEST_DATA['year'])
    month_dropdown = Select(driver.find_element_by_css_selector('[data-error-name="Birth month"]'))
    month_dropdown.select_by_value(TEST_DATA['month'])
    day_dropdown = Select(driver.find_element_by_css_selector('[data-error-name="Birth day"]'))
    day_dropdown.select_by_value(TEST_DATA['day'])
    print('5. Заполнить случайными данными блок "3. Личные данные" [SUCCESS]')

    driver.find_element_by_css_selector('#submit > span').click()
    print('6. Нажать на кнопку отправить резюме [SUCCESS]')  # кнопка [Отправить анкету]

    actions.move_to_element(find_element_by_text(driver, "Анкета на вакансию", "h1")).perform()

    assert TEST_DATA['submit error message'] in driver.find_element_by_css_selector('.warning-fields.help-block').text
    warning_message_color = driver.find_element_by_css_selector('.warning-fields.help-block').value_of_css_property('color')
    warning_message_color_hex = Color.from_string(warning_message_color).hex
    assert warning_message_color_hex == TEST_DATA['hex color']
    print('7. Проверить что сообщение на текущей странице  - "Все поля являются обязательными для заполнения" - '
          'подсветилось красным цветом [SUCCESS]')

    driver.find_element_by_css_selector('[alt="Netpeak"]').click()
    sleep(3)
    if driver.current_url == main_page_url:
        print('8. Нажать на логотип для перехода на главную страницу и убедиться что открылась нужная страница [SUCCESS]')

    driver.quit()


netpeak_test_task()
if SystemExit.code != 0:
    print('\n=== Тестовое задание выполнено ===')