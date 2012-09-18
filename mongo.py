from pymongo import Connection
from bson.objectid import ObjectId

class MongoCollection(object):

    def __init__(self, db_name, col_name ):
        super(MongoCollection, self).__init__()
        con=Connection()
        db=con[db_name]
        self.collection=db[col_name]
       
    def find(self, col, v):
        d={}
        d[col]=ObjectId(v)
        return self.collection.find_one( d )

    def list(self):
        return self.collection.find()  

    def new_object(self):
        return {}             

    def save(self,obj):
        self.collection.insert(obj, safe=True)

    def update(self,obj):
        d={}
        for k in obj:
            if k != '_id':
                d[k]=obj[k]
        self.collection.update(self._get_id_spec(obj), {'$set':d } ,safe=True)

    def delete(self,obj):
        self.collection.remove(self._get_id_spec(obj),safe=True)

    def _get_id_spec(self, obj):
        return  { '_id': ObjectId(obj['_id'])}



if __name__ == '__main__':
    c=MongoCollection('test', 'apps')
    for a in c.list():
        print a['name'], a.get('description'), a['_id']

    print c.find( '_id', '4ff45db031b8e7a11b000001')

    c.save({'name':'aaaaaaaaa', 'description':'cccccccc'})
    print c.collection.find_one( name= 'aaaaaaaaa')



