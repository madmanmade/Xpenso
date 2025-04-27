# Xpenso - Enhanced Expense Tracker

Xpenso is a comprehensive expense tracking application built with Django that helps users manage their finances effectively. It includes features like expense tracking, income management, budget planning, and advanced analytics.

## Features

- Expense tracking with categories and payment methods
- Income management
- Budget planning and alerts
- Advanced analytics and reports
- Machine learning-based expense predictions
- Real-time updates using WebSocket
- REST API for mobile integration
- Export data in multiple formats (CSV, PDF, Excel)
- User preferences and customization
- Responsive design for all devices

## Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- Redis (for caching and WebSocket)
- Node.js and npm (for frontend assets)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Xpenso.git
cd Xpenso
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```bash
# Django settings
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database settings
DB_NAME=xpenso_db
DB_USER=xpenso_user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

# Redis settings
REDIS_HOST=localhost
REDIS_PORT=6379

# Email settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password

# Custom settings
MAX_EXPENSE_AMOUNT=1000000
EXPENSE_CATEGORIES_LIMIT=50
EXPENSE_PAGINATION_SIZE=20
RETRAIN_MODEL_INTERVAL=7
MIN_SAMPLES_FOR_TRAINING=100
REPORT_RETENTION_DAYS=30
BUDGET_ALERT_THRESHOLDS=50,75,90
ENABLE_BUDGET_NOTIFICATIONS=True
```

5. Create the PostgreSQL database:
```sql
CREATE DATABASE xpenso_db;
CREATE USER xpenso_user WITH PASSWORD 'your-db-password';
ALTER ROLE xpenso_user SET client_encoding TO 'utf8';
ALTER ROLE xpenso_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE xpenso_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE xpenso_db TO xpenso_user;
```

6. Apply database migrations:
```bash
python manage.py migrate
```

7. Create a superuser:
```bash
python manage.py createsuperuser
```

8. Start the development server:
```bash
python manage.py runserver
```

## Running in Production

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Configure proper `ALLOWED_HOSTS`
3. Use a production-grade server like Gunicorn
4. Set up Nginx as a reverse proxy
5. Enable SSL/TLS
6. Configure proper email settings
7. Set up proper database backup

Example production deployment:

```bash
# Install Gunicorn
pip install gunicorn

# Start Gunicorn
gunicorn expensetracker_enhanced.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
```

## API Documentation

The REST API documentation is available at `/api/docs/` when running the server.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Django Framework
- Django REST Framework
- Chart.js for visualizations
- Bootstrap for UI
- Font Awesome for icons 