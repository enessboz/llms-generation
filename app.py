from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import xml.etree.ElementTree as ET

app = Flask(__name__)

def get_page_info(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.find('h1')
        if title:
            title = title.text.strip()
        else:
            title = soup.find('title')
            title = title.text.strip() if title else url
            
        description = soup.find('meta', {'name': 'description'})
        if description:
            description = description.get('content', '')
        else:
            first_p = soup.find('p')
            description = first_p.text[:200] + '...' if first_p else ''
            
        return title, description
    except:
        return url, ''

def format_llms_txt(title, description, sections):
    output = f"# {title}\n\n"
    
    if description:
        output += f"> {description}\n\n"
    
    if "Main" in sections:
        for link in sections["Main"]:
            if link.get('details'):
                output += f"- [{link['title']}]({link['url']}): {link['details']}\n"
            else:
                output += f"- [{link['title']}]({link['url']})\n"
        output += "\n"
    
    if "Optional" in sections:
        output += "## Optional\n\n"
        for link in sections["Optional"]:
            if link.get('details'):
                output += f"- [{link['title']}]({link['url']}): {link['details']}\n"
            else:
                output += f"- [{link['title']}]({link['url']})\n"
    
    return output

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def generate():
    title = request.form.get('title', '')
    description = request.form.get('description', '')
    input_type = request.form.get('input_type', 'urls')
    content = request.form.get('content', '')
    
    # URL işleme mantığı buraya gelecek
    # ... 
    
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)

