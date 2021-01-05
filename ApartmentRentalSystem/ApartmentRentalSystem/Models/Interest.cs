using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace ApartmentRentalSystem.Models
{
    public class Interest
    {
        public int Id { get; set; }
        public int ApartmentId { get; set; }
        public int UserId { get; set; }
    }
}