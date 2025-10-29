================================================================
MYSQL DATABASE CONNECTION INSTRUCTIONS
================================================================

To connect your MySQL database from Render/MySQL Workbench:

RECOMMENDED: Use environment variable (Best Practice)
================================================================

1. Go to Replit Secrets tab (or .env file for local deployment)

2. Add: DATABASE_URL = your_mysql_connection_string

   Format: mysql+pymysql://username:password@host:port/database_name
   
   Example: mysql+pymysql://root:mypassword@mysql.render.com:3306/waste_db

3. Install MySQL connector:
   Run: uv add pymysql
   Or: pip install pymysql

4. Restart the application

The app will automatically use the DATABASE_URL environment variable.
If not set, it defaults to SQLite (sqlite:///waste_management.db)

================================================================
ALTERNATIVE: Direct code edit (Not recommended)
================================================================

You can also edit app.py directly:
- Find line: DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///waste_management.db')
- Replace with: DATABASE_URL = 'mysql+pymysql://username:password@host:port/database_name'

================================================================
ESP32 INTEGRATION
================================================================

Your ESP32 module can connect to the same MySQL database using:
- Host: your_mysql_host
- Port: 3306
- Database: waste_db
- User: your_username
- Password: your_password

Use MySQL client library for ESP32 (e.g., MySQL_MariaDB_Generic)

================================================================
