from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import os

app = Flask(__name__)
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
app.template_folder = template_dir

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
    except Exception as e:
        print(f"Error getting page info: {str(e)}")
        return url, ''

def parse_sitemap(sitemap_url):
    try:
        response = requests.get(sitemap_url)
        root = ET.fromstring(response.content)
        urls = []
        for url in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
            urls.append(url.text)
        return urls
    except Exception as e:
        print(f"Error parsing sitemap: {str(e)}")
        return []

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
    
    return output

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        data = request.form
        title = data.get('title', '')
        description = data.get('description', '')
        input_type = data.get('input_type', 'urls')
        content = data.get('content', '').strip()
        
        urls = []
        if input_type == 'sitemap':
            urls = parse_sitemap(content)
        else:
            urls = [url.strip() for url in content.split('\n') if url.strip()]
        
        sections = {"Main": []}
        
        for url in urls:
            page_title, page_description = get_page_info(url)
            sections["Main"].append({
                'url': url,
                'title': page_title,
                'details': page_description
            })
        
        result = format_llms_txt(title, description, sections)
        return jsonify({'result': result})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 