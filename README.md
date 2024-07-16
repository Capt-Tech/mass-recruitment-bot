# CAPT Mass Recruitment Bot

Bot to manage recruitment links and mass distribution of results in CAPT mass recruitment

## Setup

### Requirements

- Python 3.12
- Docker (Only for deployment)

### Telegram Bot Setup (Local)

1. Create your own Telegram bot by following [BotFather](https://t.me/BotFather) instructions
2. Copy the `API_KEY` (keep this key secret)

### Running the Bot

1. Copy this repository

```
git clone https://github.com/Capt-Tech/mass-recruitment-bot
```

2. Create a `.env` file in root folder with the following content and update Telegram bot API key, admin username and developers

```
TELEGRAM_BOT_API_KEY=<YOUR_API_KEY>
ADMIN_USERNAME = <your telegram handle separated with ;>
DEVELOPERS = <your telegram handle separated with ;>
```

3. Install Packages

```
pip install -r requirements.txt
```

4. Create a data folder in teh root folder and a tmp_interview.csv file

5. Run Bot

```
python src/main.py
```

### Testing Deployment Configurations

Ensure you have docker installed

```
docker compose build
docker compose up -d
```
