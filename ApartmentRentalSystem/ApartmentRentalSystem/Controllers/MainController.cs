using ApartmentRentalSystem.Models;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;
using System.Web;
using System.Web.Mvc;

namespace ApartmentRentalSystem.Controllers
{
    public class MainController : Controller
    {
        private string BASE_URL = "http://127.0.0.1:5000/";

        public int Function()
        {
            throw new NotImplementedException();
        }

        // GET: Main
        public async Task<ActionResult> Index()
        {

            string URL = BASE_URL + "api/read/apartment?active=true";
            HttpClient http = new HttpClient();
            HttpResponseMessage response = await http.GetAsync(new Uri(URL));

            if (response.IsSuccessStatusCode)
            {
                var content = await response.Content.ReadAsStringAsync();

                List<Apartment> listOfApartment = JsonConvert.DeserializeObject<List<Apartment>>(content); // Every item we get from the api we put into a list and later display this list in th view

                if (listOfApartment != null)
                {
                    if (Session["User"] != null)
                    {
                        // A Session for user crediential
                    }
                    if (TempData["SuccessfullLogin"] != null)
                    {
                        ViewBag.Message = TempData["SuccessfullLogin"].ToString();
                    }
                    return View(listOfApartment);
                }
                else
                {
                    // LISTAN ÄR TOM
                }

            }


            
            return View();
        }
        [HttpPost]
        public async Task<ActionResult> Index(int Maxprice = 0, int Minprice = 0, string location = null, int room = 0) //This method runs When searching for a filtered apartment
        {

            string URL = BASE_URL + "api/read/apartment/filter?" + GetParam("minprice", Minprice, "maxprice", Maxprice) + GetParam("location", location) + GetParam("rooms", room); //Calls 3 diffrent functions to build up the api based on the inputs given in the seachbar
            URL = URL.TrimEnd('&');

            HttpClient http = new HttpClient();
            HttpResponseMessage response = await http.GetAsync(new Uri(URL));

            if (response.IsSuccessStatusCode)
            {
                var content = await response.Content.ReadAsStringAsync();

                List<Apartment> listOfApartment = JsonConvert.DeserializeObject<List<Apartment>>(content);

                if (listOfApartment != null)
                {
                    if (TempData["ApartmentRequirmentsSearch"] != null)
                    {
                        ViewBag.Message = TempData["ApartmentRequirmentsSearch"].ToString();
                    }
                    return View(listOfApartment);
                }
                else
                {
                    // IF the list is emtpy
                }

            }
            else if (!response.IsSuccessStatusCode)
            {
                if (response.StatusCode.ToString() == "NotFound")
                {
                    ViewBag.Message = String.Format("You could not connect to the API, Please try again later", DateTime.Now.ToString());
                    return View();
                }
                else
                {
                    ViewBag.Message = String.Format("You have entered wrong user credentials, Please try again", DateTime.Now.ToString());
                    return View();
                }

            }


            return View();
        }
        public string GetParam(string name, int number) // Function that checks the "Room" input from the search of apartments
        {
            if (number <= 0)
            {
                if (number < 0)
                {
                    TempData["ApartmentRequirmentsSearch"] = "You need to enter a positive number in room input! Please try again.";
                    return "";
                }
                return "";
            }
            else
            {
                return name + "=" + number+ "&";
            }
        }
        public string GetParam(string name, string text) // Function that checks the "Location" input from the search of apartments
        {
            if (text == null || text=="")
            {
                return "";
            }
            else
            {
                return name + "=" + text + "&";
            }
        }
        public string GetParam(string name1, int number1, string name2, int number2) // Function that checks the "Minprice" and "Maxprice" input from the search of apartments
        {
            if (number1 <= 0 || number2 <= 0)
            {
                if (number1 == 0 & number2 == 0)
                {
                    return "";
                }
                TempData["ApartmentRequirmentsSearch"] = "You need to enter both Min-Price and Max-price";
                return "";
            }
            else
            {
                if (number1 > number2)
                {
                    TempData["ApartmentRequirmentsSearch"] = "Min-Price cant be greater then Max-Price, Please try again";
                    return "";
                }
                return name1 + "=" + number1 + "&" + name2 + "=" + number2 + "&";
            }
        }


        public async Task<ActionResult> ApartmentAsync(int id)
        {
            if (id != 0)
            {
                string URL = BASE_URL + "api/read/apartment?active=true&id=" + id;
                HttpClient http = new HttpClient();
                HttpResponseMessage response = await http.GetAsync(new Uri(URL));

                if (response.IsSuccessStatusCode)
                {
                    var content = await response.Content.ReadAsStringAsync();
                    List<Apartment> listOfApartment = JsonConvert.DeserializeObject<List<Apartment>>(content);

                    return View(listOfApartment);
                }
            }
            return View();
        }
        [HttpPost]
        public async Task<ActionResult> ApartmentAsync(int Apartmentid, int LandlordId) //This funktions isn't done. Used to entere the interest queue as the user.
        {
            if (Apartmentid != 0)
            {
                string URL = BASE_URL + "api/create/interest?ApartmentId=" + Apartmentid + "&UserId=" + 1;
                HttpClient http = new HttpClient();
                HttpResponseMessage response = await http.GetAsync(new Uri(URL));

                if (response.IsSuccessStatusCode)
                {
                    var content = await response.Content.ReadAsStringAsync();
                    List<Interest> listOfInterest = JsonConvert.DeserializeObject<List<Interest>>(content);

                    return View(listOfInterest);
                }
            }
            return View();
        }

        public ActionResult ProfilePage() // this function isn't done
        {
            return View();
        }
    }
}