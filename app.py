from flask import Flask, jsonify, request, render_template
from flask_mongoengine import MongoEngine
from marshmallow_mongoengine import ModelSchema
from mongoengine.errors import NotUniqueError


# New Flask App
app = Flask(__name__)
# Configs for mLab
app.config['MONGODB_DB'] = 'myframeworksdb'
app.config['MONGODB_HOST'] = 'mongodb://dbuser:dbpassword@ds231229.mlab.com:31229/myframeworksdb'
app.config['MONGODB_PORT'] = 31229

# Create instance of MongoEngine
db = MongoEngine(app)


# Document Classes
class Framework(db.Document):
  name = db.StringField(unique=True)
  language = db.StringField()


# Document Schemas
class FrameworkSchema(ModelSchema):
  class Meta:
    model = Framework


# Routes

# Fixture of Frameworks
@app.route('/fixture-frameworks')
def fixture_frameworks():
  try:
    framework_schema = FrameworkSchema()

    Framework(name='Flask', language='Python').save()
    Framework(name='Spring', language='Java').save()
    Framework(name='Express', language='Node').save()
    Framework(name='Laravel', language='Php').save()

    output = []
    for framework in Framework.objects:
      output.append(framework_schema.dump(framework))

    return jsonify({'result': output})
  except NotUniqueError:
    return jsonify({'result': 'Already Exists!!!'})


# List all Frameworks
@app.route('/frameworks')
def frameworks():
  framework_schema = FrameworkSchema()

  output = []
  for framework in Framework.objects:
    output.append(framework_schema.dump(framework))

  return jsonify({'result': output})


# Retrieve a Framework by name
@app.route('/framework/<name>')
def get_framework(name):
  framework_schema = FrameworkSchema()
  framework = Framework.objects.get(name=name)
  output = framework_schema.dump(framework)

  return jsonify({'result': output})


# Update a Framework by name
@app.route('/framework/<name>', methods=['PUT'])
def update_framework(name):
  framework_schema = FrameworkSchema()

  data = request.get_json(force=True)
  new_name = data['name']
  new_language = data['language']

  framework = Framework.objects.get(name=name)
  framework.name = new_name
  framework.language = new_language
  framework = framework.save()

  output = framework_schema.dump(framework)

  return jsonify({'result': output})


# Delete a Framework by name
@app.route('/framework/<name>', methods=['DELETE'])
def remove_framework(name):
  framework_schema = FrameworkSchema()

  framework = Framework.objects.get(name=name)
  framework.delete()

  return jsonify({'result': 'Removed'})


# Create new Framework
@app.route('/framework', methods=['POST'])
def new_framework():
  framework_schema = FrameworkSchema()

  data = request.get_json(force=True)
  name = data['name']
  language = data['language']

  framework = Framework(name=name, language=language).save()
  output = framework_schema.dump(framework)

  return jsonify({'result': output})


# Home Page
@app.route('/')
def home():
  return render_template('index.html')


if __name__ == '__main__':
  app.run(debug=True)
