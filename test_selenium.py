import pytest
from driver import driver
from selenium import webdriver as selenium_webdriver
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from collections import Counter

from selenium.webdriver.support.wait import WebDriverWait


def test_show_my_pets(selenium_driver):
    ''' Тест на проверку списка питомцев:
       1. Проверяем, что оказались на странице питомцев пользователя.
       2. Проверяем, что присутствуют все питомцы.  '''

    driver = selenium_driver
    driver.implicitly_wait(10)

    # Нажимаем на кнопку входа в пункт меню Мои питомцы
    driver.find_element(By.CSS_SELECTOR, "a.nav-link[href='/my_pets']").click()

    # Проверяем, что оказались на странице питомцев пользователя
    assert driver.current_url == 'https://petfriends.skillfactory.ru/my_pets'

    # 1. Проверяем, что присутствуют все питомцы, для этого:
    # находим кол-во питомцев по статистике пользователя и проверяем, что их число
    # соответствует кол-ву питомцев в таблице
    pets_number = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1]
    # pets_count = 100
    pets_count = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
    assert int(pets_number) == len(pets_count)

# проверяем, что хотя бы у половины питомцев есть фото
def test_half_of_pets_have_photo(selenium_driver):
    driver = selenium_driver
    driver.implicitly_wait(10)
    driver.find_element(By.CSS_SELECTOR, "a.nav-link[href='/my_pets']").click()
    pets_number = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1]
    photos = []
    try:
        photos = driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets > table img')
    except TimeoutException:
        print("Не удалось загрузить элементы на странице")
    finally:
        photo_count = 0
        for i in range(len(photos)):
            if photos[i].get_attribute('src') != '':
                photo_count += 1
        assert photo_count >= int(pets_number) / 2


# проверяем, что у всех питомцев есть имя, возраст и порода
def test_pets_have_name_age_type(selenium_driver):
    driver = selenium_driver
    driver.implicitly_wait(10)
    driver.find_element(By.CSS_SELECTOR, "a.nav-link[href='/my_pets']").click()
    pets_number = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1]
    names = driver.find_elements(By.CSS_SELECTOR, 'tbody > tr > td:nth-of-type(1)')
    text_names = [names[i].text for i in range(len(names))]
    types = driver.find_elements(By.CSS_SELECTOR, 'tbody > tr > td:nth-of-type(2)')
    text_types = [types[i].text for i in range(len(types))]
    ages = driver.find_elements(By.CSS_SELECTOR, 'tbody > tr > td:nth-of-type(3)')
    text_ages = [ages[i].text for i in range(len(ages))]

    for i in range(len(pets_number)):
        assert text_names[i] != ''
        assert text_ages[i] != ''
        assert text_types[i] != ''

# проверяем, что у всех питомцев разные имена
def test_pets_have_diff_name(selenium_driver):
    driver = selenium_driver
    driver.implicitly_wait(10)
    driver.find_element(By.CSS_SELECTOR, "a.nav-link[href='/my_pets']").click()
    names = driver.find_elements(By.CSS_SELECTOR, 'tbody > tr > td:nth-of-type(1)')
    text_names = [names[i].text for i in range(len(names))]

    new_arr = Counter(text_names)
    for i in text_names:
        assert new_arr[i] <= 1

# проверяем, что в списке нет повторяющихся питомцев
def test_all_pets_are_unique(selenium_driver):
    driver = selenium_driver
    driver.implicitly_wait(10)
    driver.find_element(By.CSS_SELECTOR, "a.nav-link[href='/my_pets']").click()
    pets_number = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1]
    names = driver.find_elements(By.CSS_SELECTOR, 'tbody > tr > td:nth-of-type(1)')
    text_names = [names[i].text for i in range(len(names))]
    types = driver.find_elements(By.CSS_SELECTOR, 'tbody > tr > td:nth-of-type(2)')
    text_types = [types[i].text for i in range(len(types))]
    ages = driver.find_elements(By.CSS_SELECTOR, 'tbody > tr > td:nth-of-type(3)')
    text_ages = [ages[i].text for i in range(len(ages))]

    pets = []
    for i in range(len(names)):
        pets.append({'name': text_names[i], 'type': text_types[i], 'age': text_ages[i]})

    error = False
    for i in range(len(pets)-1):
        for k in range(i+1, (len(pets))):
            if pets[i] == pets[k]:
                error = True
                break
        if error:
            break
    assert error == False


def test_web_driver_implicitly_wait(selenium_driver):
    # Переходим на страницу c таблицей питомцев
    driver = selenium_driver
    driver.find_element(By.CSS_SELECTOR, "a.nav-link[href='/my_pets']").click()
    # Устанавливаем неявное ожидание
    driver.implicitly_wait(10)
    images = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr[1]/th[1]')
    names = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr[1]/td[1]')
    ages = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr[1]/td[3]')
    # Src фотографий
    src_images = [x.get_attribute('src') for x in images]
    # Text имен
    text_names = [x.text for x in names]
    # Text возраста
    text_ages = [x.text for x in ages]
    # Число найденных элементов одинаковое (небольшой смок тест,
    # что элементы получены, ожидания отработали)
    assert len(src_images) == len(text_names)
    assert len(src_images) == len(text_ages)

