from linkedin.linkedin import extract_linkedin_posts
import json
with open('output_final.json','r') as f:
    data = json.load(f)

print(len(data))

