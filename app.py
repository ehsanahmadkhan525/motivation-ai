# """
# Find and apply to jobs.

# @dev You need to add OPENAI_API_KEY to your environment variables.

# Also you have to install PyPDF2 to read pdf files: pip install PyPDF2
# """

# import csv
# import os
# import re
# import sys
# from pathlib import Path

# from PyPDF2 import PdfReader

# from browser_use.browser.browser import Browser, BrowserConfig

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import asyncio
# from typing import List, Optional



# from dotenv import load_dotenv
# from langchain_openai import AzureChatOpenAI, ChatOpenAI
# from langchain_anthropic import ChatAnthropic
# from pydantic import BaseModel, SecretStr, Field

# from browser_use import ActionResult, Agent, Controller
# from browser_use.browser.context import BrowserContext

# import markdown
# from fpdf import FPDF, XPos, YPos


# load_dotenv()
# import logging

# logger = logging.getLogger(__name__)
# # full screen mode
# controller = Controller()
# CV = Path.cwd() / 'cv.pdf'


# class Job(BaseModel):
# 	title: str
# 	link: str
# 	company: str
# 	fit_score: float
# 	location: Optional[str] = None
# 	salary: Optional[str] = None

# class JobDescription(BaseModel):
# 	job_description: str = Field(description='The Complete job description from top to bottom in a single string')

# @controller.action(
# 	'Save jobs to file - with a score how well it fits to my profile', param_model=Job
# )
# def save_jobs(job: Job):
# 	with open('jobs.csv', 'a', newline='') as f:
# 		writer = csv.writer(f)
# 		writer.writerow([job.title, job.company, job.link, job.salary, job.location])

# 	return 'Saved job to file'


# @controller.action('Read jobs from file')
# def read_jobs():
# 	with open('jobs.csv', 'r') as f:
# 		return f.read()


# @controller.action('Read my cv for context to fill forms')
# def read_cv():
# 	pdf = PdfReader(CV)
# 	text = ''
# 	for page in pdf.pages:
# 		text += page.extract_text() or ''
# 	logger.info(f'Read cv with {len(text)} characters')
# 	return ActionResult(extracted_content=text, include_in_memory=True)

# # @controller.action('Create custom CV according to the job description and apply to the job')
# # def create_custom_cv(job_description: JobDescription):
# # 	pdf = PdfReader(CV)
# # 	text = ''
# # 	for page in pdf.pages:
# # 		text += page.extract_text() or ''
# # 	custom_cv = ChatOpenAI(model='gpt-4o-2024-11-20', temperature=0).invoke(
# # 		f"You are a professional cv creator. Create a custom cv in markdown format for the following job description: {job_description.job_description} and use the following text for my cv: {text}"
# # 	)
# # 	custom_cv = str(custom_cv.content)

# # 	# Save the Markdown file
# # 	md_file_path = 'custom_cv.md'
# # 	with open(md_file_path, 'w', encoding='utf-8') as md_file:
# # 		md_file.write(custom_cv)

# # 	# Convert markdown to HTML
# # 	html_content = markdown.markdown(custom_cv)
	
# # 	# Create PDF using FPDF
# # 	pdf = FPDF()
# # 	pdf.add_page()
# # 	pdf.set_auto_page_break(auto=True, margin=15)
	
# # 	# Instead of using write_html, let's write text directly
# # 	pdf.set_font('Courier', size=12)
	
# # 	# Split content into lines and write line by line
# # 	lines = html_content.split('\n')
# # 	for line in lines:
# # 		# Remove HTML tags (simple approach)
# # 		clean_line = re.sub('<[^<]+?>', '', line)
# # 		# Replace problematic characters
# # 		clean_line = clean_line.replace('"', '"').replace('"', '"').replace(''', "'").replace(''', "'")
# # 		try:
# # 			pdf.cell(0, 10, text=clean_line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
# # 		except Exception as e:
# # 			# If there's an error with specific characters, try to encode/decode
# # 				clean_line = clean_line.encode('ascii', 'replace').decode('ascii')
# # 				pdf.cell(0, 10, text=clean_line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
	
# # 	# Save the PDF
# # 	pdf_file_path = 'custom_cv.pdf'
# # 	pdf.output(pdf_file_path)

# # 	Result = f"PDF CV saved at: {pdf_file_path} , call upload_cv to upload the cv"

# # 	return ActionResult(extracted_content=Result, include_in_memory=True)



# @controller.action(
# 	'Upload cv to element - call this function to upload if element is not found, try with different index of the same upload element',
# 	requires_browser=True,
# )
# async def upload_cv(index: int, browser: BrowserContext):
# 	path = str(CV.absolute())
# 	dom_el = await browser.get_dom_element_by_index(index)

# 	if dom_el is None:
# 		return ActionResult(error=f'No element found at index {index}')

# 	file_upload_dom_el = dom_el.get_file_upload_element()

# 	if file_upload_dom_el is None:
# 		logger.info(f'No file upload element found at index {index}')
# 		return ActionResult(error=f'No file upload element found at index {index}')

# 	file_upload_el = await browser.get_locate_element(file_upload_dom_el)

# 	if file_upload_el is None:
# 		logger.info(f'No file upload element found at index {index}')
# 		return ActionResult(error=f'No file upload element found at index {index}')

# 	try:
# 		await file_upload_el.set_input_files(path)
# 		msg = f'Successfully uploaded file to index {index}'
# 		logger.info(msg)
# 		return ActionResult(extracted_content=msg)
# 	except Exception as e:
# 		logger.debug(f'Error in set_input_files: {str(e)}')
# 		return ActionResult(error=f'Failed to upload file to index {index}')


# browser = Browser(
# 	config=BrowserConfig(
# 		chrome_instance_path='C:/Program Files/Google/Chrome/Application/chrome.exe',
# 		disable_security=True,
# 	)
# )


# async def main():
# 	# ground_task = (
# 	# 	'You are a professional job finder. '
# 	# 	'1. Read my cv with read_cv'
# 	# 	'2. Read the saved jobs file '
# 	# 	'3. start applying to the first link of Amazon '
# 	# 	'You can navigate through pages e.g. by scrolling '
# 	# 	'Make sure to be on the english version of the page'
# 	# )
# 	ground_task = (
# 		'You are a professional job finder. '
# 		'find ml internships in and apply to them'
# 		'1. When you find a job, read the job description by reading the entire page from top to bottom \n' 
# 		'2. Read my cv with read_cv'
# 		'3. Upload cv to the job application form using upload_cv'
# 		'search at company:'
# 	)
# 	tasks = [
# 		ground_task + '\n' + 'Google',
# 		# ground_task + '\n' + 'Amazon',
# 		# ground_task + '\n' + 'Apple',
# 		# ground_task + '\n' + 'Microsoft',
# 		# ground_task
# 		# + '\n'
# 		# + 'go to https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/job/Taiwan%2C-Remote/Fulfillment-Analyst---New-College-Graduate-2025_JR1988949/apply/autofillWithResume?workerSubType=0c40f6bd1d8f10adf6dae42e46d44a17&workerSubType=ab40a98049581037a3ada55b087049b7 NVIDIA',
# 		# ground_task + '\n' + 'Meta',
# 	]
# 	model = ChatOpenAI(model='gpt-4o-2024-11-20', temperature=0)

# 	agents = []
# 	for task in tasks:
# 		agent = Agent(task=task, llm=model, controller=controller)
# 		agents.append(agent)

# 	await asyncio.gather(*[agent.run() for agent in agents])


# if __name__ == '__main__':
# 	asyncio.run(main())

from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
import os
load_dotenv()
import csv
import os
import re
import sys
from pathlib import Path

from PyPDF2 import PdfReader

from browser_use.browser.browser import Browser, BrowserConfig

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio
from typing import List, Optional

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from pydantic import BaseModel, SecretStr

from browser_use import ActionResult, Agent, Controller
from browser_use.browser.context import BrowserContext

browser = Browser(
	config=BrowserConfig(
		chrome_instance_path='/usr/bin/google-chrome',
		disable_security=True,
	)
)

async def main():
    agent = Agent(
        task="Go to https://x.com/compose/post, post a motivational tweet",
        llm=ChatOpenAI(model='gpt-4o-mini'),
        browser=browser,
        # llm=ChatOpenAI(api_key=os.getenv("GEMINI_API_KEY"), base_url="https://generativelanguage.googleapis.com/v1beta/openai/"),
    )
    result = await agent.run()
    print(result)

asyncio.run(main())