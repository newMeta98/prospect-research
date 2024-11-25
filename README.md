 # Prospect Company Research

## Overview
A web application designed to help sales teams gather and summarize information about prospective companies by inputting the company's URL.

## Features

- **Web Scraping**: Extracts information from the specified company URL. For more in-depth extraction, change the system message in `scraping/scraper.py` to return more than 2 useful page links. This will probably prolong the research time but give better results.
- **Text Summarization**: Summarizes the scraped content using AI.
- **User Authentication**: Secure login to access the tool.
- **Caching**: Stores summaries for faster access.
- **Responsive Design**: Optimized for various devices.

## Prerequisites

- Python 3.8 or higher
- Flask and related libraries
- DeepSeek API key for summarization
- A web browser

## Installation

### Clone the repository:

```bash
git clone https://github.com/newMeta98/prospect-research.git
cd prospect-research
```

### Install dependencies:
```bash
pip install -r requirements.txt
```
### Set DeepSeek API KEY:
```bash
In scraping/scraper.py and processing/summarizer.py
OR set environment variables
```
### Run the application:
```bash
python app.py
```

### Usage

Access the application:
Open a web browser and navigate to http://localhost:5000.
Login: Use the credentials username: admin and password: password to log in.
Once logged in, you'll be redirected to the home page.
Generate Summary:
Enter the URL of the company's website in the provided field.
Click the "Generate Article" button.
Wait for the summary to be generated and displayed.
Dependencies
Flask
Flask-Caching
Flask-Login
validators
requests
beautifulsoup4
openai
Contributing
Contributions are welcome! Please open an issue or submit a pull request.

License
This project is licensed under the MIT License - see the LICENSE.md file for details.

Architecture
The application is built using Flask, a micro web framework in Python. It includes modules for web scraping, text summarization, user authentication, and caching. The front-end is designed using HTML and CSS for a responsive user interface.

The authentication system is basic and intended for demonstration purposes.
Summaries are cached for 1 hour (3600 seconds).
FAQ
Q: How do I obtain a DeepSeek API key?

A: Visit the DeepSeek website to sign up for an API key.

Q: Can I deploy this application to a production environment?

A: Yes, consider using platforms like Heroku or AWS for deployment.
