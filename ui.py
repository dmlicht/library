import re
import sys
from library import Library

class LibraryTerminalInterface(object):
    def __init__(self):
        self.library = Library()

    def run(self):
        print "Welcome to your library!"
        while True:
            user_input = sys.stdin.readline()
            #TODO: ADD TRY BLOCK
            action, args = self.parse_query(user_input)
            if action == 'quit':
                break
            else:
                self.execute(action, args)

    def parse_query(self, input_string):
        #TODO: push actions definition to decorators
        parsers = {
            'show': self.parse_show,
            'add': self.parse_add,
            'read': self.parse_read
        }
        action, arg_string = input_string.split(" ", 1)
        parser = parsers.get(action, False)
        args = (parser and parser(arg_string)) or []
        return action, args

    def parse_add(self, arg_string):
        """returns an ordered list containing title and author
        throws exception if input string is bad"""
        quote_terms = re.findall(r'\"(.+?)\"', arg_string)
        if len(quote_terms) == 2:
            return quote_terms
        raise Exception('BAD ADD INPUT')

    def parse_show(self, arg_string):
        """returns list containing state of books to return
        and author to filter by if author supplied in arg string"""
        tokens = arg_string.split()
        all_or_unread = tokens[0]
        returns = []
        returns.append(all_or_unread)
        if all_or_unread not in ['all', 'unread']:
            raise Exception('BAD SHOW INPUT')
        if len(tokens) > 1:
            quote_terms = re.findall(r'\"(.+?)\"', arg_string)
            if ('by' not in arg_string) or (len(quote_terms) is not 1):
                raise Exception('BAD SHOW INPUT')
            author = quote_terms[0]
            returns.append(author)
        return returns

    def parse_read(self, arg_string):
        """returns a list containing only title
        throws exception if input string is bad"""
        quote_terms = re.findall(r'\"(.+?)\"', arg_string)
        if len(quote_terms) == 1:
            if len(quote_terms[0])+2 != len(arg_string):
                raise Exception('BAD_READ_INPUT')
            return quote_terms
        else:
            raise Exception('BAD_READ_INPUT')

    def execute(self, action, args):
        """executes given action with args list"""
        exec 'result = self.library.' + action + '(*args)'
