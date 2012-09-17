from flask import render_template,request, session, redirect, url_for, flash,current_app
import random
import os
from forms import Form, create_form

   
class BaseCrud(object):
    

    def __init__(self, name, **kwargs):
        super(BaseCrud, self).__init__()
        self.name=name
        self.pk_type='int'
        self.navigation_hint=name+'.list'
        self.form=[]
        self.label=name
        self.url='/{0}/'.format(name)
        self.parent=None
        self.labels={}
        self.list_columns=[]
        self.form=Form()



        if 'pk_type' in kwargs: self.pk_type=kwargs['pk_type'] 
        if 'navigation_hint' in kwargs: self.navigation_hint=kwargs['navigation_hint'] 
        if 'label' in kwargs: self.label=kwargs['label'] 
        if 'url' in kwargs: self.url=kwargs['url'] 
        if 'labels' in kwargs: self.labels=kwargs['labels'] 
        if 'list_columns' in kwargs: self.list_columns=kwargs['list_columns'] 
        if 'form' in kwargs: 
            self.form=create_form(kwargs['form'],self.labels)  
        



    def list(self):
        context = self.__get_context()
        context['rows']=self.get_objects()
        return self.render('list', context) 

    def view(self, id):
        obj=self.get_object(id)
        context = self.__get_context()
        context['obj']=obj
        return 'view '+str(id)+' '+str(context)

    def edit(self, id):
        obj=self.get_object(id)
        context = self.__get_context()
        context['obj']=obj
        context['form']=self.form
        context['form_data']=self.form.form_data(obj)
        
        if request.method == 'POST':
            data=self.form.form_data(request.form)
            errors=self.form.validate(data)
            if not errors:
                self.formToModel(request.form, obj, False)
                self.update(obj)
                flash('<strong>{name}</strong> updated!'.format(name=self.get_label(obj)))
                return redirect(url_for('%s.list' % self.name, id=id))
            else:
                context['form_data']=data
                context['form_errors']=errors

        return self.render('edit', context) 

    def delete(self, id):
        obj=self.get_object(id)
        context = self.__get_context()
        context['obj']=obj
        self.delete_obj(obj)
        flash('<strong>{name}</strong> deleted!'.format(name=self.get_label(obj)))
        return redirect(url_for('%s.list' % self.name))

    def new(self):
        obj=self.new_object()
        context = self.__get_context()
        context['obj']=obj
        context['form']=self.form
        context['form_data']=self.form.form_data(obj)

        if request.method == 'POST':
            data=self.form.form_data(request.form)
            errors=self.form.validate(data)
            if not errors:
                self.formToModel(request.form, obj, True)
                self.save(obj)
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
        app.add_url_rule('%sl' % self.url, '{0}.list'.format(self.name), self.list)   
        app.add_url_rule('%sv/<%s:id>' % (self.url, self.pk_type), '{0}.view'.format(self.name), self.view)   
        app.add_url_rule('%se/<%s:id>' % (self.url, self.pk_type), '{0}.edit'.format(self.name), self.edit, methods=['POST', 'GET'])   
        app.add_url_rule('%sd/<%s:id>' % (self.url, self.pk_type), '{0}.delete'.format(self.name), self.delete)   
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



    def get_object(self,id):
        return  next(u for u in self.objects if u[self.pk_prop] == id)

    def get_objects(self):
        return self.objects  

    def new_object(self):
        return {}             

    def get_id(self, obj):
        return obj[self.pk_prop]

    def get_label(self, obj):
        return obj[self.label_prop]

    def formToModel(self, form, obj ,isNew):
        for f in self.form.fields:
            obj[f.name]=request.form[f.name]
        if isNew:
            obj[self.pk_prop]=random.randint(0,100000)
        

    def save(self,obj):
        self.objects.append(obj)

    def update(self,obj):
        pass

    def delete_obj(self,obj):
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

        roots=[]    
        for r in self.roots:
            root=BaseDictCrud(**r)
            root.parent=self
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




if __name__ == '__main__':
    c=BaseDictCrud('name', pk_type='int', navigation_hint='2')
    print c.navigation_hint