from getsecret import *
import json

def lambda_handler(event, context):
    # TODO implement
    resp_data = {}
    print(event)

    if event['password'].strip() == '':
        return {}
    resp = get_secret( event['serverId'] + '/' +  event['username'] )
    if resp != None:
        resp_dict = json.loads(resp)
        print(resp_dict)
    else:
        print("Secrets Manager exception thrown")
        return {}
        
    if event['password'] != resp_dict['password']: 
        return {}
    
    resp_data['Role'] = resp_dict['role']
    print("Completed Response Data: "+json.dumps(resp_data))
    return resp_data
    
    
    
