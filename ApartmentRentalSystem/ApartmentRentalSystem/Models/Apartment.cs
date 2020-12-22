using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace ApartmentRentalSystem.Models
{
    public class Apartment
    {
        
            public bool Active { get; set; }
            public string Address { get; set; }
            public int Id { get; set; }
            public string Information { get; set; }
            public int LandlordId { get; set; }
            public string Location { get; set; }
            public string NumberOfRooms { get; set; }
            public float Price { get; set; }
            public string SizeOfApartment { get; set; }
        
    }
}