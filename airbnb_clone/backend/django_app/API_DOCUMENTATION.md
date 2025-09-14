# Airbnb Clone Backend API Documentation

This document describes the main REST API endpoints for the backend, including example requests and responses for each resource.

---

## Authentication

### Register
- **POST** `/api/auth/register/`
- **Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "yourpassword",
  "password2": "yourpassword",
  "role": "guest" // or "host"
}
```
- **Response:**
```json
{
  "user": {
    "username": "johndoe",
    "email": "john@example.com",
    "role": "guest"
  },
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

### Login
- **POST** `/api/auth/login/`
- **Body:**
```json
{
  "username": "johndoe",
  "password": "yourpassword"
}
```
- **Response:**
```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

### User Profile
- **GET/PUT/PATCH** `/api/auth/profile/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body (PUT/PATCH):**
```json
{
  "first_name": "John",
  "last_name": "Doe"
}
```
- **Response:**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "role": "guest",
  "first_name": "John",
  "last_name": "Doe"
}
```

---

## Listings

### List/Create Listings
- **GET/POST** `/api/listings/`
- **Headers (POST):** `Authorization: Bearer <access_token>`
- **Body (POST):**
```json
{
  "title": "Cozy Apartment",
  "description": "A nice place to stay.",
  "address": "123 Main St",
  "city": "Cairo",
  "country": "Egypt",
  "price": "100.00",
  "amenities": "WiFi,AC",
  "photo": "<image file>"
}
```
- **Response (GET):**
```json
[
  {
    "id": 1,
    "owner": "hostuser",
    "title": "Cozy Apartment",
    "description": "A nice place to stay.",
    "address": "123 Main St",
    "city": "Cairo",
    "country": "Egypt",
    "price": "100.00",
    "amenities": "WiFi,AC",
    "photo": "/media/listing_photos/abc.jpg",
    "created_at": "2025-09-14T12:00:00Z",
    "updated_at": "2025-09-14T12:00:00Z"
  }
]
```

### Retrieve/Update/Delete Listing
- **GET/PUT/PATCH/DELETE** `/api/listings/<id>/`
- **Headers (PUT/PATCH/DELETE):** `Authorization: Bearer <access_token>`
- **Body (PUT/PATCH):** (same as create)

---

## Bookings

### List/Create Bookings
- **GET/POST** `/api/bookings/`
- **Headers (POST):** `Authorization: Bearer <access_token>`
- **Body (POST):**
```json
{
  "listing_id": 1,
  "start_date": "2025-10-01",
  "end_date": "2025-10-05"
}
```
- **Response (GET):**
```json
[
  {
    "id": 1,
    "listing": "Cozy Apartment",
    "guest": "johndoe",
    "start_date": "2025-10-01",
    "end_date": "2025-10-05",
    "status": "pending",
    "created_at": "2025-09-14T12:00:00Z",
    "updated_at": "2025-09-14T12:00:00Z"
  }
]
```

### Retrieve/Update/Delete Booking
- **GET/PUT/PATCH/DELETE** `/api/bookings/<id>/`
- **Headers (PUT/PATCH/DELETE):** `Authorization: Bearer <access_token>`
- **Body (PUT/PATCH):**
```json
{
  "start_date": "2025-10-02",
  "end_date": "2025-10-06"
}
```

---

## Reviews

### List/Create Reviews
- **GET/POST** `/api/reviews/`
- **Headers (POST):** `Authorization: Bearer <access_token>`
- **Body (POST):**
```json
{
  "listing_id": 1,
  "rating": 5,
  "comment": "Great place!"
}
```
- **Response (GET):**
```json
[
  {
    "id": 1,
    "listing": "Cozy Apartment",
    "guest": "johndoe",
    "rating": 5,
    "comment": "Great place!",
    "created_at": "2025-09-14T12:00:00Z"
  }
]
```

### Retrieve/Update/Delete Review
- **GET/PUT/PATCH/DELETE** `/api/reviews/<id>/`
- **Headers (PUT/PATCH/DELETE):** `Authorization: Bearer <access_token>`
- **Body (PUT/PATCH):**
```json
{
  "rating": 4,
  "comment": "Nice, but could be cleaner."
}
```

---

## Notes
- All endpoints that modify data require authentication via JWT (use the `Authorization: Bearer <access_token>` header).
- For file uploads (listing photo), use `multipart/form-data`.
- Pagination, search, and ordering are available on list endpoints (see DRF docs for query params).
- Status codes: 200 OK, 201 Created, 204 No Content, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found.

---

For more details, see the codebase or contact the backend team.

