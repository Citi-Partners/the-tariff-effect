import re

with open('generate_site.py', 'r') as f:
    content = f.read()

# Find and replace the problematic section
old_section = '''published_str = original.get('published', '')
            if published_str:
                try:
                    article_datetime = date_parser.parse(published_str)
                   article_datetime = article_datetime.replace(tzinfo=None)
              except:
                    pass'''

new_section = '''                published_str = original.get('published', '')
                if published_str:
                    try:
                        article_datetime = date_parser.parse(published_str)
                        article_datetime = article_datetime.replace(tzinfo=None)
                    except:
                        pass'''

content = content.replace(old_section, new_section)

with open('generate_site.py', 'w') as f:
    f.write(content)

print("Fixed!")
