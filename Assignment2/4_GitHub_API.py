import requests

url = "https://api.github.com/users/maryamsaeedi17"

response = requests.get(url=url)

followers_num = response.json()['followers']
following_num = response.json()['following']

print("The number of your followers: ", followers_num)

print("The number of your following: ", following_num)
