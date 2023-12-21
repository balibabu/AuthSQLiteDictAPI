from sqlitedict import SqliteDict
class SQLiteDictDB:
    def create_file(self,filename):
        with open(filename,'w'):
            pass
    def set_file(self, filename):
        self._filepath = filename
    def set_table_name(self, table):
        self._table_name = table
    def read(self, key):
        with SqliteDict(self._filepath, tablename=self._table_name, autocommit=True) as db:
            return db[key]
    def override(self, key, value):
        with SqliteDict(self._filepath, tablename=self._table_name, autocommit=True) as db:
            db[key] = value
    def has(self, key):
        with SqliteDict(self._filepath, tablename=self._table_name, autocommit=True) as db:
            val = db.get(key)
            return val is not None
    def get_table_names(self):
        return SqliteDict.get_tablenames(self._filepath)
    def get_keys(self):
        with SqliteDict(self._filepath, tablename=self._table_name, autocommit=True) as db:
            return list(db.iterkeys())
    def get_content_as_dict(self):
        with SqliteDict(self._filepath, tablename=self._table_name, autocommit=True) as db:
            return dict(db.iteritems())
    def delete(self, key):
        with SqliteDict(self._filepath, tablename=self._table_name, autocommit=True) as db:
            del db[key]
    def deleteTable(self, tableName):
        with SqliteDict(self._filepath, autocommit=True) as db:
            db.conn.select_one(f'DROP TABLE "{tableName}"')