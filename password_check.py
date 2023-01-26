import requests
import hashlib
import sys


def request_api_data(query_char):
    url = "https://api.pwnedpasswords.com/range/" + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f"Error fetching: {res.status_code}, check the API and try again")
    return res

def get_leaks_count(hashes, hash_to_check):
    hashes = (line.split(":") for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(passw):
    sha1pass = hashlib.sha1(passw.encode("utf-8")).hexdigest().upper()
    first5, tail = sha1pass[:5], sha1pass[5:]
    response = request_api_data(first5)
    return get_leaks_count(response, tail)


def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f"{password} was found {count} times. You should change it.")
        else:
            print(f"{password} was NOT found. That's a good password")
    return "done"

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))


# вариант на доработку - собирать пароли из файла. Открыть файл, пройтись по нему, проверить пароли. Вывести результат в файл?