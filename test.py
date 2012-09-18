import yaml
import crud

from pymongo import Connection

def test_yaml():
    with open('/home/argrinst/Projects/flask-crud/instance/app.yaml') as f:
        c = f.read()
        data= yaml.load(c)
        print data
        model=crud.AppModel(data)
        print model.project_name
        print model.roots[1].form.fields[2].validators

if __name__ == '__main__':
    connection = Connection()
    db=connection.test
    print db.apps.find()
    for a in db.apps.find():
        print a
    print db.collection_names()