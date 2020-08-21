import os
from flask import Flask

app = Flask(__name__)
app.run(app.run(host='0.0.0.0', port=os.environ.get('PORT')))
