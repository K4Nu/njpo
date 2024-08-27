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