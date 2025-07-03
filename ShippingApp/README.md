# ShippingApp - .NET 7 Web API

A RESTful Web API for managing shipments built with .NET 7, Entity Framework Core, and SQLite.

## Features

- **Shipment Management**: Create, retrieve, and delete shipments
- **SQLite Database**: Lightweight database with Entity Framework Core
- **Automatic Migrations**: Database schema automatically managed
- **Swagger Documentation**: Interactive API documentation
- **CORS Enabled**: Cross-origin requests supported
- **Comprehensive Logging**: Request and error logging

## Project Structure

```
ShippingApp/
├── Controllers/
│   └── ShipmentsController.cs    # API endpoints
├── Data/
│   └── ShippingContext.cs        # EF Core database context
├── Models/
│   └── Shipment.cs              # Shipment entity model
├── Migrations/                   # EF Core migrations
├── Program.cs                   # Application entry point
└── appsettings.json            # Configuration
```

## API Endpoints

### Base URL: `/api/shipments`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/shipments` | Get all shipments |
| GET | `/api/shipments/{id}` | Get shipment by ID |
| POST | `/api/shipments` | Create new shipment |
| DELETE | `/api/shipments/{id}` | Delete shipment by ID |

## Shipment Model

```json
{
  "shipmentId": 0,
  "senderName": "string",
  "senderPhone": "string",
  "shipmentType": "string",
  "shipmentWeightKg": 0.0,
  "receiverName": "string",
  "receiverPhone": "string",
  "createdAt": "2024-06-24T00:00:00Z"
}
```

## Getting Started

### Prerequisites

- .NET 7.0 SDK
- SQLite (included with .NET)

### Running the Application

1. Navigate to the project directory:
   ```bash
   cd ShippingApp/ShippingApp
   ```

2. Build the project:
   ```bash
   dotnet build
   ```

3. Run the application:
   ```bash
   dotnet run
   ```

4. Access the API:
   - **Base URL**: `https://localhost:7000` or `http://localhost:5000`
   - **Swagger UI**: `https://localhost:7000/swagger`

### Database

The application uses SQLite with automatic database creation. The database file (`shipping.db`) will be created automatically in the project root when the application first runs.

## Sample API Usage

### Create a New Shipment
```bash
POST /api/shipments
Content-Type: application/json

{
  "senderName": "John Doe",
  "senderPhone": "123-456-7890",
  "shipmentType": "Standard",
  "shipmentWeightKg": 2.5,
  "receiverName": "Jane Smith",
  "receiverPhone": "098-765-4321"
}
```

### Get All Shipments
```bash
GET /api/shipments
```

### Get Shipment by ID
```bash
GET /api/shipments/1
```

### Delete Shipment
```bash
DELETE /api/shipments/1
```

## Configuration

Database connection string can be modified in `appsettings.json`:

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Data Source=shipping.db"
  }
}
```

## Development

### Adding Migrations

When modifying the data model:

```bash
dotnet ef migrations add <MigrationName>
dotnet ef database update
```

### Project Dependencies

- Microsoft.EntityFrameworkCore.Sqlite (7.0.20)
- Microsoft.EntityFrameworkCore.Tools (7.0.20)
- Microsoft.EntityFrameworkCore.Design (7.0.20)

## Error Handling

The API includes comprehensive error handling with appropriate HTTP status codes:

- **200 OK**: Successful operations
- **201 Created**: Successful creation
- **204 No Content**: Successful deletion
- **400 Bad Request**: Invalid input data
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server errors

All errors are logged with detailed information for debugging purposes.