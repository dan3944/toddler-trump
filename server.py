import os
import prefixer
import sys
from flask import Flask

app = Flask(__name__)
app.run(app.run(host='0.0.0.0', port=os.environ.get('PORT')))

handle = sys.argv[1] if len(sys.argv) >= 2 else 'realDonaldTrump'
print('Handle:', handle)

prefixer.reset_rules(handle)
prefixer.run(handle)
