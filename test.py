data = [
    {"name": "Ali", "balance": "500"},
    {"name": "Sara", "balance": "abc"},
    {"name": "Ahmed"},
    {"name": "", "balance": "300"},
    {"balance": "200"},
    "random_string",
    12345,
    {"name": "Zara", "balance": "-100"},
    {"name": "Usman", "balance": "1500"}
]


def validate(data):
    if isinstance(data, list):
        return True
    else:
        return False


def validate_users(data):
    validate_user = []
    invalid_user = []
    if validate(data):
        for i in data:
            if  not isinstance(i, dict):
                invalid_user.append(i)
                continue
                          
            elif i.get("name") and i.get("balance"):
                    try:
                        i["balance"] = int(i.get("balance"))
                        if i["balance"] > 100:
                            validate_user.append(i)
                        else:
                            invalid_user.append(i)
                    except:
                        invalid_user.append(i)
            else:
                invalid_user.append(i)
            
               
                    
        return {
                "   Valid": validate_user,
                "Invalid": invalid_user,
            }
result = validate_users(data)
print(result)