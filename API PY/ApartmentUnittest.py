import unittest
import sys
import json
import requests


class ApartmentUnittest(unittest.TestCase):
    deleteId1 = 0
    deleteId2 = 0

    def test_create1_create_new_apartment(self):
        response = requests.post("http://127.0.0.1:5000/api/create/apartment", json = {'Price':666, 'numberOfRooms': '3', 'sizeOfApartment':'88', 'Address':'Rektalvägen 4', 'Location':'Skogshöjden', "Information":"En trevlig hydda nära till närbutiken", "LandlordId":8,"Picture":'test/de/la/test', "Active":True})
        response_body = response.json()
        global deleteId1
        deleteId1 = response_body["Id"]
        assert response.status_code == 200

    def test_create1_5_create_new_apartment(self):
        response = requests.post("http://127.0.0.1:5000/api/create/apartment", json = {'Price':100, 'numberOfRooms': '3', 'sizeOfApartment':'88', 'Address':'Rektalvägen 46', 'Location':'Skogshöjden V2', "Information":"En trevlig hydda nära till närbutiken 2", "LandlordId":8,"Picture":'test/de/la/test', "Active":True})
        response_body = response.json()
        global deleteId2
        deleteId2 = response_body["Id"]
        assert response.status_code == 200

    def test_create2_create_without_all_parameters(self):
        response = requests.post("http://127.0.0.1:5000/api/create/apartment", json = {'Price':200, 'numberOfRooms': '3', 'sizeOfApartment':'35', 'Address':'Miljövägen', 'Location':'Centrum', "Information":"fin lya", "LandlordId":8,"Picture": None})
        assert response.status_code == 418

    def test_create3_create_without_landlord_user(self):
        response = requests.post("http://127.0.0.1:5000/api/create/apartment", json = {'Price':2000, 'numberOfRooms': '3', 'sizeOfApartment':'35', 'Address':'Miljövägen', 'Location':'Centrum', "Information":"fin lya", "LandlordId":2,"Picture": None, "Active": True})
        assert response.status_code == 418

    def test_read1_read_all_apartments(self):
        response = requests.get("http://127.0.0.1:5000/api/read/apartments")
        assert response.status_code == 200

    def test_read2_read_apartment_with_apartment_Id(self):
        response = requests.get("http://127.0.0.1:5000/api/read/apartment?id=6")
        assert response.status_code == 200

    def test_read3_read_apartment_with_landlord_Id(self):
        response = requests.get("http://127.0.0.1:5000/api/read/apartment?landlordid=2")
        assert response.status_code == 200

    def test_read4_read_apartment_with_active_true(self):
        response = requests.get("http://127.0.0.1:5000/api/read/apartment?active=True")
        assert response.status_code == 200

    def test_read5_invalid_id(self):
        response = requests.get("http://127.0.0.1:5000/api/read/apartment?id=0")
        assert response.status_code == 418

    def test_update1_existing_apartment(self):
        global deleteId2
        response = requests.put("http://127.0.0.1:5000/api/update/apartment", json = {'Id': str(deleteId2), 'Price':666, 'numberOfRooms': '3', 'sizeOfApartment':'100', 'Address':'Rektalvägen 46', 'Location':'Skogshöjden V2', "Information":"En trevlig hydda nära till närbutiken 2", "LandlordId":8,"Picture":'test/de/la/test', "Active":True})
        response_body = response.json()
        assert response_body["SizeOfApartment"] == "100"
    
    def test_update2_apartment_that_does_not_exist(self):
        response = requests.put("http://127.0.0.1:5000/api/update/apartment", json = {'Id': 999, 'Price':200, 'numberOfRooms': '3', 'sizeOfApartment':'35', 'Address':'Miljövägen', 'Location':'Centrum', "Information":"fin lya", "LandlordId":8,"Picture": None, "Active": True})
        assert response.status_code == 418

    def test_delete1_delete_existing(self):
        global deleteId1
        response = requests.delete("http://127.0.0.1:5000/api/delete/apartment/" + str(deleteId1))
        assert response.status_code == 200

    def test_delete2_delete_non_existing(self):
        response = requests.delete("http://127.0.0.1:5000/api/delete/apartment/1693")
        assert response.status_code == 418

    @classmethod
    def tearDownClass(cls):
        #DELETE USED CLASSES ETC
        global deleteId2
        response = requests.delete("http://127.0.0.1:5000/api/delete/apartment/" + str(deleteId2))
        assert response.status_code == 200


if __name__ == '__main__':
    unittest.main()