from flask import render_template,request, session, redirect, url_for, flash,current_app
import random
import os
from forms import Form, create_form
import mongo

   
class BaseCrud(object):
    
    def __init__(self, name, **kwargs):
        super(BaseCrud, self).__init__()
        self.name=name
        self.pk_type='int'
        self.navigation_hint=name+'.list'
        self.form=[]
        self.label=name.capitalize()
        self.url='/{0}/'.format(name)
        self.parent=None
        self.labels={}
        self.list_columns=[]
        self.form=Form()
        self.collection=None


        if 'pk_type' in kwargs: self.pk_type=kwargs['pk_type'] 
        if 'navigation_hint' in kwargs: self.navigation_hint=kwargs['navigation_hint'] 
        if 'label' in kwargs: self.label=kwargs['label'] 
        if 'url' in kwargs: self.url=kwargs['url'] 
        if 'labels' in kwargs: self.labels=kwargs['labels'] 
        if 'list_columns' in kwargs:
            self.list_columns=create_columns(kwargs['list_columns'])
        if 'form' in kwargs: 
            self.form=create_form(kwargs['form'],self.labels)  
        



    def list(self):
        context = self.__get_context()
        context['rows']=self.collection.list()
        return self.render('list', context) 

    def view(self, id):
        obj=self.collection.find(self.pk_prop,id)
        context = self.__get_context()
        context['obj']=obj
        return 'view '+str(id)+' '+str(context)

    def edit(self, id):
        obj=self.collection.find(self.pk_prop,id)
        context = self.__get_context()
        context['obj']=obj
        context['form']=self.form
        context['form_data']=self.form.form_data(obj)
        
        if request.method == 'POST':
            data=self.form.form_data(request.form)
            errors=self.form.validate(data)
            if not errors:
                self.form.set_obj(request.form, obj)
                self.collection.update(obj)
                flash('<strong>{name}</strong> updated!'.format(name=self.get_label(obj)))
                return redirect(url_for('%s.list' % self.name, id=id))
            else:
                context['form_data']=data
                context['form_errors']=errors

        return self.render('edit', context) 

    def delete(self, id):
        obj=self.collection.find(self.pk_prop,id)
        context = self.__get_context()
        context['obj']=obj
        self.collection.delete(obj)
        flash('<strong>{name}</strong> deleted!'.format(name=self.get_label(obj)))
        return redirect(url_for('%s.list' % self.name))

    def new(self):
        obj=self.collection.new_object()
        context = self.__get_context()
        context['obj']=obj
        context['form']=self.form
        context['form_data']=self.form.form_data(obj)

        if request.method == 'POST':
            data=self.form.form_data(request.form)
            errors=self.form.validate(data)
            if not errors:
                self.form.set_obj(request.form, obj)
                self.collection.save(obj)
                flash('<strong>{name}</strong> created!'.format(name=self.get_label(obj)))
                return redirect(url_for('%s.list' % self.name))
            else:
                context['form_data']=data
                context['form_errors']=errors
                            
    
        return self.render('new', context) 

    def __get_context(self):
        ctx= { 'crud_name':self.name, 'crud':self }
        if self.parent:
            ctx['app']=self.parent
        if self.navigation_hint:
            ctx['navigation_hint']=self.navigation_hint
        return ctx    

    def get_tempalte(self,view):
        template='%s/%s/%s/%s.html' % (current_app.root_path,current_app.template_folder, self.name, view)
        if os.path.exists(template):
            return '%s/%s.html' % (self.name, view)
        return'crud/%s.html' % view 

    def render(self, view, context):
        return render_template( self.get_tempalte(view) , **context)  

    def get_label(self, obj):
        return obj

    def get_id(self, obj):
        return obj
    

    def register(self, app):
        id_name='<id>'
        if self.pk_type:
            id_name='<%s:id>' % self.pk_type

        app.add_url_rule('%sl' % self.url, '{0}.list'.format(self.name), self.list)   
        app.add_url_rule('%sv/%s' % (self.url,id_name), '{0}.view'.format(self.name), self.view)   
        app.add_url_rule('%se/%s' % (self.url, id_name), '{0}.edit'.format(self.name), self.edit, methods=['POST', 'GET'])   
        app.add_url_rule('%sd/%s' % (self.url, id_name), '{0}.delete'.format(self.name), self.delete)   
        app.add_url_rule('%sn' % self.url, '{0}.new'.format(self.name), self.new, methods=['POST', 'GET'])   



class BaseDictCrud(BaseCrud):

    def __init__(self, name, **kwargs):
        super(BaseDictCrud, self).__init__(name, **kwargs)
        self.objects=[]
        self.pk_prop='id'
        self.label_prop='name'

        if 'objects' in kwargs: self.objects=kwargs['objects'] 
        if 'pk_prop' in kwargs: self.pk_prop=kwargs['pk_prop'] 
        if 'label_prop' in kwargs: self.label_prop=kwargs['label_prop'] 


    def get_id(self, obj):
        return obj[self.pk_prop]

    def get_label(self, obj):
        return obj[self.label_prop]


        

class Collection(object):

    def __init__(self, objects=[] ):
        super(Collection, self).__init__()
        self.objects=objects

    def find(self, col, v):
        return  next(u for u in self.objects if u[col] == v)

    def list(self):
        return self.objects  

    def new_object(self):
        return {}             

    def save(self,obj):
        obj['id']=random.randint(0,100000)
        self.objects.append(obj)

    def update(self,obj):
        pass

    def delete(self,obj):
        self.objects.remove(obj)

        

class CrudMeta(type):
    def __init__(cls, name, bases, attrs):
        type.__init__(cls, name, bases, attrs)
        
        options = {}
        for name in dir(cls):
            if not name.startswith('_'):
                f = getattr(cls, name)
                options[name]=f
        cls._options = options
            
               

class Crud( CrudMeta('NewBase',(BaseDictCrud,),{})):
    
    def __init__(self):
        super(Crud, self).__init__(**self._options)    


class AppModel(object):
    
    def __init__(self, *initial_data, **kwargs):
        super(AppModel, self).__init__()
        self.project_name='Project'
        self.roots=[]  

        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

        print '>>>>>>>>',initial_data[0]['data']   
        roots=[]    
        for r in self.roots:
            root=BaseDictCrud(**r)
            root.parent=self

            data_ref_name=r.get('data_ref', root.name)

            if data_ref_name in initial_data[0]['data']:
                data_ref=initial_data[0]['data'][data_ref_name]
                if type(data_ref)==dict:
                    root.collection=mongo.MongoCollection(**data_ref)
                else:    
                    root.collection=Collection(objects=data_ref)
            else:
                root.collection=Collection(objects=[])
            roots.append(root) 
        self.roots=roots    

    def register(self, app):
        for f in self.roots:
            f.register(app)
            

    def add(self, root):
        self.roots.append(root)
        root.parent=self        
    

class Base(object):
      def __init__(self, *initial_data, **kwargs):
        super(Base, self).__init__()
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])


class Column(object):

    def __init__(self, name, widget='text'):
        super(Column, self).__init__()

def create_columns(ops):
    columns=[]
    for o in ops:
        if type(o)==str:
            columns.append({ 'name': o ,  'as':'text'  })
        if type(o)==dict:
            k=o.keys()[0]
            v=o.get(k,{ 'as':'text' })
            dd={ 'name': k }
            dd.update(v)
            columns.append(dd)   
    print columns
    return columns 



if __name__ == '__main__':
    c=BaseDictCrud('name', pk_type='int', navigation_hint='2')
    print c.navigation_hint