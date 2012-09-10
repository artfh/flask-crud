
class BaseForm(object):

    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__()
        print kwargs
        self.fields=kwargs['fields']
        self.prefix=kwargs['prefix']


class FormMeta(type):
    def __init__(cls, name, bases, attrs):
        type.__init__(cls, name, bases, attrs)
        print 'init'
        
        options = {}
        for name in dir(cls):
            if not name.startswith('_'):
                f = getattr(cls, name)
                options[name]=f
        cls._options = options
            
               

class Form( FormMeta('NewBase',(BaseForm,),{})):
    
    def __init__(self):
        super(Form, self).__init__(**self._options)    
        

class MyForm(Form):    
    fields='nameField'
    prefix='actionField'


if __name__ == '__main__':
    print '-----------'
    f=BaseForm(fields=1,prefix=1)
    print f.fields

    mf=MyForm()
    print mf
    print mf.fields

    print MyForm().fields


    

    
    