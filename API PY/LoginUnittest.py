import unittest
import sys
import json
import requests


class LoginUnittest(unittest.TestCase):
    def __init__(self, deleteId1, deleteId2):
        self.deleteId1 = deleteId1
        self.deleteId2 = deleteId2

    def test_create1_create_new_prospect_tenant(self):
        response = requests.post("http://127.0.0.1:5000/api/create/user", json = {'Username':'KlaraKlet', 'Password':'Zimbabue99', 'Landlord':False})
        response_body = response.json()
        self.deleteId1 = response_body["Id"]
        assert response.status_code == 200

    def test_create2_create_new_prospect_tenant_already_exists(self):
        response = requests.post("http://127.0.0.1:5000/api/create/user", json = {'Username':'KlaraKlet', 'Password':'Zimbabue99', 'Landlord':False})
        assert response.status_code == 418

    def test_create3_create_new_landlord_account(self):
        response = requests.post("http://127.0.0.1:5000/api/create/user", json = {'Username':'PrinsAlbert', 'Password':'123', 'Landlord':True})
        response_body = response.json()
        self.deleteId2 = response_body["Id"]
        assert response.status_code == 200

    def test_create4_create_new_landlord_account_already_exists(self):
        response = requests.post("http://127.0.0.1:5000/api/create/user", json = {'Username':'PrinsAlbert', 'Password':'123', 'Landlord':True})
        assert response.status_code == 418

    def test_login1(self):
        payload = {'Username': 'KlaraKlet', 'Password': 'Zimbabue99'}
        response = requests.get("http://127.0.0.1:5000/api/login", params=payload)
        assert response.status_code == 200

    def test_login2(self):  
        payload = {'Username': 'KlaraKlet', 'Password': '123'}
        response = requests.get("http://127.0.0.1:5000/api/login", params=payload)
        assert response.status_code == 418

    def test_update1_update_a_user_with_all_fields(self):
        response = requests.put("http://127.0.0.1:5000/api/update/user", json = {'Id':self.deleteId1,'Username':'KuntaKinte', 'Password':'88666'})
        response_body = response.json()
        assert response_body["Id"] == 10
        assert response_body["Username"] == "KuntaKinte"
        assert response_body["Password"] == "88666"

    def test_update2_update_a_user_with_only_one_field(self):
        response = requests.put("http://127.0.0.1:5000/api/update/user", json = {'Id':self.deleteId1,'Username':'KuntaKinte'})
        assert response.status_code == 418

    def test_update3_update_landlord_status(self):
        response = requests.put("http://127.0.0.1:5000/api/update/user", json = {'Id':self.deleteId1,'Landlord':False})
        assert response.status_code == 418
    
    def test_read1_read_all_users(self):
        response = requests.get("http://127.0.0.1:5000/api/read/user")
        assert response.status_code == 200

    def test_read2_read_specific_user(self):
        response = requests.get("http://127.0.0.1:5000/api/read/user/2")
        response_body = response.json()
        assert response_body["Id"] == 2
        assert response_body["Username"] == "KissKalle"
        assert response_body["Password"] == "123"

    def test_read3_read_specific_user_fail(self):
        response = requests.get("http://127.0.0.1:5000/api/read/user/1")
        assert response.status_code == 418

    def test_delete1_delete_user(self):
        response = requests.delete("http://127.0.0.1:5000/api/delete/user/" + self.deleteId1)
        assert response.status_code == 200
    #Just delete to go back to reset data
    def test_delete1_05_delete_user(self):
        response = requests.delete("http://127.0.0.1:5000/api/delete/user/" + self.deleteId2)
        assert response.status_code == 200


    def test_delete2_delete_user_fail(self):
        response = requests.delete("http://127.0.0.1:5000/api/delete/user/-1")
        assert response.status_code == 418



if __name__ == '__main__':
    unittest.main()