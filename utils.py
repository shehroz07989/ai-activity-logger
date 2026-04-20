def validate(data):
    valid_users = []
    invalid_users = []
    invalid_data = []
    if isinstance(data,dict):
        results = data.get("results",[])
        for index,i in enumerate(results,start=1):
            if not isinstance(i,dict):
                invalid_users.append({
                     "valid":False,
                     "reason": "not a dictionary",
                     "user_no": index,
                })
                continue

            name = i.get("name",{})
            first_name = name.get("first","")
            if not isinstance(name,dict):
                invalid_users.append({
                     "valid":False,
                     "reason": "email missing",
                     "user_no": index,
                    })
                continue
            if not name_validator(first_name):
                invalid_users.append({
                     "valid":False,
                     "reason": "name missing",
                     "user_no": index ,
                })
                continue   
            email = i.get("email", "")
            if  not email_validator(email):
                invalid_users.append({
                     "valid":False,
                     "reason": "email missing",
                     "user_no": index,
                })
                continue
            age = i.get("dob",{}).get("age",None)
            if not age_validator(age):
                invalid_users.append({
                     "valid":False,
                     "reason": "age missing",
                     "user_no": index,
                })
                continue
            valid_users.append({
                 "valid": True,
                 "name": first_name,
                 "email": email,
                 "age": age,
            })
        return {
                "valid_users": valid_users,
                "invalid_users": invalid_users,
                }
    else:
        invalid_data.append({
                     "data":False,
                     "reason": "data not a dictionary",
                })
        return invalid_data
        
                             
    
    


def name_validator(first_name):   
    if not isinstance(first_name,str):
            return False
    if first_name == "":
                return False
    return True
            
        
def email_validator(email):
        if not isinstance(email,str):
            return False
        if email.count("@") != 1:
            return False
        parts = email.split("@") 
        left = parts[0]
        right = parts[1]
        if  left == "" or right == "":
            return False
        return True
        
def age_validator(age):
        if not isinstance(age,int):
            return False
        if age <= 0:
            return False
        return True
    
def decision(data):
    decision_users = []
    valid = data.get("valid_users")
    if valid:
        for i in valid:
            age = i.get("age",0)
            name =  i.get("name","")
            email =  i.get("email","")
            if 17< age <= 25:
                decision_users.append ({
                   "rank": "junior",
                  "name": name,
                   "age": age,
                   "email": email,
                } )
            elif 25 < age <= 40:
                decision_users.append({
               "rank": "senior",
               "name": name,
               "age": age,
               "email": email,
              })
            elif age > 40:
                decision_users.append({
               "rank": "expert",
               "name": name,
               "age": age,
               "email": email,
                })
            else:
                decision_users.append({
               "rank": "skip",
               "name": name,
               "age": age,
               "email": email,
                })
        return {
         "decision": decision_users
        }