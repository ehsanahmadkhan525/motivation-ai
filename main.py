import asyncio
from playwright.async_api import async_playwright
import time
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from dotenv import load_dotenv
import logging
from random import choice
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tweet_bot.log'),
        logging.StreamHandler()
    ]
)

load_dotenv()

async def main():
    logging.info("Starting tweet bot")
    playwright = await async_playwright().start()
    
    # Connect to existing Chrome instance on debug port
    browser = await playwright.chromium.connect_over_cdp(
        endpoint_url='http://localhost:9222'
    )
    
    # Get the default browser context and its pages
    context = browser.contexts[0]
    pages = context.pages
    page = pages[0]
    
    llm = ChatOpenAI(temperature=0.8, api_key=os.getenv("GEMINI_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/", model="gemini-1.5-flash")

    start_time = datetime.now()
    end_time = start_time + timedelta(hours=12)
    logging.info(f"Bot will run until {end_time}")
    
    while datetime.now() < end_time:
        try:
            logging.info("Navigating to compose tweet page")
            # Navigate to X's compose tweet page with delay after loading
            await page.goto('https://x.com/compose/post')
            await asyncio.sleep(2)  # Wait for page to fully stabilize
            
            # Wait for the editor to be ready
            await page.wait_for_selector('[data-testid="tweetTextarea_0"]')
            await asyncio.sleep(1)  # Short pause before typing


            topics = [
                "success", "failure", "resilience", "self-belief", "persistence",
                "dreams", "hard work", "opportunity", "learning", "courage"
            ]

            styles = [
                "short and punchy", "poetic", "inspirational", "reflective",
                "powerful", "uplifting", "lighthearted", "empathetic"
            ]

            motivation_prompt = f"Write a {choice(styles)} motivational quote about {choice(topics)}."

            motivation_quote = llm.invoke(motivation_prompt)
            # Fill the motivation quote with human-like typing speed
            # motivation_quote = "Success doesn't come from what you do occasionally, it comes from what you do consistently. Stay focused, work hard, and believe in the power of perseverance."

            motivation_quote = motivation_quote.content
            await page.type('[data-testid="tweetTextarea_0"]', motivation_quote, delay=100)  # 100ms between keystrokes
            
            await asyncio.sleep(1)  # Pause before clicking post
            
            # Click the post button
            await page.click('[data-testid="tweetButton"]')
            
            # Wait a moment to ensure the tweet is posted
            await asyncio.sleep(15)
            
            logging.info(f"Tweet posted successfully at {datetime.now()}")
            
            logging.info("Waiting 30 minutes for next tweet")
            await asyncio.sleep(30 * 60)
            
        except Exception as e:
            logging.error(f"Error occurred: {str(e)}")
            logging.info("Waiting 5 minutes before retrying")
            await asyncio.sleep(5 * 60)
    
    logging.info("12-hour period complete. Cleaning up resources")
    # Clean up
    await browser.close()
    await playwright.stop()

if __name__ == "__main__":
    # First, make sure Chrome is running with remote debugging enabled
    import subprocess
    subprocess.Popen([
        '/usr/bin/google-chrome',
        '--remote-debugging-port=9222'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Give Chrome a moment to start (wait 3 seconds)
    time.sleep(3)
    
    # Now run the main async function
    asyncio.run(main())
