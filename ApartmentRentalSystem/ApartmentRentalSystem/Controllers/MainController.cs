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

                List<Apartment> listOfApartment = JsonConvert.DeserializeObject<List<Apartment>>(content);

                if (listOfApartment != null)
                {
                    if (Session["User"] != null)
                    {
                        // 
                    }
                    if (TempData["SuccessfullLogin"] != null)
                    {
                        ViewBag.Message = TempData["SuccessfullLogin"].ToString();
                    }
                    // nu skall vi foreach:a varje item i html för att kunna skapa en data-view
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
        public async Task<ActionResult> Index(int Maxprice = 0, int Minprice = 0, string location = null, int room = 0)
        {
            //Om alla värde är null så kommer en error. Behöver fixas
            //Lägga till fler if satser


            string URL = BASE_URL + "api/read/apartment/filter?" + GetParam("minprice", Minprice, "maxprice", Maxprice) + GetParam("location", location) + GetParam("rooms", room);
            //string URL = BASE_URL + "api/read/apartment/filter?" + GetParam("minprice", Minprice) + GetParam("maxprice", Maxprice) + GetParam("location", location) + GetParam("rooms", room);

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
        public string GetParam(string name, int number)
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
        public string GetParam(string name, string text)
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
        public string GetParam(string name1, int number1, string name2, int number2)
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