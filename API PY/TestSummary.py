import unittest
import sys
import json
import requests
import RentalService

class TestSummary(unittest.TestCase):
    deleteId1 = 0
    deleteId2 = 0
    deleteId3 = 0
    deleteId4 = 0
    deleteId5 = 0
    deleteId6 = 0
    deleteId7 = 0
    deleteId8 = 0
    deleteId9 = 0
    deleteId10 = 0

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

    #NEXT

    def test_create1_create_new_apartment(self):
        response = requests.post("http://127.0.0.1:5000/api/create/apartment", json = {'Price':666, 'numberOfRooms': '3', 'sizeOfApartment':'88', 'Address':'Rektalvägen 4', 'Location':'Skogshöjden', "Information":"En trevlig hydda nära till närbutiken", "LandlordId":8,"Picture":'test/de/la/test', "Active":True})
        response_body = response.json()
        global deleteId3
        deleteId3 = response_body["Id"]
        assert response.status_code == 200

    def test_create1_5_create_new_apartment(self):
        response = requests.post("http://127.0.0.1:5000/api/create/apartment", json = {'Price':100, 'numberOfRooms': '3', 'sizeOfApartment':'88', 'Address':'Rektalvägen 46', 'Location':'Skogshöjden V2', "Information":"En trevlig hydda nära till närbutiken 2", "LandlordId":8,"Picture":'test/de/la/test', "Active":True})
        response_body = response.json()
        global deleteId4
        deleteId4 = response_body["Id"]
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
        global deleteId4
        response = requests.put("http://127.0.0.1:5000/api/update/apartment", json = {'Id': str(deleteId4), 'Price':666, 'numberOfRooms': '3', 'sizeOfApartment':'100', 'Address':'Rektalvägen 46', 'Location':'Skogshöjden V2', "Information":"En trevlig hydda nära till närbutiken 2", "LandlordId":8,"Picture":'test/de/la/test', "Active":True})
        response_body = response.json()
        assert response_body["SizeOfApartment"] == "100"
    
    def test_update2_apartment_that_does_not_exist(self):
        response = requests.put("http://127.0.0.1:5000/api/update/apartment", json = {'Id': 999, 'Price':200, 'numberOfRooms': '3', 'sizeOfApartment':'35', 'Address':'Miljövägen', 'Location':'Centrum', "Information":"fin lya", "LandlordId":8,"Picture": None, "Active": True})
        assert response.status_code == 418

    def test_delete1_delete_existing(self):
        global deleteId3
        response = requests.delete("http://127.0.0.1:5000/api/delete/apartment/" + str(deleteId3))
        assert response.status_code == 200

    def test_delete2_delete_non_existing(self):
        response = requests.delete("http://127.0.0.1:5000/api/delete/apartment/1693")
        assert response.status_code == 418

    #NEXT

    def test_create1_create_new_rental(self):
        response = requests.post("http://127.0.0.1:5000/api/create/rental", json= {'LandlordId': 8, 'ApartmentId':10, 'UserId':2})
        response_body = response.json()
        global deleteId5
        deleteId5 = response_body["Id"]
        assert response.status_code == 200

    def test_create1_5_create_test_data(self):
        response = requests.post("http://127.0.0.1:5000/api/create/rental", json= {'LandlordId': 8, 'ApartmentId':10, 'UserId':13})
        response_body = response.json()
        global deleteId6
        deleteId6 = response_body["Id"]
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
        global deleteId6
        response = requests.put("http://127.0.0.1:5000/api/update/rental", json = {'Id': str(deleteId6),'LandlordId': 8, 'ApartmentId':10, 'UserId':14})
        response_body = response.json()
        assert response_body["UserId"] == 14

    def test_update2_update_non_existing_rental(self):
        response = requests.put("http://127.0.0.1:5000/api/update/rental", json = {'Id': 999,'LandlordId': 8, 'ApartmentId':10, 'UserId':13})
        assert response.status_code == 418

    def test_delete1_delete_rental(self):
        global deleteId5
        response = requests.delete("http://127.0.0.1:5000/api/delete/rental/" + str(deleteId5))
        assert response.status_code == 200

    def test_delete2_delete_non_existing_rental(self):
        response = requests.delete("http://127.0.0.1:5000/api/delete/rental/9999")
        assert response.status_code == 418


    #NEXT
    def test_create1_create_new_point(self):
        response = requests.post("http://127.0.0.1:5000/api/create/point", json= {'UserId': 2, 'Points':200})
        response_body = response.json()
        global deleteId7
        deleteId7 = response_body["Id"]
        assert response.status_code == 200

    def test_create1_5_create_new_point(self):
        response = requests.post("http://127.0.0.1:5000/api/create/point", json= {'UserId': 13, 'Points':200})
        response_body = response.json()
        global deleteId8
        deleteId8 = response_body["Id"]
        assert response.status_code == 200


    def test_create2_create_existing_user(self):
        response = requests.post("http://127.0.0.1:5000/api/create/point", json= {'UserId': 2, 'Points':200})
        assert response.status_code == 418

    def test_read1_read_all_point(self):
        response = requests.get("http://127.0.0.1:5000/api/read/points")
        assert response.status_code == 200
        
    def test_read2_read_specific_point(self):
        response = requests.get("http://127.0.0.1:5000/api/read/point/7")
        assert response.status_code == 200

    def test_read3_read_user_not_existing(self):
        response = requests.get("http://127.0.0.1:5000/api/read/point/-1")
        assert response.status_code == 418

    def test_update1_update_points(self):
        global deleteId8
        response = requests.put("http://127.0.0.1:5000/api/update/point", json = {'Id': str(deleteId8),'UserId':13, 'Points':500})
        response_body = response.json()
        assert response_body["Points"] == 500

    def test_update2_update_userId(self):
        global deleteId8
        response = requests.put("http://127.0.0.1:5000/api/update/point", json = {'Id': str(deleteId8),'UserId':12, 'Points':500})
        response_body = response.json()
        assert response_body["UserId"] == 12
    
    def test_update3_update_user_not_exist(self):
        response = requests.put("http://127.0.0.1:5000/api/update/point", json = {'Id': str(deleteId2),'UserId':-1, 'Points':200})
        assert response.status_code == 418
    
    def test_update4_update_user_that_already_exists(self):
        response = requests.put("http://127.0.0.1:5000/api/update/point", json = {'Id': str(deleteId2),'UserId':7, 'Points':200})
        assert response.status_code == 418

    def test_delete1_delete_user_point(self):
        global deleteId7
        response = requests.delete("http://127.0.0.1:5000/api/delete/point/" + str(deleteId7))
        assert response.status_code == 200

    def test_delete2_delete_user_fail_point(self):
        response = requests.delete("http://127.0.0.1:5000/api/delete/point/-1")
        assert response.status_code == 418

    #NEXT

    def test_create1_create_new_prospect_tenant(self):
        response = requests.post("http://127.0.0.1:5000/api/create/user", json = {'Username':'KnasKlas', 'Password':'1234', 'Landlord':False})
        response_body = response.json()
        global deleteId9
        deleteId9 = response_body["Id"]
        assert response.status_code == 200

    def test_create2_create_new_prospect_tenant_already_exists(self):
        response = requests.post("http://127.0.0.1:5000/api/create/user", json = {'Username':'KnasKlas', 'Password':'1234', 'Landlord':False})
        assert response.status_code == 418

    def test_create3_create_new_landlord_account(self):
        response = requests.post("http://127.0.0.1:5000/api/create/user", json = {'Username':'SaraSand', 'Password':'1234', 'Landlord':True})
        response_body = response.json()
        global deleteId10
        deleteId10 = response_body["Id"]
        assert response.status_code == 200

    def test_create4_create_new_landlord_account_already_exists(self):
        response = requests.post("http://127.0.0.1:5000/api/create/user", json = {'Username':'SaraSand', 'Password':'1234', 'Landlord':True})
        assert response.status_code == 418

    def test_login1(self):
        payload = {'username': 'KlaraKlet', 'password': 'Zimbabue99'}
        response = requests.get("http://127.0.0.1:5000/api/login", params=payload)
        assert response.status_code == 200

    def test_login2(self):  
        payload = {'username': 'KlaraKlet', 'password': '123'}
        response = requests.get("http://127.0.0.1:5000/api/login", params=payload)
        assert response.status_code == 418

    def test_update1_update_a_user_with_all_fields(self):
        global deleteId10
        response = requests.put("http://127.0.0.1:5000/api/update/user", json = {'Id': str(deleteId10),'Username':'KuntaKinte', 'Password':'88666'})
        response_body = response.json()
        assert response_body["Username"] == "KuntaKinte"
        assert response_body["Password"] == "88666"

    def test_update2_update_a_user_with_only_one_field(self):
        global deleteId9
        response = requests.put("http://127.0.0.1:5000/api/update/user", json = {'Id': str(deleteId9),'Username':'KuntaKinte'})
        assert response.status_code == 418

    def test_update3_update_landlord_status(self):
        global deleteId9
        response = requests.put("http://127.0.0.1:5000/api/update/user", json = {'Id': str(deleteId9),'Landlord':False})
        assert response.status_code == 418
    
    def test_read1_read_all_users(self):
        response = requests.get("http://127.0.0.1:5000/api/read/users")
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
        global deleteId9
        response = requests.delete("http://127.0.0.1:5000/api/delete/user/" + str(deleteId9))
        assert response.status_code == 200

    def test_delete2_delete_user_fail(self):
        response = requests.delete("http://127.0.0.1:5000/api/delete/user/1")
        assert response.status_code == 418

    @classmethod
    def tearDownClass(cls):
        #DELETE USED CLASSES ETC
        global deleteId2
        response = requests.delete("http://127.0.0.1:5000/api/delete/interest/" + str(deleteId2))
        assert response.status_code == 200

        global deleteId4
        response = requests.delete("http://127.0.0.1:5000/api/delete/apartment/" + str(deleteId4))
        assert response.status_code == 200

        global deleteId6
        response = requests.delete("http://127.0.0.1:5000/api/delete/rental/" + str(deleteId6))
        assert response.status_code == 200

        global deleteId8
        response = requests.delete("http://127.0.0.1:5000/api/delete/point/" + str(deleteId8))
        assert response.status_code == 200

        global deleteId10
        response = requests.delete("http://127.0.0.1:5000/api/delete/user/" + str(deleteId10))
        assert response.status_code == 200

if __name__ == '__main__':
    unittest.main()