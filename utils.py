def status_check(response):
    if 200 <= response.status_code < 300:
        return response.json()
    else:
        return f"Status Code Error: {response.status_code}" 
def clean_post(data):
    cleaned_post = []
    for i in data:
        if i.get("id") and i.get("title"):
            cleaned_post.append(
                {
                    "id": i.get("id"),
                    "title": i.get("title"),
                }
            )
    return cleaned_post

def filter_post(cleaned_post):
    filtered_post = []
    for i in cleaned_post:
        if i.get("id") > 5:
            filtered_post.append(
                {
                    "id": i.get("id"),
                    "title": i.get("title"),
                }
            )
    return filtered_post

def display_post(filtered_post):
    display = []
    for i in filtered_post:
        display.append(
            f"ID: {i.get('id')} - Title: {i.get('title')}",
        
            )
    return display