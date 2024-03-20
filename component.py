import requests
from uuid import UUID, uuid4
from datetime import datetime
import unittest


pet_url = 'http://localhost:8000'
get_pets_url = f'{pet_url}/get_pets'
add_pets_url = f'{pet_url}/add_pet'
get_pet_by_id_url = f'{pet_url}/get_pet_by_id/'
delete_pet_url = f'{pet_url}/delete_pet'

generatepass_url = 'http://localhost:8001'


pet = {
    "id": "945949ce-4aaa-49f0-a13c-f8ae7a19df44",
    "name": "Bessi",
    "favorite_delicacy": "Carrot",
    "weight": 20,
    "age": 5,
    "favorite_activity": "Sleep"

}


class TestComponent(unittest.TestCase):

    def test_1_get_pets(self):
        res = requests.get(f"{get_pets_url}")
        self.assertTrue(res != None)

    def test_2_add_pet(self):
        res = requests.post(f"{add_pets_url}", json=pet)
        self.assertEqual(res.status_code, 200)

    def test_3_get_pet_by_id(self):
        res = requests.get(f"{get_pet_by_id_url}?pet_id={pet['id']}").json()
        self.assertTrue(res, pet)

    def test_4_delete_pet(self):
        res = requests.delete(f"{delete_pet_url}?pet_id={pet['id']}").json()
        self.assertEqual(res, "Success")

if __name__ == '__main__':
    unittest.main()
