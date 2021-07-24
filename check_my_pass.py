import hashlib
import sys

import requests


def request_api_date(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
    return res


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())

    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    # check password if it exists in API response
    sha1password = hashlib.sha1(password.encode()).hexdigest().upper()
    first5_char, tale = sha1password[:5], sha1password[5:]
    response = request_api_date(first5_char)
    return get_password_leaks_count(response, tale)


def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'You should change your password. It was found {count} times.')
        else:
            print("It wasn't found. Carry on!")
    return 'done'


main(sys.argv[1:])
