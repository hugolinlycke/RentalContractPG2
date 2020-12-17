﻿using System;
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
            return View();
        }
        [HttpPost]
        public async Task<ActionResult> Index(User inloggning)
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
            

            // Here functionall Code. What will happen when we get answers.
            return View();
        }
        public ActionResult CreateAccount() 
        {
            return View();
        }
        [HttpPost]
        public async Task<ActionResult> CreateAccount(User inloggning)
        {
            string URL = BASE_URL + "api/create/user";
            HttpClient http = new HttpClient();
            
            string jsonString = JsonConvert.SerializeObject(inloggning);
            var newContent = new StringContent(jsonString, Encoding.UTF8, "application/json");
            var newResponse = await http.PostAsync(URL, newContent);

            if (newResponse.IsSuccessStatusCode)
            {
                if (newResponse != null)
                {
                    return RedirectToAction("Index");
                }
                else
                {
                    Console.WriteLine("Account already with that information");
                }
            }
            else
            {
                //CRITICAL SERVER FAIL,  MAKE A POP UP
                Console.WriteLine("failed Server Connection");
            }
             return View();
        }
        }
}