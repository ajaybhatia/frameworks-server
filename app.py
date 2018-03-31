from flask import Flask, jsonify
from flask_mongoengine import MongoEngine
from marshmallow_mongoengine import ModelSchema
from mongoengine.errors import NotUniqueError


app = Flask(__name__)
app.config['MONGODB_DB'] = 'myframeworksdb'
app.config['MONGODB_HOST'] = 'mongodb://dbuser:dbpassword@ds231229.mlab.com:31229/myframeworksdb'
app.config['MONGODB_PORT'] = 31229

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


@app.route('/frameworks')
def frameworks():
  framework_schema = FrameworkSchema()

  output = []
  for framework in Framework.objects:
    output.append(framework_schema.dump(framework))

  return jsonify({'result': output})


if __name__ == '__main__':
  app.run(debug=True)



