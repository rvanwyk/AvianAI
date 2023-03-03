from google.cloud import storage
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/file/file.json"

# Initialize Google Cloud Storage client
client = storage.Client()

# Get the bucket object
bucket_name = 'avian_motion'
bucket = client.bucket(bucket_name)

# List all blobs in the bucket
blobs = bucket.list_blobs()

# Generate HTML code to display all images
html = '<!DOCTYPE html>\n<html>\n<head>\n  <title>My Image Gallery</title>\n  <style>\n    img {\n      max-width: 100%;\n      height: auto;\n      display: block;\n      margin: auto;\n      margin-bottom: 20px;\n    }\n    h1 {\n      text-align: center;\n    }\n    body {\n      max-width: 800px;\n      margin: auto;\n      padding: 20px;\n    }\n  </style>\n</head>\n<body>\n  <h1>My Image Gallery</h1>\n  <div>\n'
for blob in blobs:
    if blob.content_type.startswith('image/'):
        url = blob.public_url
        html += '    <img src="{}" alt="{}">\n'.format(url, blob.name)
html += '  </div>\n</body>\n</html>'

# Write the HTML code to a file
with open('all_images.html', 'w') as f:
    f.write(html)
