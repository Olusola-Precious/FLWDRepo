import os
import requests



def get_droplets():

    transaction_id = 1839314
    url = 'https://api.flutterwave.com/v3/transactions/{}/verify'.format(
        transaction_id)
    d = 1839314 # os.getenv('ACCESS_TOKEN')
    #print(d)
    #print(os.getenv('SECRET_ADMIN_URL'))
    
    r = requests.get(url, headers={
                     'Authorization': 'Bearer %s' % 'FLWSECK_TEST-dc31c69f07d5feb57e91f417b94f8a09-X'})
    droplets = r.json()

    """
    droplet_list = []
    for i in range(len(droplets['droplets'])):
        droplet_list.append(droplets['droplets'][i])
    return droplet_list
    """
    return  droplets['status']

if __name__=='__main__':
    print(get_droplets())
