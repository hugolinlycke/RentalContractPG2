import unittest
import sys
import json
import requests
import RentalService

class PointUnittest(unittest.TestCase):
    deleteId1 = 0
    deleteId2 = 0
    def test_create1_create_new_point(self):
        response = requests.post("http://127.0.0.1:5000/api/create/point", json= {'UserId': 2, 'Points':200})
        response_body = response.json()
        global deleteId1
        deleteId1 = response_body["Id"]
        assert response.status_code == 200

    def test_create1_5_create_new_point(self):
        response = requests.post("http://127.0.0.1:5000/api/create/point", json= {'UserId': 13, 'Points':200})
        response_body = response.json()
        global deleteId2
        deleteId2 = response_body["Id"]
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
        global deleteId2
        response = requests.put("http://127.0.0.1:5000/api/update/point", json = {'Id': str(deleteId2),'UserId':13, 'Points':500})
        response_body = response.json()
        assert response_body["Points"] == 500

    def test_update2_update_userId(self):
        global deleteId2
        response = requests.put("http://127.0.0.1:5000/api/update/point", json = {'Id': str(deleteId2),'UserId':12, 'Points':500})
        response_body = response.json()
        assert response_body["UserId"] == 12
    
    def test_update3_update_user_not_exist(self):
        response = requests.put("http://127.0.0.1:5000/api/update/point", json = {'Id': str(deleteId2),'UserId':-1, 'Points':200})
        assert response.status_code == 418
    
    def test_update4_update_user_that_already_exists(self):
        response = requests.put("http://127.0.0.1:5000/api/update/point", json = {'Id': str(deleteId2),'UserId':7, 'Points':200})
        assert response.status_code == 418

    def test_delete1_delete_user(self):
        global deleteId1
        response = requests.delete("http://127.0.0.1:5000/api/delete/point/" + str(deleteId1))
        assert response.status_code == 200

    def test_delete2_delete_user_fail(self):
        response = requests.delete("http://127.0.0.1:5000/api/delete/point/-1")
        assert response.status_code == 418

    @classmethod
    def tearDownClass(cls):
        #DELETE USED CLASSES ETC
        global deleteId2
        response = requests.delete("http://127.0.0.1:5000/api/delete/point/" + str(deleteId2))
        assert response.status_code == 200


if __name__ == '__main__':
    unittest.main()