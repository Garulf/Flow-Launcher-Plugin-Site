import sys

from website import app
from flask_frozen import Freezer

if __name__ == '__main__':
    if sys.argv > 1 and sys.argv[1] == 'build':
        freezer = Freezer(app)
        freezer.freeze()
    else:
        app.run(debug=True)
