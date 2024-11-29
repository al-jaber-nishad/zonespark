# E-commerce Online Platform  

## Overview  
This project is a backend implementation for an e-commerce online platform. It includes user authentication, product management, stock management, and category management APIs. The application is designed to handle high traffic efficiently and follows good coding practices.  

---

## Features  
- **User Authentication and Registration API**  
  - User login and registration system.  
  - JWT-based authentication for secure access.  

- **E-commerce API**  
  - Models for **Product**, **Stock**, and **Category**.  
  - CRUD operations for managing products, stock, and categories.  

- **Database Integration**  
  - PostgreSQL database connected with pgAdmin4 for management.  

- **Bonus Features**  
  - Dockerized application for easy deployment.  
  - Hosted on a live server for demonstration.  

---

## Technology Stack  
- **Backend Framework:** Django REST Framework  
- **Database:** PostgreSQL  
- **Authentication:** JWT  
- **Containerization:** Docker  

---

## Installation  

### Prerequisites  
- Python (3.10 or later)  
- Docker and Docker Compose  
- PostgreSQL and pgAdmin4  
- Git  

### Steps  

1. **Clone the repository:**  
   ```bash  
   git clone https://github.com/al-jaber-nishad/zonespark.git
   cd zonespark
   ```
2. **Create and activate a virtual environment:**

```bash
python -m venv venv  
source venv/bin/activate  # For Linux/macOS  
venv\Scripts\activate     # For Windows  
```
3. **Install dependencies:**

```bash
pip install -r requirements.txt  
```

4. **Create .env file**
```bash
DB_NAME=your_database_name  
DB_USER=your_database_user  
DB_PASS=your_database_password  
DB_HOST=your_database_host  
```

5. **Apply database migrations:**

```bash
python manage.py makemigrations  
python manage.py migrate  
```

6. **Create a superuser:**

```bash
python manage.py createsuperuser  
```

7. **Run the development server:**

```bash
python manage.py runserver  
```


## Docker Deployment

1. **Build and run the Docker containers:**

```bash
docker build -t zonespark . 
docker run -p 8000:8000 zonespark
```

2. **Access the application:**

Admin Panel: http://localhost:8000/admin/ \
API Endpoints: http://localhost:8000/schema/swagger-ui/


### Notes
The project includes thorough comments for better readability.
Implements scalable patterns for handling large datasets and requests.

### Contact
Developer: Al Jaber Nishad \
Email: mailnishad02@gmail.com