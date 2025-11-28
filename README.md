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

## Author

- [RohanMankame](https://github.com/RohanMankame)
