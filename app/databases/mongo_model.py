from databases.base import MongoDBCollection


class TestCol(MongoDBCollection):

    _collection = 'test-collection'

    def __init__(self):
        super(TestCol, self).__init__()
        self.field_list = {
        }

    def create_lang(self, item):
        try:
            self.coll.insert_one(item.dict())
        except Exception as e:
            raise e

    def find_lang(self, name):
        try:
            result = self.coll.find_one({'name': name})
            result['_id'] = str(result['_id'])
        except Exception as e:
            raise e

        return result