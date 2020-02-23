from databases.base import MySQLBase


class TestModel(MySQLBase):

    def __init__(self):
        super(TestModel, self).__init__()
        self.table = 'test_model'
        self.field_list = {
        }

    def create_model(self, item):
        try:
            self.cursor.execute(
                f'''
                INSERT INTO {self.table} 
                ( name,description,language,type )
                VALUES
                ( '{item.name}', '{item.description}', '{item.language}', '{item.type}' );  
                '''
            )
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def get_model(self, name):
        try:
            self.cursor.execute(
                f'''
                SELECT *
                FROM {self.table}
                WHERE name='{name}'
                '''
            )
        except Exception as e:
            raise e

        result = self.cursor.fetchall()

        return result[0]