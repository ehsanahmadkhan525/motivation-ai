import asyncio
from playwright.async_api import async_playwright
import time
from dotenv import load_dotenv
import os
load_dotenv()
from langchain_openai import AzureChatOpenAI, ChatOpenAI


async def main():
    playwright = await async_playwright().start()
    
    # Connect to existing Chrome instance on debug port
    browser = await playwright.chromium.connect_over_cdp(
        endpoint_url='http://localhost:9222'
    )
    
    # Get the default browser context and its pages
    context = browser.contexts[0]
    pages = context.pages
    page = pages[0]
    
    # Navigate to X's compose tweet page with delay after loading
    await page.goto('https://x.com/compose/post')
    await asyncio.sleep(2)  # Wait for page to fully stabilize
    
    # Wait for the editor to be ready
    await page.wait_for_selector('[data-testid="tweetTextarea_0"]')
    await asyncio.sleep(1)  # Short pause before typing
    
    llm = ChatOpenAI( temperature=0.8, api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/", model="gemini-1.5-flash")

    # Fill the motivation quote with human-like typing speed
    # motivation_quote = "Success doesn't come from what you do occasionally, it comes from what you do consistently. Stay focused, work hard, and believe in the power of perseverance."
    motivation_quote = llm.invoke("write a motivational tweet")
    motivation_quote = motivation_quote.content
    await page.type('[data-testid="tweetTextarea_0"]', motivation_quote, delay=100)  # 100ms between keystrokes
    
    await asyncio.sleep(1)  # Pause before clicking post
    
    # Click the post button
    await page.click('[data-testid="tweetButton"]')
    
    # Wait a moment to ensure the tweet is posted
    await asyncio.sleep(15)
    
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
