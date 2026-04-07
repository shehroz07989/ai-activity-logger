def json_return(response):
    data = response.json()
    return data

def filter_posts(data):
    x = []
    for i in data:
        if i.get("id") and i.get("id") > 5:
            x.append({
                "id": i.get("id"),
                "title": i.get("title")
                 })
        
    return x

def display_posts(x):
    for i in x:
        print(f"ID - {i.get('id')} -- Title - {i.get('title')}")