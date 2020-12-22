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
        public ActionResult Index()
        {
            if (TempData["SuccessfullLogin"] != null)
            {
                ViewBag.Message = TempData["SuccessfullLogin"].ToString();
            }



            return View();
        }
        [HttpPost]
        public async Task<ActionResult> Index(User inloggning)
        {

            string URL = BASE_URL + "api/read/apartments";
            HttpClient http = new HttpClient();
            HttpResponseMessage response = await http.GetAsync(new Uri(URL));

            if (response.IsSuccessStatusCode)
            {
                var content = await response.Content.ReadAsStringAsync();

                User activeUser = JsonConvert.DeserializeObject<User>(content);

                if (activeUser.Username != null || activeUser.Password != null)
                {

                    TempData["SuccessfullLogin"] = "You successfully logged in!";
                    return RedirectToAction("Index", "Main", inloggning);
                    //Remove "Login" Text from nav bar then add profile button, if possible

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