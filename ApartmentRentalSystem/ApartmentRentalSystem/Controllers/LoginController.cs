using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Web;
using System.Web.Mvc;

namespace ApartmentRentalSystem.Controllers
{
    public class LoginController : Controller
    {
        private string BASE_URL = "http://127.0.0.1:5000/";
        public ActionResult Index()
        {
            return View();
        }
        [HttpPost]
        public ActionResult Index(Models.User inloggning)
        {
            
            
            return View();
        }
        public async void CheckUser()
        {
            string URL = BASE_URL + "/api/login";
            HttpClient http = new HttpClient();
            HttpResponseMessage response = await http.GetAsync(new Uri(URL));

            if (response.IsSuccessStatusCode)
            {

            }
        }
      
    }
}