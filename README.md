# Twitter Motivational Quote Bot

A Python bot that automatically posts motivational quotes to Twitter (X) using Playwright and OpenAI's GPT model.

## Features
- Automatically composes and posts motivational tweets
- Human-like typing simulation
- Runs for 12 hours, posting every 30 minutes
- Error handling with automatic retries
- Uses OpenAI's GPT model for quote generation

## Requirements
- Python 3.8+
- Chrome browser
- Twitter (X) account

## Installation
1. Clone this repository
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Set up your environment variables:
```
cp .env.example .env
```
4. Install Playwright and set up your environment variables:
```
playwright install
```
add env
```
GEMINI_API_KEY=your_api_key_here
```
5. Run the bot:
```
python main.py
```