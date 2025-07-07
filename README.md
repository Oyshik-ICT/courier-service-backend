# Courier Backend API

A comprehensive Django REST API for managing courier/delivery services with user authentication, order management, and payment processing via Stripe.

## 🚀 Live Demo

**Base URL:** `https://web-production-34587.up.railway.app/`

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Local Setup](#local-setup)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [User Roles](#user-roles)
- [Admin Credentials](#admin-credentials)
- [Usage Examples](#usage-examples)
- [Payment Integration](#payment-integration)
- [Deployment](#deployment)

## ✨ Features

- **User Management**: Custom user model with role-based access (Admin, Regular User, Delivery Man)
- **Order Management**: Create, track, and manage courier orders
- **Payment Processing**: Stripe integration for secure payments
- **Role-based Permissions**: Different access levels for different user types
- **Order Tracking**: Unique tracking numbers for each order
- **RESTful API**: Clean and well-documented API endpoints
- **JWT Authentication**: Secure token-based authentication

## 🛠 Tech Stack

- **Backend**: Django 5.2.4, Django REST Framework 3.16.0
- **Database**: PostgreSQL (Production), SQLite (Development)
- **Authentication**: JWT (Simple JWT)
- **Payment**: Stripe API
- **Deployment**: Railway
- **Other**: Django Silk (API profiling), Gunicorn (WSGI server)

## 📁 Project Structure

```
courier_backend/
├── accounts/                 # User management & authentication
│   ├── models.py            # Custom user model
│   ├── serializers.py       # User serializers
│   ├── views.py             # User viewsets
│   ├── permissions.py       # Custom permissions
│   └── choices.py           # User role choices
├── order/                   # Order management
│   ├── models.py            # Order model
│   ├── serializers.py       # Order serializers
│   ├── views.py             # Order viewsets
│   └── choices.py           # Order status choices
├── payment/                 # Payment processing
│   └── views.py             # Stripe payment views
└── courier_backend/         # Project settings
    ├── settings.py          # Django settings
    └── urls.py              # URL configuration
```

## 🔧 Local Setup

### Prerequisites

- Python 3.11.9
- pip (Python package manager)
- Git

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Oyshik-ICT/courier-service-backend.git

   cd courier-service-backend
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   BASE_URL=http://localhost:8000
   STRIPE_SECRET_KEY=your-stripe-secret-key
   STRIPE_PUBLIC_KEY=your-stripe-public-key
   ```

5. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

   The API will be available at `http://localhost:8000/`

## 👥 User Roles

### 1. Admin (`ADMIN`)
- Full access to all resources
- Can manage all users and orders
- **Only admins can create other admin users**
- Access to admin panel
- Access to `/api/v1/auth/admin-users/` endpoints

### 2. Regular User (`REGULAR_USER`)
- Can create and manage their own orders
- Can make payments
- Limited to their own data

### 3. Delivery Man (`DELIVERY_MAN`)
- Can view assigned orders
- Can update order status
- Limited to delivery-related operations

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### Get Authentication Token

**POST** `/api/v1/auth/api/token/`

```json
{
  "email": "user@example.com",
  "password": "your_password"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Refresh Token

**POST** `/api/v1/auth/api/token/refresh/`

```json
{
  "refresh": "your_refresh_token_here"
}
```

## 🔑 Admin Credentials

A superuser has been created for testing purposes:

> **⚠️ IMPORTANT: Default Admin Credentials**
> 
> **Email:** `admin@gmail.com`  
> **Password:** `admin123456@`
> 
> **🔒 Security Note:** These are test credentials. In production, always change the default password immediately after first login.

### Admin Access

Only users with `ADMIN` role can:
- Access `/api/v1/auth/admin-users/` endpoints
- Create other admin users
- View and manage all users and orders

## 🛣 API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| POST | `/api/v1/auth/api/token/` | Login & get tokens | No |
| POST | `/api/v1/auth/api/token/refresh/` | Refresh access token | No |

### User Management Endpoints

| Method | Endpoint | Description | Authentication | Permission |
|--------|----------|-------------|----------------|------------|
| GET | `/api/v1/auth/users/` | List users | Yes | Authenticated |
| POST | `/api/v1/auth/users/` | Register new user | No | None |
| GET | `/api/v1/auth/users/{id}/` | Get user details | Yes | Authenticated |
| PUT | `/api/v1/auth/users/{id}/` | Update user | Yes | Authenticated |
| DELETE | `/api/v1/auth/users/{id}/` | Delete user | Yes | Authenticated |

### Admin User Management Endpoints

| Method | Endpoint | Description | Authentication | Permission |
|--------|----------|-------------|----------------|------------|
| GET | `/api/v1/auth/admin-users/` | List admin users | Yes | **Admin Only** |
| POST | `/api/v1/auth/admin-users/` | Create admin user | Yes | **Admin Only** |
| GET | `/api/v1/auth/admin-users/{id}/` | Get admin user details | Yes | **Admin Only** |
| PUT | `/api/v1/auth/admin-users/{id}/` | Update admin user | Yes | **Admin Only** |
| DELETE | `/api/v1/auth/admin-users/{id}/` | Delete admin user | Yes | **Admin Only** |

### Order Management Endpoints

| Method | Endpoint | Description | Authentication | Permission |
|--------|----------|-------------|----------------|------------|
| GET | `/api/v1/orders/orders-detail/` | List orders | Yes | Regular User/Admin |
| POST | `/api/v1/orders/orders-detail/` | Create new order | Yes | Regular User/Admin |
| GET | `/api/v1/orders/orders-detail/{id}/` | Get order details | Yes | Regular User/Admin |
| PUT | `/api/v1/orders/orders-detail/{id}/` | Update order | Yes | Regular User/Admin |
| DELETE | `/api/v1/orders/orders-detail/{id}/` | Delete order | Yes | Regular User/Admin |

### Delivery Man Endpoints

| Method | Endpoint | Description | Authentication | Permission |
|--------|----------|-------------|----------------|------------|
| GET | `/api/v1/orders/delivery/` | List assigned orders | Yes | Delivery Man |
| PATCH | `/api/v1/orders/delivery/{order_id}/` | Update order status | Yes | Delivery Man |

### Payment Endpoints

| Method | Endpoint | Description | Authentication | Permission |
|--------|----------|-------------|----------------|------------|
| POST | `/api/v1/payment/order/{order_id}/` | Create payment session | Yes | Regular User |
| GET | `/api/v1/payment/payment-success/` | Payment success callback | No | None |
| GET | `/api/v1/payment/payment-cancel/` | Payment cancel callback | No | None |

## 📝 Usage Examples

### Using Postman

#### 1. Admin Login

**POST** `https://web-production-34587.up.railway.app/api/v1/auth/api/token/`

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "email": "admin@gmail.com",
  "password": "admin123456@"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### 2. Create Admin User (Admin Only)

**POST** `https://web-production-34587.up.railway.app/api/v1/auth/admin-users/`

**Headers:**
```
Authorization: Bearer YOUR_ADMIN_ACCESS_TOKEN
Content-Type: application/json
```

**Body:**
```json
{
  "email": "newadmin@example.com",
  "password": "SecurePass123!",
  "address": "123 Admin St, City",
  "role": "ADMIN"
}
```

> **⚠️ Important:** The `role` field is crucial when creating admin users. Without it, the user will be created as a regular user by default.

#### 3. Register a New Regular User

**POST** `https://web-production-34587.up.railway.app/api/v1/auth/users/`

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "email": "john@example.com",
  "password": "MySecure123!",
  "address": "123 Main St, City"
}
```

#### 4. Create an Order

**POST** `https://web-production-34587.up.railway.app/api/v1/orders/orders-detail/`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
```

**Body:**
```json
{
  "sender_phone": "+1234567890",
  "pickup_address": "123 Pickup St, City",
  "delivery_address": "456 Delivery Ave, City",
  "receiver_name": "Jane Doe",
  "receiver_phone": "+0987654321",
  "package_details": "Small package containing documents"
}
```

#### 5. Get Orders (Admin sees all, Regular users see only their own)

**GET** `https://web-production-34587.up.railway.app/api/v1/orders/orders-detail/`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

#### 6. Make Payment

**POST** `https://web-production-34587.up.railway.app/api/v1/payment/order/{order_id}/`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
```

**Body:**
```json
{}
```

**Response:**
```json
{
  "checkout_url": "https://checkout.stripe.com/pay/cs_test_..."
}
```

#### 7. Update Order Status (Delivery Man)

**PATCH** `https://web-production-34587.up.railway.app/api/v1/orders/delivery/{order_id}/`

**Headers:**
```
Authorization: Bearer DELIVERY_MAN_ACCESS_TOKEN
Content-Type: application/json
```

**Body:**
```json
{
  "status": "DELIVERED"
}
```

### Using cURL

#### Admin Login Example
```bash
curl -X POST https://web-production-34587.up.railway.app/api/v1/auth/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@gmail.com", "password": "admin123456@"}'
```

#### Create Admin User Example
```bash
curl -X POST https://web-production-34587.up.railway.app/api/v1/auth/admin-users/ \
  -H "Authorization: Bearer YOUR_ADMIN_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newadmin@example.com",
    "password": "SecurePass123!",
    "address": "123 Admin St",
    "role": "ADMIN"
  }'
```

#### Create Order Example
```bash
curl -X POST https://web-production-34587.up.railway.app/api/v1/orders/orders-detail/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "sender_phone": "+1234567890",
    "pickup_address": "123 Pickup St",
    "delivery_address": "456 Delivery Ave",
    "receiver_name": "Jane Doe",
    "receiver_phone": "+0987654321",
    "package_details": "Documents"
  }'
```

## 💳 Payment Integration

The system integrates with Stripe for secure payment processing:

1. **Payment Flow:**
   - User creates an order
   - Order status: `PENDING`, Payment status: `UNPAID`
   - User initiates payment via `/api/v1/payment/order/{order_id}/`
   - System creates Stripe checkout session
   - User redirected to Stripe payment page
   - Upon successful payment: Order status → `CONFIRMED`, Payment status → `PAID`
   - Upon cancellation: Order status → `PENDING`, Payment status → `UNPAID`

2. **Stripe Configuration:**
   - Test mode is enabled
   - Webhook endpoints handle payment success/failure
   - All amounts are processed in USD

## 📊 Order Status Flow

```
PENDING → CONFIRMED → DELIVERED
   ↓
CANCELLED (can be cancelled at any time)
```

## 🔒 Security Features

- JWT token authentication
- Role-based access control
- Password validation (length, complexity)
- Secure payment processing via Stripe
- Environment-based configuration
- CORS protection
- Admin-only routes for sensitive operations

## 🚀 Deployment

The application is deployed on Railway with the following configuration:

- **Runtime**: Python 3.11.9
- **Database**: PostgreSQL
- **Static Files**: Collected automatically
- **Process**: Gunicorn WSGI server

### Deploy Commands
```bash
# Railway automatically runs these commands
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn courier_backend.wsgi:application --bind 0.0.0.0:$PORT
```

## 🐛 Error Handling

The API returns appropriate HTTP status codes:

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

### Common Error Responses

```json
{
  "detail": "Authentication credentials were not provided."
}
```

```json
{
  "detail": "You do not have permission to perform this action."
}
```

```json
{
  "email": ["This field is required."],
  "password": ["Password length must be greater than 5"]
}
```

## 📞 Support

For issues or questions:
1. Check the error responses for debugging information
2. Verify authentication tokens are valid
3. Ensure correct permissions for the endpoint
4. Review the request format and required fields





---

**Note**: This is a production-ready API with proper security measures. Always use HTTPS in production and keep your environment variables secure. Remember to change default admin credentials in production environments.