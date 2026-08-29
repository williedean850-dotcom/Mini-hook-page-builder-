from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
from datetime import datetime
import json
import os
from dotenv import load_dotenv
import openai
import uuid

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Simple in-memory storage (replace with database later)
pages_db = {}
emails_db = {}

# Generate AI Hook Title
@app.route('/api/generate-hook', methods=['POST'])
def generate_hook():
    try:
        data = request.json
        description = data.get('description', '')
        
        if not description:
            return jsonify({'error': 'Description required'}), 400
        
        # Use OpenAI to generate compelling hook title
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert copywriter specializing in creating attention-grabbing hook titles for affiliate marketing landing pages. Generate a compelling, short headline (under 10 words) that creates curiosity and urgency."
                },
                {
                    "role": "user",
                    "content": f"Create an attention-grabbing hook title for this: {description}"
                }
            ],
            temperature=0.7,
            max_tokens=50
        )
        
        hook_title = response.choices[0].message.content.strip()
        return jsonify({'hook_title': hook_title}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Create a Hook Page
@app.route('/api/pages', methods=['POST'])
def create_page():
    try:
        data = request.json
        
        # Validate required fields
        required = ['hook_title', 'description', 'image_url', 'affiliate_url']
        if not all(field in data for field in required):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Generate unique page ID
        page_id = str(uuid.uuid4())[:8]
        
        page_data = {
            'id': page_id,
            'hook_title': data['hook_title'],
            'description': data['description'],
            'image_url': data['image_url'],
            'affiliate_url': data['affiliate_url'],
            'created_at': datetime.now().isoformat(),
            'emails_captured': 0
        }
        
        pages_db[page_id] = page_data
        
        return jsonify({
            'success': True,
            'page_id': page_id,
            'page_url': f"http://localhost:5000/page/{page_id}",
            'copy_url': f"http://localhost:5000/page/{page_id}"
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get all pages for user dashboard
@app.route('/api/pages', methods=['GET'])
def get_pages():
    try:
        pages_list = list(pages_db.values())
        return jsonify(pages_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get single page details
@app.route('/api/pages/<page_id>', methods=['GET'])
def get_page(page_id):
    try:
        if page_id not in pages_db:
            return jsonify({'error': 'Page not found'}), 404
        
        page = pages_db[page_id]
        return jsonify(page), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Display the actual hook page (what visitors see)
@app.route('/page/<page_id>')
def view_page(page_id):
    try:
        if page_id not in pages_db:
            return "Page not found", 404
        
        page = pages_db[page_id]
        
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{page['hook_title']}</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                }}
                .container {{
                    background: white;
                    border-radius: 12px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    max-width: 600px;
                    width: 100%;
                    overflow: hidden;
                }}
                .image-container {{
                    width: 100%;
                    height: 300px;
                    overflow: hidden;
                }}
                .image-container img {{
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                }}
                .content {{
                    padding: 40px 30px;
                }}
                h1 {{
                    font-size: 28px;
                    color: #1a202c;
                    margin-bottom: 15px;
                    line-height: 1.3;
                }}
                .description {{
                    font-size: 16px;
                    color: #4a5568;
                    margin-bottom: 30px;
                    line-height: 1.6;
                }}
                .email-form {{
                    display: flex;
                    gap: 10px;
                    margin-bottom: 15px;
                }}
                input {{
                    flex: 1;
                    padding: 12px 15px;
                    border: 2px solid #e2e8f0;
                    border-radius: 6px;
                    font-size: 14px;
                    transition: border-color 0.3s;
                }}
                input:focus {{
                    outline: none;
                    border-color: #667eea;
                }}
                button {{
                    padding: 12px 30px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-size: 16px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: transform 0.2s, box-shadow 0.2s;
                }}
                button:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
                }}
                .privacy {{
                    font-size: 12px;
                    color: #a0aec0;
                    text-align: center;
                    margin-top: 20px;
                }}
                .loading {{
                    display: none;
                    text-align: center;
                    color: #667eea;
                    margin-top: 15px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="image-container">
                    <img src="{page['image_url']}" alt="{page['hook_title']}">
                </div>
                <div class="content">
                    <h1>{page['hook_title']}</h1>
                    <p class="description">{page['description']}</p>
                    
                    <form id="emailForm" class="email-form">
                        <input type="email" id="email" placeholder="Enter your email" required>
                        <button type="submit">Get Access</button>
                    </form>
                    
                    <div class="loading" id="loading">Redirecting...</div>
                    
                    <p class="privacy">✓ We respect your privacy. No spam, unsubscribe anytime.</p>
                </div>
            </div>
            
            <script>
                document.getElementById('emailForm').addEventListener('submit', async (e) => {{
                    e.preventDefault();
                    const email = document.getElementById('email').value;
                    
                    // Show loading
                    document.getElementById('loading').style.display = 'block';
                    
                    try {{
                        // Send email to backend
                        const response = await fetch('/api/capture-email', {{
                            method: 'POST',
                            headers: {{'Content-Type': 'application/json'}},
                            body: JSON.stringify({{
                                page_id: '{page_id}',
                                email: email
                            }})
                        }});
                        
                        if (response.ok) {{
                            // Redirect to affiliate link
                            window.location.href = '{page['affiliate_url']}';
                        }} else {{
                            alert('Error capturing email. Redirecting...');
                            setTimeout(() => {{
                                window.location.href = '{page['affiliate_url']}';
                            }}, 1000);
                        }}
                    }} catch (error) {{
                        console.error('Error:', error);
                        window.location.href = '{page['affiliate_url']}';
                    }}
                }});
            </script>
        </body>
        </html>
        """
        return html
    
    except Exception as e:
        return f"Error: {str(e)}", 500

# Capture email before redirect
@app.route('/api/capture-email', methods=['POST'])
def capture_email():
    try:
        data = request.json
        page_id = data.get('page_id')
        email = data.get('email')
        
        if not page_id or not email:
            return jsonify({'error': 'Missing required fields'}), 400
        
        if page_id not in pages_db:
            return jsonify({'error': 'Page not found'}), 404
        
        # Store email
        email_record = {
            'email': email,
            'page_id': page_id,
            'captured_at': datetime.now().isoformat(),
            'affiliate_url': pages_db[page_id]['affiliate_url']
        }
        
        email_id = str(uuid.uuid4())
        emails_db[email_id] = email_record
        
        # Update page email count
        pages_db[page_id]['emails_captured'] = pages_db[page_id].get('emails_captured', 0) + 1
        
        return jsonify({
            'success': True,
            'message': 'Email captured successfully'
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get all captured emails
@app.route('/api/emails', methods=['GET'])
def get_emails():
    try:
        emails_list = list(emails_db.values())
        return jsonify(emails_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get emails for specific page
@app.route('/api/pages/<page_id>/emails', methods=['GET'])
def get_page_emails(page_id):
    try:
        if page_id not in pages_db:
            return jsonify({'error': 'Page not found'}), 404
        
        page_emails = [email for email in emails_db.values() if email['page_id'] == page_id]
        return jsonify(page_emails), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health check
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    print("🚀 Hook Page Builder Backend Running on http://localhost:5000")
    app.run(debug=True, port=5000)
