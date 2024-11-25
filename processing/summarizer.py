from openai import OpenAI
import requests

def summarize_text(text):
    print(text)
    text = str(text)
    api_key = 'YOUR_API_KEY'  # Replace with your actual API key
    base_url = 'https://api.deepseek.com'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'deepseek-chat',
        'messages': [
            {'role': 'system', 'content': 'You are a helpful assistant that produce a concise, informative article about this prospect for the sales team as output. Lets think through this step-by-step: Company Overview: Name and Location: Basic information about the company. Industry: The sector or market the company operates in. Company Size: Number of employees, revenue, and market share. Key Personnel: Decision Makers: Identify the key decision-makers such as CEOs, CFOs, and other executives. Contact Information: Email addresses, phone numbers, and LinkedIn profiles of key personnel. Products and Services: Offerings: Detailed information about the products or services the company provides. Unique Selling Points: What sets their offerings apart from competitors. Financial Health: Revenue and Profit: Financial performance and trends. Funding and Investments: Information on venture capital, investments, and financial backing. Market Position: Competitors: Identify main competitors and their market position. Market Share: The companys share in its industry. Recent News and Developments: Press Releases: Recent announcements and updates. Industry Trends: How the company is adapting to current industry trends. Customer Base: Target Market: Who their primary customers are. Customer Feedback: Reviews, testimonials, and customer satisfaction ratings. Technology and Innovation: Tech Stack: Technologies and tools the company uses. Innovations: Recent innovations or technological advancements. Company Culture and Values: Mission and Vision: The companys goals and values. Corporate Social Responsibility: Initiatives related to sustainability and social impact. Pain Points and Challenges: Current Issues: Any known challenges or problems the company is facing. Potential Needs: Areas where the company might benefit from your products or services. Sales History: Previous Engagements: Any past interactions or sales history with the company. Purchase Behavior: Patterns in their purchasing decisions. Regulatory and Compliance: Legal Status: Any legal issues or compliance requirements. Certifications: Industry-specific certifications and standards they adhere to.'},
            {'role': 'user', 'content': text}
        ],
        'stream': False
    }
    try:
        response = requests.post(f'{base_url}/chat/completions', headers=headers, json=data)
        response.raise_for_status()
        summary = response.json()['choices'][0]['message']['content']
        return summary
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return f'An HTTP error occurred: {http_err}'
    except Exception as err:
        print(f'An error occurred: {err}')
        return f'An error occurred: {err}'