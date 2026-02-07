# Chakidon_antropic
By using Claude version  
# Telegram Cleaning Service Bot (aiogram 3.x)

Professional bilingual (Russian/Uzbek) Telegram bot for carpet and sofa cleaning services.

## Features

- 🌐 Bilingual interface (Russian/Uzbek)
- 🧺 Multiple service types
- 📦 Multiple item support with custom sizes
- 📍 GPS location and manual address entry
- 💬 Order comments and customer feedback
- ⭐ 5-star rating system
- 📋 Order history tracking
- 👨‍💼 Complete admin panel
- 🗑️ Auto-message deletion for clean UX
- 💾 PostgreSQL database with async SQLAlchemy
- 🔒 Phone number validation (Uzbekistan)

## Requirements

- Python 3.12+
- PostgreSQL 14+
- pip

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/cleaning-bot.git
cd cleaning-bot
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup PostgreSQL Database
```bash
# Create database
createdb cleaning_bot

# Or using psql
psql -U postgres
CREATE DATABASE cleaning_bot;
\q
```

### 5. Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
```

Required variables:
```env
BOT_TOKEN=your_bot_token_here
ADMIN_IDS=123456789,987654321
DB_HOST=localhost
DB_PORT=5432
DB_NAME=cleaning_bot
DB_USER=postgres
DB_PASSWORD=your_password
```

### 6. Run Bot
```bash
python bot.py
```

## Project Structure
```
telegram_cleaning_bot/
├── bot.py                  # Main entry point
├── config.py               # Configuration
├── requirements.txt        # Dependencies
├── .env                    # Environment variables
│
├── database/
│   ├── models.py          # SQLAlchemy models
│   ├── database.py        # DB connection
│   └── repository.py      # Database queries
│
├── handlers/              # All bot handlers
├── keyboards/             # Keyboard builders
├── localization/          # Translations
├── middlewares/           # Custom middlewares
├── services/              # Business logic
└── utils/                 # Utilities
```

## Configuration

### BotFather Setup

1. **Create bot**: `/newbot`
2. **Set description**: `/setdescription`
3. **Set profile pic**: `/setuserpic`
4. **Set commands**: `/setcommands`
```
start - Начать заказ / Buyurtma boshlash
myorders - Мои заказы / Buyurtmalarim
help - Помощь / Yordam
cancel - Отменить / Bekor qilish
```

### Pricing

Edit `config.py`:
```python
CARPET_PRICE_PER_M2=15000
SOFA_PRICE_2_SEAT=50000
```

## Usage

### For Customers

1. `/start` - Start bot
2. Select language
3. Choose service
4. Enter details
5. Confirm order
6. Track with `/myorders`
7. Rate service after completion

### For Admins

1. Receive order notification
2. Accept/reject order
3. Mark as in progress
4. Complete order
5. View customer feedback

## Development

### Adding New Features

1. Create handler in `handlers/`
2. Add router to `bot.py`
3. Update translations in `localization/`
4. Add keyboard in `keyboards/`

### Database Migrations

Use Alembic for migrations:
```bash
alembic init alembic
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Testing
```bash
pytest tests/
```

## Deployment

### Using systemd
```bash
sudo nano /etc/systemd/system/cleaning-bot.service
```
```ini
[Unit]
Description=Cleaning Service Telegram Bot
After=network.target postgresql.service

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/cleaning-bot
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl enable cleaning-bot
sudo systemctl start cleaning-bot
sudo systemctl status cleaning-bot
```

## Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Test connection
psql -h localhost -U postgres -d cleaning_bot
```

### Bot Not Responding
```bash
# Check logs
tail -f bot.log

# Verify token
echo $BOT_TOKEN
```

## License

MIT

## Support

For issues: https://github.com/yourusername/cleaning-bot/issues