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
        // GET: Main
        public async Task<ActionResult> Index()
        {

            string URL = BASE_URL + "api/read/apartment?active=true";
            HttpClient http = new HttpClient();
            HttpResponseMessage response = await http.GetAsync(new Uri(URL));

            if (response.IsSuccessStatusCode)
            {
                var content = await response.Content.ReadAsStringAsync();

                List<Apartment> listOfApartment = JsonConvert.DeserializeObject<List<Apartment>>(content);

                if (listOfApartment != null)
                {
                    // nu skall vi foreach:a varje item i html för att kunna skapa en data-view
                    return View(listOfApartment);
                }
                else
                {
                    // LISTAN ÄR TOM
                }

            }


            if (TempData["SuccessfullLogin"] != null)
            {
                ViewBag.Message = TempData["SuccessfullLogin"].ToString();
            }
            return View();
        }
        [HttpPost]
        public async Task<ActionResult> Index(int Maxprice = 0, int Minprice = 0, string location = null, int room = 0)
        {
            //Om alla värde är null så kommer en error. Behöver fixas
            //Lägga till fler if satser

            

            string URL = BASE_URL + "api/read/apartment/filter?" + GetParam("minprice", Minprice) + GetParam("maxprice", Maxprice) + GetParam("location", location) + GetParam("rooms", room);

            URL = URL.TrimEnd('&');

            //string URL_2 = BASE_URL + "api/read/apartment/filter?minprice=" + Minprice + "&maxprice=" + Minprice + "&location=" + location + "&rooms=" + room;
            //if ( location == null)
            //{
            //    URL = BASE_URL + "api/read/apartment/filter?minprice=" + Minprice + "&maxprice=" + Minprice + "&rooms=" + room;
            //}
            //else if (price != null || location == null || room == 0)
            //{
            //    URL = BASE_URL + "api/read/apartment/filter?minprice=" + price;
            //}
            //else if (price != null || location != null || room == 0)
            //{
            //    URL = BASE_URL + "api/read/apartment/filter?minprice=" + price;
            //}



            HttpClient http = new HttpClient();
            HttpResponseMessage response = await http.GetAsync(new Uri(URL));

            if (response.IsSuccessStatusCode)
            {
                var content = await response.Content.ReadAsStringAsync();

                List<Apartment> listOfApartment = JsonConvert.DeserializeObject<List<Apartment>>(content);

                if (listOfApartment != null)
                {
                    // nu skall vi foreach:a varje item i html för att kunna skapa en data-view
                    return View(listOfApartment);
                }
                else
                {
                    // LISTAN ÄR TOM
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
        private string GetParam(string name, int number)
        {
            if (number == 0)
            {
                return "";
            }
            else
            {
                return name + "=" + number+ "&";
            }
        }
        private string GetParam(string name, string text)
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

        public ActionResult Apartment()
        {

            return View();
        }
        
        public ActionResult ProfilePage()
        {
            return View();
        }
    }
}