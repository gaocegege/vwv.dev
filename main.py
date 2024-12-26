from openai import OpenAI
import os


api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

# for backward compatibility, you can still use `https://api.deepseek.com/v1` as `base_url`.
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-coder",
    messages=[
        {"role": "system", "content": "You are a helpful assistant, who will help me to write front-end code. Your code should be clean, well-organized, and easy to understand."},
        {"role": "user", "content": "Write a blog website with blue theme"},
  ],
    max_tokens=1024,
    temperature=0.0,
    stream=False
)

print(response.choices[0].message.content)

# The output will be:
# ---

# ### **HTML (index.html)**
# ```html
# <!DOCTYPE html>
# <html lang="en">
# <head>
#   <meta charset="UTF-8">
#   <meta name="viewport" content="width=device-width, initial-scale=1.0">
#   <title>Blue Blog</title>
#   <link rel="stylesheet" href="styles.css">
# </head>
# <body>
#   <header>
#     <div class="container">
#       <h1>Blue Blog</h1>
#       <nav>
#         <ul>
#           <li><a href="#">Home</a></li>
#           <li><a href="#">About</a></li>
#           <li><a href="#">Blog</a></li>
#           <li><a href="#">Contact</a></li>
#         </ul>
#       </nav>
#     </div>
#   </header>

#   <main class="container">
#     <section class="blog-posts">
#       <article class="post">
#         <h2>Post Title 1</h2>
#         <p class="meta">Posted on January 1, 2023</p>
#         <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam scelerisque leo a libero tincidunt, id fermentum nisi tincidunt.</p>
#         <a href="#" class="read-more">Read More</a>
#       </article>
#       <article class="post">
#         <h2>Post Title 2</h2>
#         <p class="meta">Posted on February 15, 2023</p>
#         <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam scelerisque leo a libero tincidunt, id fermentum nisi tincidunt.</p>
#         <a href="#" class="read-more">Read More</a>
#       </article>
#     </section>

#     <aside class="sidebar">
#       <h3>Categories</h3>
#       <ul>
#         <li><a href="#">Technology</a></li>
#         <li><a href="#">Lifestyle</a></li>
#         <li><a href="#">Travel</a></li>
#         <li><a href="#">Health</a></li>
#       </ul>
#     </aside>
#   </main>

#   <footer>
#     <div class="container">
#       <p>&copy; 2023 Blue Blog. All rights reserved.</p>
#     </div>
#   </footer>

#   <script src="script.js"></script>
# </body>
# </html>
# ```

# ---

# ### **CSS (styles.css)**
# ```css
# /* General Styles */
# body {
#   font-family: Arial, sans-serif;
#   line-height: 1.6;
#   margin: 0;
#   padding: 0;
#   background-color: #f0f8ff; /* Light blue background */
#   color: #333;
# }

# .container {
#   width: 90%;
#   max-width: 1200px;
#   margin: 0 auto;
# }

# /* Header Styles */
# header {
#   background-color: #0073e6; /* Dark blue */
#   color: #fff;
#   padding: 20px 0;
#   text-align: center;
# }

# header h1 {
#   margin: 0;
# }

# nav ul {
#   list-style: none;
#   padding: 0;
#   margin: 10px 0 0;
# }

# nav ul li {
#   display: inline;
#   margin: 0 15px;
# }

# nav ul li a {
#   color: #fff;
#   text-decoration: none;
#   font-weight: bold;
# }

# nav ul li a:hover {
#   text-decoration: underline;
# }

# /* Main Content Styles */
# main {
#   display: flex;
#   margin: 20px 0;
# }

# .blog-posts {
#   flex: 3;
#   margin-right: 20px;
# }

# .post {
#   background-color: #fff;
#   padding: 20px;
#   margin-bottom: 20px;
#   border-radius: 8px;
#   box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
# }

# .post h2 {
#   margin-top: 0;
# }

# .post .meta {
#   color: #666;
#   font-size: 0.9em;
# }

# .post .read-more {
#   display: inline-block;
#   margin-top: 10px;
#   color: #0073e6;
#   text-decoration: none;
#   font-weight: bold;
# }

# .post .read-more:hover {
#   text-decoration: underline;
# }

# /* Sidebar Styles */
# .sidebar {
#   flex: 1;
#   background-color: #fff

def write_files_from_response(response):
    sections = response.choices[0].message.content.split('### **')
    for section in sections[1:]:
        header, content = section.split('**', 1)
        file_name = header.strip().lower().replace(' ', '_')
        content = content.split('```')[1].strip()  # Extract content between the first pair of ```
        print (file_name)
        with open(file_name, 'w') as file:
            file.write(content)
            print(f"Written to {file_name}")
            print(f"Content written to {file_name}:\n{content}\n")

write_files_from_response(response)
