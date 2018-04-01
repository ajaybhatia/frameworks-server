from flask import Flask, jsonify, request, render_template
from flask_mongoengine import MongoEngine
from mongoengine.errors import NotUniqueError

import mongoengine_goodjson as gj
import json


# New Flask App
app = Flask(__name__)
# Configs for mLab
app.config['MONGODB_DB'] = 'myframeworksdb'
app.config['MONGODB_HOST'] = 'mongodb://dbuser:dbpassword@ds231229.mlab.com:31229/myframeworksdb'
app.config['MONGODB_PORT'] = 31229
# connect('myframeworksdb', host='mongodb://dbuser:dbpassword@ds231229.mlab.com:31229/myframeworksdb')

# Create instance of MongoEngine
db = MongoEngine(app)


# Document Classes
class Framework(gj.Document):
  name = db.StringField(unique=True)
  language = db.StringField()


# Routes

# Fixture of Frameworks
@app.route('/fixture-frameworks')
def fixture_frameworks():
  try:
    Framework(name='Flask', language='Python').save()
    Framework(name='Spring', language='Java').save()
    Framework(name='Express', language='Node').save()
    Framework(name='Laravel', language='Php').save()

    return jsonify({'result': 'Fixture executed!!!'})
  except NotUniqueError:
    return jsonify({'result': 'Already Exists!!!'})


# List all Frameworks
@app.route('/frameworks')
def frameworks():
  return jsonify({'result': [json.loads(o.to_json()) for o in Framework.objects]})


# Retrieve a Framework by name
@app.route('/framework/<name>')
def get_framework(name):
  framework = Framework.objects.get(name=name)
  return jsonify({'result': json.loads(framework.to_json())})


# Update a Framework by name
@app.route('/framework/<name>', methods=['PUT'])
def update_framework(name):
  data = request.get_json(force=True)
  new_name = data['name']
  new_language = data['language']

  framework = Framework.objects.get(name=name)
  framework.name = new_name
  framework.language = new_language
  framework = framework.save()

  return jsonify({'result': json.loads(framework.to_json())})


# Delete a Framework by name
@app.route('/framework/<name>', methods=['DELETE'])
def remove_framework(name):
  framework = Framework.objects.get(name=name)
  framework.delete()

  return jsonify({'result': 'Removed'})


# Delete a Framework by name
@app.route('/frameworks', methods=['DELETE'])
def remove_all_frameworks():
  for framework in Framework.objects:
    framework.delete()

  return jsonify({'result': 'Removed All!'})


# Create new Framework
@app.route('/framework', methods=['POST'])
def new_framework():
  data = request.get_json(force=True)
  name = data['name']
  language = data['language']

  framework = Framework(name=name, language=language).save()
  return jsonify({'result': json.loads(framework.to_json())})


# Home Page
@app.route('/')
def home():
  return render_template('index.html')


if __name__ == '__main__':
  app.run(debug=True)
