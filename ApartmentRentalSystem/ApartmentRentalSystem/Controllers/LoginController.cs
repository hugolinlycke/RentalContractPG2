using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Web;
using System.Web.Mvc;
using ApartmentRentalSystem.Models;
using Newtonsoft.Json;

namespace ApartmentRentalSystem.Controllers
{
    public class LoginController : Controller
    {
        private string BASE_URL = "http://127.0.0.1:5000/";

        public ActionResult Index()
        {
            if (TempData["SuccessfullCreateAccount"] != null)
            {
                ViewBag.Message = TempData["SuccessfullCreateAccount"].ToString();
            }
            

            return View();
        }
        [HttpPost]
        public async Task<ActionResult> Index(User inloggning) // Checking the Login function. 
        {

            string URL = BASE_URL + "api/login?username=" + inloggning.Username + "&password=" + inloggning.Password;
            HttpClient http = new HttpClient();
            HttpResponseMessage response = await http.GetAsync(new Uri(URL));

            if (response.IsSuccessStatusCode)
            {
                var content = await response.Content.ReadAsStringAsync();

                User activeUser = JsonConvert.DeserializeObject<User>(content);

                if (activeUser.Username != null || activeUser.Password != null)
                {

                    TempData["SuccessfullLogin"] = "You successfully logged in!";
                    // ADD SESSION FOR LOGGIN
                    Session["User"] = activeUser;

                    return RedirectToAction("Index", "Main", activeUser);
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
        public ActionResult CreateAccount() 
        {
            return View();
        }
        [HttpPost]
        public async Task<ActionResult> CreateAccount(User inloggning) // When you create an account this function runs
        {

            if (inloggning.Username == null || inloggning.Password == null)
            {
                ViewBag.Message = String.Format("Please fill both Username and Password", DateTime.Now.ToString());
                return View();
            }

            string URL = BASE_URL + "api/create/user";
            HttpClient http = new HttpClient();
            
            string jsonString = JsonConvert.SerializeObject(inloggning);
            var newContent = new StringContent(jsonString, Encoding.UTF8, "application/json");
            var newResponse = await http.PostAsync(URL, newContent);

            if (newResponse.IsSuccessStatusCode)
            {
                if (newResponse != null)
                {
                    TempData["SuccessfullCreateAccount"] = "You successfully created an account!";
                    return RedirectToAction("Index");
                }
            }
            else if (!newResponse.IsSuccessStatusCode)
            {
                if (newResponse.StatusCode.ToString() == "NotFound")
                {
                    ViewBag.Message = String.Format("You could not connect to the API, Please try again", DateTime.Now.ToString());
                    return View();
                }
                else
                {
                    ViewBag.Message = String.Format("There is already an account with that username or password", DateTime.Now.ToString());
                    return View();
                }
            }
            return View();
        }

    }

}