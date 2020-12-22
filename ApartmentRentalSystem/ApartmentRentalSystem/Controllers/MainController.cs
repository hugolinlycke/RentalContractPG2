using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace ApartmentRentalSystem.Controllers
{
    public class MainController : Controller
    {
        // GET: Main
        public ActionResult Index()
        {
            if (TempData["SuccessfullLogin"] != null)
            {
                ViewBag.Message = TempData["SuccessfullLogin"].ToString();
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