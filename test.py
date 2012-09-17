import yaml
import crud

if __name__ == '__main__':

    with open('/home/argrinst/Projects/flask-crud/instance/app.yaml') as f:
        c = f.read()
        data= yaml.load(c)
        print data
        model=crud.AppModel(data)
        print model.project_name
        print model.roots[1].form.fields[2].validators
