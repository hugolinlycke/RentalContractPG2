using ApartmentRentalSystem.Controllers;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using System;

namespace UnitTestProject1
{
    [TestClass]
    public class UnitTest1
    {
        MainController mainController = new MainController();


        //MAXPRICE AND MINPRICE SEARCH TESTING
        [TestMethod]
        public void Searching_minprice_500_maxprice_5000()
        {
            string result = mainController.GetParam("minprice", 500, "maxprice", 5000);
            Assert.AreEqual("minprice=500&maxprice=5000&", result);
        }
        [TestMethod]
        public void Searching_minprice_6000_maxprice_600()
        {
            string result = mainController.GetParam("minprice", 6000, "maxprice", 600);
            Assert.AreNotEqual("minprice=6000&maxprice=600&", result);
        }
        [TestMethod]
        public void Searching_minprice_7000_maxprice_700()
        {
            string result = mainController.GetParam("minprice", 7000, "maxprice", 700);
            Assert.AreEqual("", result);
        }
        [TestMethod]
        public void Searching_minprice_0_maxprice_0()
        {
            string result = mainController.GetParam("minprice", 0, "maxprice", 0);
            Assert.AreEqual("", result);
        }
        [TestMethod]
        public void Searching_minprice_NegativeValue1_maxprice_NegativeValue1()
        {
            string result = mainController.GetParam("minprice", -1, "maxprice", -1);
            Assert.AreEqual("", result);
        }


        // LOCATION SREACHBAR TESTING 
        [TestMethod]
        public void Searching_Location_Null()
        {
            string result = mainController.GetParam("location", null);
            Assert.AreEqual("", result);
        }
        [TestMethod]
        public void Searching_Location_EmptyString()
        {
            string result = mainController.GetParam("location", "");
            Assert.AreEqual("", result);
        }
        [TestMethod]
        public void Searching_Location_Centrum_Value()
        {
            string result = mainController.GetParam("location", "Centrum");
            Assert.AreEqual("location=Centrum&", result);
        }

        // ROOM SREACHBAR TESTING 
        [TestMethod]
        public void Searching_Room_Negative1()
        {
            string result = mainController.GetParam("room", -1);
            Assert.AreEqual("", result);
        }
        [TestMethod]
        public void Searching_Room_0()
        {
            string result = mainController.GetParam("room", 0);
            Assert.AreEqual("", result);
        }
        [TestMethod]
        public void Searching_Room_1()
        {
            string result = mainController.GetParam("room", 1);
            Assert.AreEqual("room=1&", result);
        }
    }
}
