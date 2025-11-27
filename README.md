# API Contract Management System

This ‘API contract management system’ provides an internal company management system for contracts made with clients. This ‘API contract management system’ will be used for internal company employees/ management to keep track of current, past and future contracts. The system would be able to centralize all data needed to be accessed to view client contracts made.  

## Features

### Core Functionality
- **User Management**: Complete user authentication and authorization with JWT
- **Client Management**: Manage client companies and their information
- **Product Management**: Define and manage API products
- **Contract Management**: Create and manage contracts between clients and the company
- **Subscription Management**: Handle different subscription types with flexible pricing models
- **Subscription Tiers**: Define pricing tiers with various strategies (Pick, Fill, Flat, Fixed)

### Key Features
- **JWT Authentication**: Secure user authentication and authorization
- **Flexible Pricing Models**: Support for Fixed and Variable pricing
- **Multiple Pricing Strategies**: Pick, Fill, Flat, and Fixed strategies
- **RESTful API**: Complete REST API with proper HTTP methods
- **Interactive Documentation**: Built-in Swagger UI for API documentation
- **PostgreSQL Support**: Robust database with UUID primary keys
- **Soft Delete**: Archive functionality instead of hard deletion
- **Audit Trail**: Track creation and modification timestamps and users

## Technologies

- **Backend**: Flask (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **Documentation**: Swagger UI


## Prerequisites

- Python 3.7+
- PostgreSQL database

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/RohanMankame/API-Contract-Management-System.git
   cd API-Contract-Management-System
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/your_database_name
   JWT_SECRET_KEY=your_super_secret_jwt_key_here
   ```

5. **Initialize the database**
   ```bash
   python run.py
   ```

## Running the Application

```bash
python run.py
```

The application will start on `http://localhost:5000`

## API Documentation

Access the interactive Swagger documentation at: `http://localhost:5000/api/docs`

## Authentication

### Initial Setup
1. Create the first user (no authentication required):
   ```
   POST /UsersFirst
   ```

2. Login to get JWT token:
   ```
   POST /login
   ```

3. Use the JWT token in the Authorization header for subsequent requests:
   ```
   Authorization: Bearer <your_jwt_token>
   ```

## API Endpoints

### Authentication
- `POST /login` - User login
- `GET /protected` - Test protected endpoint

### Users
- `POST /UsersFirst` - Create first user (no auth required)
- `POST /Users` - Create new user
- `GET /Users` - Get all users
- `GET /Users/{id}` - Get user by ID
- `PUT /Users/{id}` - Update user
- `DELETE /Users/{id}` - Archive user
- `GET /Users/{id}/Contracts` - Get contracts created by user

### Clients
- `POST /Clients` - Create new client
- `GET /Clients` - Get all clients
- `GET /Clients/{id}` - Get client by ID
- `PUT /Clients/{id}` - Update client
- `DELETE /Clients/{id}` - Archive client

### Products
- `POST /Products` - Create new product
- `GET /Products` - Get all products
- `GET /Products/{id}` - Get product by ID
- `PUT /Products/{id}` - Update product
- `DELETE /Products/{id}` - Archive product

### Contracts
- `POST /Contracts` - Create new contract
- `GET /Contracts` - Get all contracts
- `GET /Contracts/{id}` - Get contract by ID
- `PUT /Contracts/{id}` - Update contract
- `DELETE /Contracts/{id}` - Archive contract

### Subscriptions
- `POST /Subscriptions` - Create new subscription
- `GET /Subscriptions` - Get all subscriptions
- `GET /Subscriptions/{id}` - Get subscription by ID
- `PUT /Subscriptions/{id}` - Update subscription
- `DELETE /Subscriptions/{id}` - Archive subscription

### Subscription Tiers
- `POST /Subscription_tiers` - Create new tier
- `GET /Subscription_tiers` - Get all tiers
- `GET /Subscription_tiers/{id}` - Get tier by ID
- `PUT /Subscription_tiers/{id}` - Update tier
- `DELETE /Subscription_tiers/{id}` - Archive tier

## Database Schema

### Core Models

**User**: System employees who can create and manage contracts
- UUID primary key
- Email, password hash, full name
- Audit fields (created_by, updated_by, timestamps)
- Soft delete support

**Client**: Company clients who purchase API contracts
- UUID primary key
- Company details (name, email, phone, address)
- Audit fields and soft delete support

**Product**: API products offered by the company
- UUID primary key
- API name and description
- Audit fields and soft delete support

**Contract**: Agreements between clients and the company
- UUID primary key
- Links to client and creator
- Contract name and details
- Audit fields and soft delete support

**Subscription**: Subscription types for products within contracts
- UUID primary key
- Links to contract and product
- Pricing type (Fixed/Variable) and strategy (Pick/Fill/Flat/Fixed)
- Audit fields and soft delete support

**Subscription_tier**: Pricing tiers for subscriptions
- UUID primary key
- Call limits (min/max)
- Date ranges and pricing details
- Base price and per-tier pricing options

## Security Features

- JWT-based authentication
- Password hashing using Werkzeug
- Protected endpoints requiring valid tokens
- User-based audit trails
- Soft delete for data preservation

## Pricing Strategies

The system supports multiple pricing strategies:

1. **Pick**: Pay per tier based on usage
2. **Fill**: Fill up tiers sequentially
3. **Flat**: Flat rate pricing
4. **Fixed**: Fixed pricing regardless of usage


## Author

- [RohanMankame](https://github.com/RohanMankame)
