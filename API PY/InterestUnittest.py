import unittest
import sys
import json
import requests
import RentalService

class InterestUnittest(unittest.TestCase):
    deleteId1 = 0
    deleteId2 = 0
    def test_create1_new_interest(self):
        response = requests.post("http://127.0.0.1:5000/api/create/interest", json= {'UserId': 2, 'ApartmentId':10})
        response_body = response.json()
        global deleteId1
        deleteId1 = response_body["Id"]
        assert response.status_code == 200

    def test_create1_5_test_object(self):
        response = requests.post("http://127.0.0.1:5000/api/create/interest", json= {'UserId': 13, 'ApartmentId':10})
        response_body = response.json()
        global deleteId2
        deleteId2 = response_body["Id"]
        assert response.status_code == 200

    def test_create2_create_existing(self):
        response = requests.post("http://127.0.0.1:5000/api/create/interest", json= {'UserId': 8, 'ApartmentId':10})
        assert response.status_code == 418

    def test_read1_read_all(self):
        response = requests.get("http://127.0.0.1:5000/api/read/interests")
        assert response.status_code == 200

    def test_read2_read_interest_with_userid(self):
        response = requests.get("http://127.0.0.1:5000/api/read/interest?userid=8")
        assert response.status_code == 200
    
    def test_read3_read_interest_with_apartmentid(self):
        response = requests.get("http://127.0.0.1:5000/api/read/interest?apartmentid=10")
        assert response.status_code == 200

    def test_update1_update_interest(self):
        global deleteId2
        response = requests.put("http://127.0.0.1:5000/api/update/interest", json = {'Id': str(deleteId2),'UserId':14, 'ApartmentId':10})
        response_body = response.json()
        assert response_body["UserId"] == 14

    def test_update2_update_interest_that_does_not_exist(self):
        response = requests.put("http://127.0.0.1:5000/api/update/interest", json = {'Id': 666,'UserId':666, 'ApartmentId':666})
        assert response.status_code == 418

    def test_delete1_delete_interest_that_exists(self):
        global deleteId1
        response = requests.delete("http://127.0.0.1:5000/api/delete/interest/" + str(deleteId1))
        assert response.status_code == 200

    def test_delete2_delete_interest_that_does_not_exist(self):
        response = requests.delete("http://127.0.0.1:5000/api/delete/interest/1693")
        assert response.status_code == 418


    @classmethod
    def tearDownClass(cls):
        #DELETE USED CLASSES ETC
        global deleteId2
        response = requests.delete("http://127.0.0.1:5000/api/delete/interest/" + str(deleteId2))
        assert response.status_code == 200


if __name__ == '__main__':
    unittest.main()