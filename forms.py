
class Form(object):
    
    def __init__(self):
        super(Form, self).__init__()
        self.fields=[]

    def as_text(self):
        for f in self.fields:
            print f.label, f.name, f.widget, f.validators    

    def form_data(self, obj):
        d={}
        for f in self.fields:
            d[f.name]=obj.get(f.name)
        return d

    def validate(self, d):
        errors={}
        for f in self.fields:
            f.validate(d,errors)
        return errors

class Field(object):

    def __init__(self, name, label=None, widget='text', validators=[]):
        super(Field, self).__init__()
        self.name=name
        self.label=name
        if label:
            self.label=label
        
        self.widget=widget
        self.validators=validators

    def value(self, obj):
        if self.name in obj and obj[self.name]:
            return obj[self.name]
        return ''

    def validate(self, obj,errors):
        if self.validators:
            for v in self.validators:
                print v
                if v=='required':
                    if self.name not in obj or not obj.get(self.name) or len(obj.get(self.name).strip())==0:
                        errors[self.name]='required'

        


def create_form(field_props, labels):
    form=Form()
    fields=[]
    for f in field_props:
        if type(f)==str:
            field=Field(f, labels.get(f) )
        if type(f)==dict:
            validators=[]
            if 'validators' in f:
                v=f['validators']
                if type(v)==str:
                    validators=[v]
                if type(v)==list:
                    validators=v
            print '>>>',f, labels, validators        
            field=Field(name=f['name'], label=labels.get(f['name']),validators=validators)
        if field:

            fields.append(field)

    form.fields=fields    
    return form

def make_dict(f, prop='name'):
    if type(f)==str:
        return {prop:f}
    if type(f)==dict:
        return f
    raise Exception() 




    


if __name__ == '__main__':
    labels={'name':'Name', 'actions':'Actions'}
    #fields={    {'name': {'validators':'requried' }}, 'actions', {'desc': {'widget':'richtext'}}}
    fields=[ 'name', { 'name' : 'actions' ,'validators':'requried'},'name123' ] 
    form=create_form(fields, labels)
    form.as_text()
    