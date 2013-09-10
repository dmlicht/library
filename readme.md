Library
=======

## David Lichtenberg

## Structure
The application breaks into two pieces:
* data structures -contained in library.py
* user interaction -contained in ui.py

main.py creates an instance of TerminalLibraryInterface (from ui.py) and starts it running. 

### Tests
Tests are written using the pytest framework.
To install pytest, run: pip install pytest
To run the tests, run: py.test

Tests for library and ui are contained in test/test_library.py and test/test_ui.py, respectively. conftest.py contains fixture definitions. 
To learn more about pytest, visit: http://pytest.org/
