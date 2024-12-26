import json
from openai import OpenAI
import os
import re


api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

# for backward compatibility, you can still use `https://api.deepseek.com/v1` as `base_url`.
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-coder",
    messages=[
        {"role": "system", "content": 
"""As a helpful assistant, you will write clean, well-organized, and easy-to-understand front-end code. The code should be written in markdown format, with file names indicated as section titles using the "###" prefix. Different files should be separated by a "---".

Focus on creating simple, understandable, and modular code. Include necessary comments to explain the purpose of each section or function.

Below is a template to follow:

### script.js
```javascript
// Your code here
```
---
### style.css
```css
/* Your code here */
```
---
### index.html
```html
<!-- Your code here -->
```
"""},
        {"role": "user", "content": "Write a blog website with blue theme"},
  ],
    max_tokens=1024,
    temperature=0.0,
    stream=False,
    response_format={
        'type': 'json_object'
    }
)

print(json.loads(response.choices[0].message.content))

# Here’s a simple blog website with a blue theme. The design is clean and modular, with a focus on readability and simplicity.

# ---

# ### style.css
# ```css
# /* General Styles */
# body {
#     font-family: Arial, sans-serif;
#     margin: 0;
#     padding: 0;
#     background-color: #f0f8ff; /* Light blue background */
#     color: #333;
# }

# /* Header */
# header {
#     background-color: #0073e6; /* Dark blue header */
#     color: white;
#     padding: 20px;
#     text-align: center;
# }

# header h1 {
#     margin: 0;
#     font-size: 2.5em;
# }

# /* Navigation */
# nav {
#     background-color: #005bb5; /* Slightly darker blue for navigation */
#     padding: 10px;
#     text-align: center;
# }

# nav a {
#     color: white;
#     text-decoration: none;
#     margin: 0 15px;
#     font-size: 1.2em;
# }

# nav a:hover {
#     text-decoration: underline;
# }

# /* Main Content */
# main {
#     padding: 20px;
# }

# .blog-post {
#     background-color: white;
#     padding: 20px;
#     margin-bottom: 20px;
#     border-radius: 8px;
#     box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
# }

# .blog-post h2 {
#     color: #0073e6; /* Dark blue for post titles */
#     margin-top: 0;
# }

# .blog-post p {
#     line-height: 1.6;
# }

# /* Footer */
# footer {
#     background-color: #0073e6; /* Dark blue footer */
#     color: white;
#     text-align: center;
#     padding: 10px;
#     position: fixed;
#     bottom: 0;
#     width: 100%;
# }
# ```

# ---

# ### index.html
# ```html
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Blue Theme Blog</title>
#     <link rel="stylesheet" href="style.css">
# </head>
# <body>
#     <!-- Header -->
#     <header>
#         <h1>Blue Theme Blog</h1>
#     </header>

#     <!-- Navigation -->
#     <nav>
#         <a href="#">Home</a>
#         <a href="#">About</a>
#         <a href="#">Contact</a>
#     </nav>

#     <!-- Main Content -->
#     <main>
#         <div class="blog-post">
#             <h2>Welcome to My Blog</h2>
#             <p>This is a simple blog website with a blue theme. It's designed to be clean, readable, and easy to navigate. Feel free to explore and read the posts!</p>
#         </div>

#         <div class="blog-post">
#             <h2>Why I Love Blue</h2>
#             <p>Blue is a calming and serene color. It reminds me of the sky and the ocean, and it brings a sense of peace and tranquility. That's why I chose it as the theme for this blog.</p>
#         </div>
#     </main>

#     <!-- Footer -->
#     <footer>
#         <p>&copy; 2023 Blue Theme Blog. All rights reserved.</p>
#     </footer>
# </body>
# </html>
# ```

# ---

# ### script.js
# ```javascript
# // Optional: Add interactivity or dynamic content here
# // For example, you could fetch blog posts from an API and display them dynamically.

# // Example: Add a simple alert when the page loads
# window.onload = function() {
#     alert("Welcome to the Blue Theme Blog!");
# };
# ```

# ---

# This code creates a simple blog website with a blue theme. The `style.css` file defines the colors and layout, the `index.html` file structures the content, and the `script.js` file can be used to add interactivity if needed.

def write_files_from_response(response):
    print("Parsing response and writing files...")
    sections = re.split(r'### (.+)', response.choices[0].message.content)
    for i in range(1, len(sections), 2):
        filename = sections[i].strip()
        content = sections[i + 1].strip().strip('```').strip()
        print(f"Writing to file: {filename}")
        with open(filename, 'w') as file:
            file.write(content)
    print("Files written successfully.")
