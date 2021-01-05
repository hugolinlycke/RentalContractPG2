import unittest
import sys
import json
import requests

class RentalUnittest(unittest.TestCase):
    deleteId1 = 0
    deleteId2 = 0
    def test_create1_create_new_rental(self):
        response = requests.post("http://127.0.0.1:5000/api/create/rental", json= {'LandlordId': 8, 'ApartmentId':10, 'UserId':2})
        response_body = response.json()
        global deleteId1
        deleteId1 = response_body["Id"]
        assert response.status_code == 200

    def test_create1_5_create_test_data(self):
        response = requests.post("http://127.0.0.1:5000/api/create/rental", json= {'LandlordId': 8, 'ApartmentId':10, 'UserId':13})
        response_body = response.json()
        global deleteId2
        deleteId2 = response_body["Id"]
        assert response.status_code == 200

    def test_create2_create_rental_with_non_existing_apartment(self):
        response = requests.post("http://127.0.0.1:5000/api/create/rental", json= {'LandlordId': 8, 'ApartmentId':9999, 'UserId':2})
        assert response.status_code == 418

    def test_read1_read_all_rentals(self):
        response = requests.get("http://127.0.0.1:5000/api/read/rentals")
        assert response.status_code == 200

    def test_read2_read_rental_with_landlordid(self):
        response = requests.get("http://127.0.0.1:5000/api/read/rental?landlordid=2")
        assert response.status_code == 200
    
    def test_update1_update_rental(self):
        global deleteId2
        response = requests.put("http://127.0.0.1:5000/api/update/rental", json = {'Id': str(deleteId2),'LandlordId': 8, 'ApartmentId':10, 'UserId':14})
        response_body = response.json()
        assert response_body["UserId"] == 14

    def test_update2_update_non_existing_rental(self):
        response = requests.put("http://127.0.0.1:5000/api/update/rental", json = {'Id': 999,'LandlordId': 8, 'ApartmentId':10, 'UserId':13})
        assert response.status_code == 418

    def test_delete1_delete_rental(self):
        global deleteId1
        response = requests.delete("http://127.0.0.1:5000/api/delete/rental/" + str(deleteId1))
        assert response.status_code == 200

    def test_delete2_delete_non_existing_rental(self):
        response = requests.delete("http://127.0.0.1:5000/api/delete/rental/9999")
        assert response.status_code == 418

    @classmethod
    def tearDownClass(cls):
        #DELETE USED CLASSES ETC
        global deleteId2
        response = requests.delete("http://127.0.0.1:5000/api/delete/rental/" + str(deleteId2))
        assert response.status_code == 200


if __name__ == '__main__':
    unittest.main()