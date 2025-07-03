using System.ComponentModel.DataAnnotations;

namespace ShippingApp.Models
{
    public class Shipment
    {
        [Key]
        public int ShipmentId { get; set; }
        
        [Required]
        [StringLength(100)]
        public string SenderName { get; set; } = string.Empty;
        
        [Required]
        [StringLength(20)]
        public string SenderPhone { get; set; } = string.Empty;
        
        [Required]
        [StringLength(50)]
        public string ShipmentType { get; set; } = string.Empty;
        
        [Required]
        [Range(0.1, 1000.0)]
        public double ShipmentWeightKg { get; set; }
        
        [Required]
        [StringLength(100)]
        public string ReceiverName { get; set; } = string.Empty;
        
        [Required]
        [StringLength(20)]
        public string ReceiverPhone { get; set; } = string.Empty;
        
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    }
}