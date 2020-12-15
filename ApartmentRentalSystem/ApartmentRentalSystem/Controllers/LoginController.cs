using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;
using System.Web;
using System.Web.Mvc;
using ApartmentRentalSystem.Models;

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
        public ActionResult Index(User inloggning)
        {
            
            bool result = CheckUser(inloggning).Result;
            // Here functionall Code. What will happen when we get answers.
            return View();
        }
        public async Task<bool> CheckUser(User inloggning)
        {
            string URL = BASE_URL + "api/login?username=" + inloggning.Username + "&password=" + inloggning.Password;
            HttpClient http = new HttpClient();
            HttpResponseMessage response = await http.GetAsync(new Uri(URL));

            if (response.IsSuccessStatusCode)
            {
                return true;
            }
            else
            {
                return false;
            }
        }
      
    }
}