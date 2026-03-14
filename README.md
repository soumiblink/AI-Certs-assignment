# Modular Entity Mapping

A production-quality Django REST Framework project for managing vendors, products, courses, certifications, and their hierarchical mappings.

## Tech Stack

- Python 3.11+
- Django
- Django REST Framework
- drf-yasg (Swagger + ReDoc)

## Project Structure

```
modular_entity_mapping/   # Django project config
core/                     # Shared base model, utils, dashboard, seed command
vendor/                   # Vendor master app
product/                  # Product master app
course/                   # Course master app
certification/            # Certification master app
vendor_product_mapping/   # Vendor ↔ Product mapping app
product_course_mapping/   # Product ↔ Course mapping app
course_certification_mapping/  # Course ↔ Certification mapping app
```

## Setup

### 1. Create and activate a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run migrations

```bash
python manage.py migrate
```

### 4. Seed sample data

```bash
python manage.py seed_data
```

### 5. Create a superuser (optional, for admin panel)

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

## API Documentation

- Swagger UI: http://127.0.0.1:8000/swagger/
- ReDoc:       http://127.0.0.1:8000/redoc/
- Admin Panel: http://127.0.0.1:8000/admin/

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/vendors/` | List / Create vendors |
| GET/PUT/PATCH/DELETE | `/api/vendors/{id}/` | Vendor detail |
| GET | `/api/vendors/{id}/full-structure/` | Full nested structure |
| GET/POST | `/api/products/` | List / Create products |
| GET/PUT/PATCH/DELETE | `/api/products/{id}/` | Product detail |
| GET/POST | `/api/courses/` | List / Create courses |
| GET/PUT/PATCH/DELETE | `/api/courses/{id}/` | Course detail |
| GET/POST | `/api/certifications/` | List / Create certifications |
| GET/PUT/PATCH/DELETE | `/api/certifications/{id}/` | Certification detail |
| GET/POST | `/api/vendor-product-mappings/` | List / Create vendor-product mappings |
| GET/PUT/PATCH/DELETE | `/api/vendor-product-mappings/{id}/` | Mapping detail |
| GET/POST | `/api/product-course-mappings/` | List / Create product-course mappings |
| GET/PUT/PATCH/DELETE | `/api/product-course-mappings/{id}/` | Mapping detail |
| GET/POST | `/api/course-certification-mappings/` | List / Create course-certification mappings |
| GET/PUT/PATCH/DELETE | `/api/course-certification-mappings/{id}/` | Mapping detail |
| GET | `/api/dashboard/stats/` | Aggregate entity counts |

## Query Parameter Filtering

```
GET /api/products/?vendor_id=1
GET /api/courses/?product_id=2
GET /api/certifications/?course_id=3
GET /api/vendor-product-mappings/?vendor_id=1
GET /api/product-course-mappings/?product_id=2
GET /api/course-certification-mappings/?course_id=3
```

## Example Requests

### Create a Vendor
```bash
curl -X POST http://127.0.0.1:8000/api/vendors/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Microsoft", "code": "MSFT", "description": "Microsoft Corporation"}'
```

### Get Full Vendor Structure
```bash
curl http://127.0.0.1:8000/api/vendors/1/full-structure/
```

### Dashboard Stats
```bash
curl http://127.0.0.1:8000/api/dashboard/stats/
```

## Response Format

All responses follow a consistent format:

**Success:**
```json
{"success": true, "data": {...}}
```

**Error:**
```json
{"success": false, "message": "..."}
```
