using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using ShippingApp.Data;
using ShippingApp.Models;

namespace ShippingApp.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class ShipmentsController : ControllerBase
    {
        private readonly ShippingContext _context;
        private readonly ILogger<ShipmentsController> _logger;

        public ShipmentsController(ShippingContext context, ILogger<ShipmentsController> logger)
        {
            _context = context;
            _logger = logger;
        }

        // GET: api/shipments
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Shipment>>> GetShipments()
        {
            try
            {
                var shipments = await _context.Shipments
                    .OrderByDescending(s => s.CreatedAt)
                    .ToListAsync();
                
                _logger.LogInformation($"Retrieved {shipments.Count} shipments");
                return Ok(shipments);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving shipments");
                return StatusCode(500, "Internal server error while retrieving shipments");
            }
        }

        // GET: api/shipments/{id}
        [HttpGet("{id}")]
        public async Task<ActionResult<Shipment>> GetShipment(int id)
        {
            try
            {
                var shipment = await _context.Shipments.FindAsync(id);

                if (shipment == null)
                {
                    _logger.LogWarning($"Shipment with ID {id} not found");
                    return NotFound($"Shipment with ID {id} not found");
                }

                _logger.LogInformation($"Retrieved shipment with ID {id}");
                return Ok(shipment);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error retrieving shipment with ID {id}");
                return StatusCode(500, "Internal server error while retrieving shipment");
            }
        }

        // POST: api/shipments
        [HttpPost]
        public async Task<ActionResult<Shipment>> CreateShipment(Shipment shipment)
        {
            try
            {
                if (!ModelState.IsValid)
                {
                    return BadRequest(ModelState);
                }

                shipment.CreatedAt = DateTime.UtcNow;
                _context.Shipments.Add(shipment);
                await _context.SaveChangesAsync();

                _logger.LogInformation($"Created new shipment with ID {shipment.ShipmentId}");
                return CreatedAtAction(nameof(GetShipment), new { id = shipment.ShipmentId }, shipment);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating shipment");
                return StatusCode(500, "Internal server error while creating shipment");
            }
        }

        // DELETE: api/shipments/{id}
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteShipment(int id)
        {
            try
            {
                var shipment = await _context.Shipments.FindAsync(id);
                if (shipment == null)
                {
                    _logger.LogWarning($"Attempt to delete non-existent shipment with ID {id}");
                    return NotFound($"Shipment with ID {id} not found");
                }

                _context.Shipments.Remove(shipment);
                await _context.SaveChangesAsync();

                _logger.LogInformation($"Deleted shipment with ID {id}");
                return NoContent();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error deleting shipment with ID {id}");
                return StatusCode(500, "Internal server error while deleting shipment");
            }
        }
    }
}