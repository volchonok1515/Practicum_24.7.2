import os
from api import PetFriends
from settings import valid_email, valid_pwd

Test_PF = PetFriends()


# Негативные тесты


# 1. Попытка получить ключ авторизации без пароля
def test_get_api_key_without_password(email=valid_email, pwd=''):

    status, result = Test_PF.get_api_key(email, pwd)

    assert status == 403
    assert 'key' not in result


# 2. Попытка получить ключ авторизации без емейла
def test_get_api_key_without_email(email='', pwd=valid_pwd):

    status, result = Test_PF.get_api_key(email, pwd)

    assert status == 403
    assert 'key' not in result


# 3. Попытка добавить питомца без авторизации
def test_add_new_pet_without_auth(name='Владлен', animal_type='козёл', age='10'):

    auth = ''

    status, result = Test_PF.add_new_pet_simple(auth, name, animal_type, age)

    assert status == 403


# 4. Изменяем данные о питомце - пустое имя
def test_update_pet_without_name(name='', animal_type='козел', age='10', fltr='my_pets'):

    _, res_auth = Test_PF.get_api_key(valid_email, valid_pwd)
    auth = res_auth['key']

    _, _, pet_id = Test_PF.get_pet_list_and_last_id(auth, fltr)

    if pet_id != 0:

        status, result = Test_PF.update_pet_by_id(auth, pet_id, name, animal_type, age)

        assert status == 400
    else:
        raise Exception("Нет моих питомцев")


# 5. Добавление питомца без типа
def test_add_new_pet_without_type(name='Вениамин Бедросович', animal_type='', age='5'):

    status, res_auth = Test_PF.get_api_key(valid_email, valid_pwd)
    auth = res_auth['key']

    status, result = Test_PF.add_new_pet_simple(auth, name, animal_type, age)

    assert status == 400


# 6. Добавляем питомца с отрицательным возрастом
def test_add_new_pet_without_negative_age(name='Вениамин Бедросович', animal_type='Пёс', age='-7'):

    status, res_auth = Test_PF.get_api_key(valid_email, valid_pwd)
    auth = res_auth['key']

    status, result = Test_PF.add_new_pet_simple(auth, name, animal_type, age)

    assert status == 400


# 7. Добавляем питомца с возрастом - текстом
def test_add_new_pet_without_age_not_number(name='Владлен', animal_type='Козёл', age='десять лет'):

    status, res_auth = Test_PF.get_api_key(valid_email, valid_pwd)
    auth = res_auth['key']

    status, result = Test_PF.add_new_pet_simple(auth, name, animal_type, age)

    assert status == 400


# 8. Добавляем питомца с несуществующим возрастом
def test_add_new_pet_with_too_much_age(name='Дункан МакЛауд', animal_type='Чебуртор', age=(7899455611123)):

    status, res_auth = Test_PF.get_api_key(valid_email, valid_pwd)
    auth = res_auth['key']

    status, result = Test_PF.add_new_pet_simple(auth, name, animal_type, age)

    assert status == 400

# 9. Добавление питомца с несуществующим типом
def test_add_new_pet_without_type(name='Вениамин Бедросович', animal_type='@#$%^&*', age='5'):

    status, res_auth = Test_PF.get_api_key(valid_email, valid_pwd)
    auth = res_auth['key']

    status, result = Test_PF.add_new_pet_simple(auth, name, animal_type, age)

    assert status == 400


# 10. Добавление фото питомца файл .exe, а не jpg
def test_add_photo_of_pet_txt_file(pet_photo='Joxy.exe',  fltr='my_pets'):

    _, res_auth = Test_PF.get_api_key(valid_email, valid_pwd)
    auth = res_auth['key']

    _, _, pet_id = Test_PF.get_pet_list_and_last_id(auth, fltr)

    pet_photo = os.path.join(os.path.dirname(__file__), 'images', pet_photo)

    if pet_id != 0:

        status, result = Test_PF.add_pets_photo(auth, pet_id, pet_photo)

        assert status == 500
    else:
        raise Exception("Нет моих питомцев")