import unittest
import sys
import json
import requests

class LoginUnittest(unittest.TestCase):
    def test_create1_create_new_prospect_tenant(self):
        response = requests.post("http://127.0.0.1:5000/api/create/user", data = {'Username':'KlaraKlet', 'Password':'Zimbabue99', 'Landlord':False})
        assert response.status_code == 200

    def test_create2_create_new_prospect_tenant_already_exists(self):
        response = requests.post("http://127.0.0.1:5000/api/create/user", data = {'Username':'KlaraKlet', 'Password':'Zimbabue99', 'Landlord':False})
        assert response.status_code == 418

    def test_create3_create_new_landlord_account(self):
        response = requests.post("http://127.0.0.1:5000/api/create/user", data = {'Username':'PrinsAlbert', 'Password':'123', 'Landlord':True})
        assert response.status_code == 200

    def test_create4_create_new_landlord_account_already_exists(self):
        response = requests.post("http://127.0.0.1:5000/api/create/user", data = {'Username':'PrinsAlbert', 'Password':'123', 'Landlord':True})
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
        response = requests.put("http://127.0.0.1:5000/api/update/user", data = {'Id':10,'Username':'KuntaKinte', 'Password':'88666'})
        response_body = response.json()
        assert response_body["Id"] == 10
        assert response_body["Username"] == "KuntaKinte"
        assert response_body["Password"] == "88666"

    def test_update2_update_a_user_with_only_one_field(self):
        response = requests.put("http://127.0.0.1:5000/api/update/user", data = {'Id':10,'Username':'KuntaKinte'})
        assert response.status_code == 418

    def test_update3_update_landlord_status(self):
        response = requests.put("http://127.0.0.1:5000/api/update/user", data = {'Id':10,'Landlord':False})
        assert response.status_code == 418
    
    def test_read1_read_all_users(self):
        response = requests.get("http://127.0.0.1:5000/api/read/user")
        assert response.status_code == 200

    def test_read2_read_specific_user(self):
        response = requests.get("http://127.0.0.1:5000/api/read/user/10")
        response_body = response.json()
        assert response_body["Id"] == 10
        assert response_body["Username"] == "KuntaKinte"
        assert response_body["Password"] == "88666"

    def test_read3_read_specific_user_fail(self):
        response = requests.get("http://127.0.0.1:5000/api/read/user/1")
        assert response.status_code == 418

    def test_delete1_delete_user(self):
        response = requests.delete("http://127.0.0.1:5000/api/delete/user/10")
        assert response.status_code == 200

    def test_delete2_delete_user_fail(self):
        response = requests.delete("http://127.0.0.1:5000/api/delete/user/-1")
        assert response.status_code == 418
        

if __name__ == '__main__':
    unittest.main()