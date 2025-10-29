# Waste Management System

## Overview
A comprehensive Flask-based waste management web application connecting four stakeholder roles: Users, Collectors, Recyclers, and Government officials. The system enables bin monitoring, waste selling/buying marketplace, complaint management, and analytics integration.

## Project Architecture

### Technology Stack
- **Backend**: Flask (Python)
- **Database**: SQLite (development), MySQL via SQLAlchemy (production)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Authentication**: Flask-Login with role-based access control
- **File Handling**: Pillow for image processing

### Database Models
- **User**: Authentication and profile management for all roles
- **Bin**: Smart bin monitoring with fill levels and status tracking
- **Complaint**: Issue reporting and management system
- **WasteSale**: Marketplace for waste buying and selling transactions

## Role-Based Features

### User Role
- **Dashboard**: QR code scanner simulation to check bin status (fill level, last cleaned, compartment weights)
- **Complaint System**: Submit complaints about bins or waste collection
- **Sell Waste**: List waste for sale with images, view nearby recyclers

### Collector Role
- **Dashboard**: Monitor all bins in assigned location with status indicators (Urgent/Medium/Enough Space)
- **Complaints**: View and manage user-submitted complaints
- **Sell**: List collected waste for sale
- **Analytics**: Placeholder page for Power BI integration

### Recycler Role
- **Buy Marketplace**: Browse available waste listings filtered by location
- **Complaint**: Submit and track complaints
- **Sell**: List recycled materials for sale

### Government Role
- **Dashboard**: Multi-location bin monitoring with comprehensive status overview
- **Complaint Details**: View all regional complaints
- **Transaction History**: Track all buy/sell activities
- **Analytics**: Placeholder for Power BI dashboard embedding

## Setup Instructions

### 1. Installation
Dependencies are already installed. The project uses:
- Flask
- SQLAlchemy
- Flask-Login
- Werkzeug (password hashing)
- Pillow (image handling)

### 2. Database Configuration

**Current Setup**: SQLite (waste_management.db)

**To Connect MySQL** (see DATABASE_CONFIG_README.txt for details):
1. Set `DATABASE_URL` environment variable with your MySQL connection string
2. Install pymysql: `uv add pymysql`
3. Restart the application

Format: `mysql+pymysql://username:password@host:port/database_name`

### 3. Demo Data
Run `python init_db.py` to create demo accounts:
- User: demo_user / password123
- Collector: demo_collector / password123
- Recycler: demo_recycler / password123
- Government: demo_gov / password123

Demo bins: BIN001, BIN002, BIN003

## ESP32 Integration
The application is designed to work with ESP32 modules for real-time bin monitoring. ESP32 devices can connect directly to the MySQL database to:
- Update bin fill levels (recyclable/non-recyclable weights)
- Set last cleaned timestamps
- Trigger status updates (Urgent/Medium/Enough Space)

Configure ESP32 with the same MySQL connection credentials used by the application.

## Power BI Analytics
Placeholder pages are ready in Collector and Government dashboards for Power BI dashboard embedding. Connect Power BI to the MySQL database to visualize:
- Bin status trends
- Waste collection efficiency
- Regional comparisons
- Transaction analytics

## Security Features
- Password hashing with Werkzeug
- Flask-Login session management
- Role-based access control (@role_required decorator)
- Secure file upload validation (16MB limit, image types only)
- CSRF protection via Flask secret key

## File Structure
```
.
├── app.py                  # Main Flask application
├── init_db.py             # Database initialization script
├── config.py              # Configuration file
├── templates/             # Jinja2 templates
│   ├── base.html
│   ├── login.html
│   ├── signup.html
│   ├── user/
│   ├── collector/
│   ├── recycler/
│   └── government/
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
└── uploads/               # User-uploaded waste images

```

## Recent Changes
- 2025-10-29: Initial implementation with all 4 role-based interfaces
- 2025-10-29: Fixed database schema creation to work with fresh MySQL databases
- 2025-10-29: Updated database configuration to support environment variable override

## Next Steps
1. Connect to production MySQL database from Render/MySQL Workbench
2. Integrate ESP32 modules for real-time bin monitoring
3. Embed Power BI dashboards in analytics pages
4. Add real-time notification system for urgent bin status
5. Implement admin panel for bin assignment and user management
