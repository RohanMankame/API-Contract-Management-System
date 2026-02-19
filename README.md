# API Contract Management System

This is an internal company management system for contracts made with clients. The API Contract Management System is used by internal company employees and management to keep track of current, past, and future contracts. The system centralizes all data needed to view and manage client contracts.

## 🚀 Quick Links

- **Deployed Project**: https://api-contract-management-system-frontend.onrender.com 
- **Frontend Repository**: https://github.com/RohanMankame/api_contract_manager
- **API Documentation**: https://api-contract-management-system.onrender.com/api/docs



## ✨ Features

### Core Functionality
- **User Management**: Complete user authentication and authorization with JWT
- **Client Management**: Manage client companies and their information
- **Product Management**: Define and manage API products
- **Contract Management**: Create and manage contracts between clients and the company
- **Subscription Management**: Handle different subscription types with flexible pricing models
- **Rate Cards**: Define pricing rates for different time periods
- **Subscription Tiers**: Define pricing tiers with various strategies (Pick, Fill, Flat, Fixed)

### Key Features
- **JWT Authentication**: Secure user authentication and authorization
- **Flexible Pricing Models**: Support for Fixed and Variable pricing
- **Multiple Pricing Strategies**: Pick, Fill, Flat, and Fixed strategies
- **RESTful API**: Complete REST API with proper HTTP methods and status codes
- **Interactive Documentation**: Built-in Swagger UI for API documentation
- **PostgreSQL Support**: Robust relational database with UUID primary keys
- **Soft Delete**: Archive functionality instead of hard deletion
- **Audit Trail**: Track creation and modification timestamps and user IDs
- **Data Validation**: Comprehensive input validation and error handling

## 🛠️ Technologies

- **Backend Framework**: Flask (Python 3.7+)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **API Documentation**: Swagger UI
- **ORM**: SQLAlchemy with Marshmallow for serialization
- **CORS**: Flask-CORS for cross-origin requests

## 📦 Prerequisites

- Python 3.7 or higher
- PostgreSQL 10 or higher
- pip (Python package manager)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/RohanMankame/API-Contract-Management-System.git
   cd API-Contract-Management-System
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root with the following variables:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/api_contract_db
   JWT_SECRET_KEY=your_super_secret_jwt_key_here
   FLASK_ENV=development
   ```

5. **Initialize the database & starting application**
   ```bash
   python run.py
   ```
   This will create all necessary tables in your PostgreSQL database.


The application will start on `http://localhost:5000`



## 📂 Project Structure

```
API-Contract-Manager/
├── blueprints/               # Flask route blueprints
│   ├── auth.py              # Authentication routes
│   ├── user.py              # User management routes
│   ├── client.py            # Client management routes
│   ├── product.py           # Product management routes
│   ├── contract.py          # Contract management routes
│   ├── subscription.py       # Subscription routes
│   ├── rate_card.py         # Rate card routes
│   └── subscription_tier.py  # Subscription tier routes
├── models/                   # SQLAlchemy database models
│   ├── client.py
│   ├── contract.py
│   ├── product.py
│   ├── subscription.py
│   ├── rate_card.py
│   ├── subscription_tier.py
│   ├── user.py
│   └── mixins.py            # Reusable model mixins
├── schemas/                  # Marshmallow serialization schemas
│   ├── client_schema.py
│   ├── contract_schema.py
│   ├── product_schema.py
│   ├── subscription_schema.py
│   ├── rate_card_schema.py
│   ├── subscription_tier_schema.py
│   └── user_schema.py
├── utils/                    # Utility functions
│   └── response.py          # Standard response formatting
├── tests/                    # Test suite
│   ├── integration/         # Integration tests
│   ├── factories.py         # Test data factories
│   └── conftest.py          # Pytest configuration
├── app.py                   # Flask application factory
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
└── README.md               
```

### Integration with Backend

The frontend communicates with the backend API at `https://api-contract-management-system.onrender.com/`. CORS is configured to allow requests from the frontend domain.

## 🧪 Testing

Run the test suite:
```bash
pytest
```

For coverage report:
```bash
pytest --cov=.
```

For specific test file:
```bash
pytest tests/integration/test_name.py
```


## Author

- [RohanMankame](https://github.com/RohanMankame)
