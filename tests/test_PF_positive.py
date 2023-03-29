import os
from api import PetFriends
from settings import valid_email, valid_pwd

Test_PF = PetFriends()

# Позитивные тесты

# Получаем ключ авторизации
def test_get_api_key(email=valid_email, pwd=valid_pwd):

    status, result = Test_PF.get_api_key(email, pwd)

    assert status == 200
    assert 'key' in result


# Добавляем питомца без фото
def test_add_new_pet_simple(name='Барсик', animal_type='кот', age='1'):

    status, res_auth = Test_PF.get_api_key(valid_email, valid_pwd)
    auth = res_auth['key']

    status, result = Test_PF.add_new_pet_simple(auth, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


# Изменяем даные о питомце
def test_update_pet(name='Владлен', animal_type='козёл', age='10', fltr='my_pets'):

    _, res_auth = Test_PF.get_api_key(valid_email, valid_pwd)
    auth = res_auth['key']

    _, _, pet_id = Test_PF.get_pet_list_and_last_id(auth, fltr)

    if pet_id != 0:

        status, result = Test_PF.update_pet_by_id(auth, pet_id, name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Нет моих питомцев")


# Добавляем фото питомца
def test_add_photo_of_pet(pet_photo='кузёл.jpg',  fltr='my_pets'):

    status, res_auth = Test_PF.get_api_key(valid_email, valid_pwd)
    auth = res_auth['key']

    _, _, pet_id = Test_PF.get_pet_list_and_last_id(auth, fltr)

    pet_photo = os.path.join(os.path.dirname(__file__), 'images', pet_photo)

    if pet_id != 0:

        status, result = Test_PF.add_pets_photo(auth, pet_id, pet_photo)

        assert status == 200
        assert result['pet_photo'].startswith('data:image/jpeg')
    else:
        raise Exception("Нет моих питомцев")


# Удаляем питомца
def test_delete_pet(fltr='my_pets'):

    _, res_auth = Test_PF.get_api_key(valid_email, valid_pwd)
    auth = res_auth['key']

    _, _, pet_id = Test_PF.get_pet_list_and_last_id(auth, fltr)

    if pet_id != 0:

        status, result = Test_PF.delete_pet_by_id(auth, pet_id)

        assert status == 200

        _, _, pet_new_id = Test_PF.get_pet_list_and_last_id(auth, fltr)

        assert pet_new_id == 0 or pet_id != pet_new_id
    else:
        raise Exception('Нет моих питомцев')


# Добавляем питомца с фото
def test_add_new_pet(name='Вениамин Бедросович', animal_type='пёс', age='5', pet_photo='собаня.jpg'):

    status, res_auth = Test_PF.get_api_key(valid_email, valid_pwd)
    auth = res_auth['key']

    pet_photo = os.path.join(os.path.dirname(__file__), 'images', pet_photo)

    status, result = Test_PF.add_new_pet(auth, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


# Выводим список "моих" питомцев
def test_get_pets_list(name='Вениамин Бедрович', animal_type='пёс', age='5', fltr='my_pets'):

    status, res_auth = Test_PF.get_api_key(valid_email, valid_pwd)
    auth = res_auth['key']

    _, pets_list, _ = Test_PF.get_pet_list_and_last_id(auth, fltr)
    len_pets_list = len(pets_list['pets'])

    _, result = Test_PF.add_new_pet_simple(auth, f'{name} New', animal_type, age)

    status, pets_list_new, _ = Test_PF.get_pet_list_and_last_id(auth, fltr)

    assert status == 200
    assert len(pets_list_new['pets']) == len_pets_list + 1