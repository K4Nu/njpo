from abc import ABC,abstractmethod
from collections import deque
from time import time
import re

class User:
    def __init__(self, name, role,logged_in=False):
        self.name = name
        self.role = role
        self.request_times=deque()
        self.logged_in=logged_in
class Request:
    def __init__(self, method,data,file):
        self.method = method
        self.data=data
        self.file=file

class Handler(ABC):
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    @abstractmethod
    def handle(self, user, request):
        pass

class AuthorizationHandler(Handler):
    requests = {
        "GET": ["admin", "employee", "user"],
        "POST": ["admin", "employee"],
        "DELETE": ["admin"],
        "PUT": ["admin", "employee"],
    }

    def handle(self, user, request):
        try:
            if user.role in self.requests[request]:
                if self.next_handler:
                    self.next_handler.handle(user,request)
                else:
                    return True
            else:
                print("User does not has access to this request")
                return False
        except KeyError:
            print(f"Request method {request.method} is not recognized.")
            return False

class FileHandler(Handler):

    def handle(self, user, request):
        try:
            if request.method=="POST" and request.file:
                if self.next_handler:
                    self.next_handler.handle(user,request)
                else:
                    return True
            else:
                print("The request does not has file")
                return False
        except KeyError:
            print("The request does not works")
            return False


class RateLimitHandler(Handler):
    def __init__(self, next_handler=None, max_requests_per_minute_logged_in=10, max_requests_per_minute_guest=5):
        super().__init__(next_handler)
        self.max_requests_per_minute_logged_in = max_requests_per_minute_logged_in
        self.max_requests_per_minute_guest = max_requests_per_minute_guest

    def handle(self, user, request):
        current_time = time()
        # Usuń żądania starsze niż 60 sekund
        while user.request_times and current_time - user.request_times[0] > 60:
            user.request_times.popleft()

        max_requests = self.max_requests_per_minute_logged_in if user.logged_in else self.max_requests_per_minute_guest

        if len(user.request_times) < max_requests:
            user.request_times.append(current_time)
            if self.next_handler:
                return self.next_handler.handle(user, request)
            else:
                return True
        else:
            print(f"User {user.name} has exceeded the request limit of {max_requests} per minute.")
            return False

class SQLInjectionHandler(Handler):

    def handle(self, user, request):
        if request.data:
            if re.search(r"(;|--|\b(OR|AND)\b\s*['\"]\s*\d|\b(UNION|SELECT|INSERT|UPDATE|DELETE|DROP)\b)", request.data,re.IGNORECASE):
                print(f"Potential SQL injection attempt detected in request data: {request.data}")
                return False
        if self.next_handler:
            self.next_handler.handle(user,request)
        else:
            return True

class HttpRequestHandler(Handler):
    def handle(self, user, request):
        print(f"Handling {request.method} request for {user.name}.")
        return True

user1 = User("Alice", "admin", logged_in=True)
user2 = User("Bob", "user", logged_in=False)

request_get = Request("GET")
request_post_with_file = Request("POST", data="valid_data", file="some_file.txt")
request_post_with_bad_data = Request("POST", data="invalid_data'; DROP TABLE users; --")
request_delete = Request("DELETE")


handler_chain = SQLInjectionHandler(
    AuthorizationHandler(
        FileHandler(
            RateLimitHandler(
                HttpRequestHandler()
            )
        )
    )
)

from abc import ABC,abstractmethod
class Validator(ABC):
    def __init__(self,next_handle=None):
        self.next_handle=next_handle
    @abstractmethod
    def validate(self,sentence):
        pass

class ParenthessesValidator(Validator):

     def validate(self,sentence):
         if sentence.count("(")!=sentence.count(")"):
             print("The parenthesses are not even")
             return False
         else:
             if self.next_handle:
                 return self.next_handle.validate(self,sentence)
             return True

class VariableValidator(Validator):

    def validate(self,sentence):
        parts = sentence.replace('(', '').replace(')', '').split('=')
        for char in parts:
            if not part.isalnum() and not all(char in "+-*/=" for char in part):
                print("The sentence is wrong")
                return False
        if self.next_handle:
            return self.next_handle.validate(self,sentence)
        return True

class EqualValidator(Validator):

    def validate(self,sentence):
        if "=" not in sentence:
            print("wrong sentence")
            return False
        if sentence.count("=")>1:
            print("too much equal signs")
            return False
        if self.next_handle:
            return self.next_handle.validate(self,sentence)
        return True

class OperatorValidator(Validator):

    def validate(self,sentence):
        operators=["+","-","*","/"]
        if not any(operators) in sentence:
            print("wrong sentence")
            return False
        if self.next_handle:
            return self.next_handle.validate(sentence)
        return True

class GeneralValidator(Validator):

    def validate(self,sentence):
        try:
            left,right=sentence.split("=")
            eval(left)
            eval(right)
            if self.next_handle:
                return self.next_handle.validate(sentence)
            return True
        except:
            print("wrong sentence")
            return False