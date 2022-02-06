import json


class query_builder():

    def __init__(self, *args, **kwargs):  # I need to write more in the init function
        self.database = None
        self.table = None
        self.req_type = None
        self.fields = None
        self.set_field = None
        self.where = None
        self.query = None
        self.comment = None
        self.dep = None
        self.update = None
        self.result = {}

    def set_database(self, database):
        assert type(database) == str or database == None
        self.database = database

    def set_table(self, table):
        assert type(table) == str or table == None
        self.table = table

    def set_req_type(self, req_type):
        assert type(req_type) == str and req_type in [
            'insert', 'update', 'describe', 'delete', 'select', 'alter', 'show']
        self.req_type = req_type

    def set_fields(self, fields):
        assert type(fields) == dict or type(fields) == list or fields == None
        self.fields = fields

    def set_set(self, set_field):
        assert type(set_field) == dict or set_field == None
        self.set_field = set_field

    def set_where(self, where):
        assert type(where) == dict or where == None
        self.where = where

    def set_comment(self, comment):
        assert type(comment) == str or comment == None
        self.comment = comment

    def set_dep(self, dep):
        assert type(dep) == dict or dep == None
        self.dep = dep

    def set_update(self, update):
        assert type(update) == dict or update == None
        self.update = update

    def build(self):
        header = {}
        data = {}
        footer = {}
        if(self.req_type == 'insert'):
            if(self.database and self.table and self.fields):
                header.update({"DATABASE": self.database})
                header.update({"TABLE_NAME": self.table})
                header.update({"REQUEST_TYPE": self.req_type})
                data.update({"FIELDS": self.fields})
                footer.update({"COMMENT": self.comment})
                footer.update({"DEP": self.dep})
                footer.update({"UPDATE": self.update})
                self.result.update({"HEADER": header})
                self.result.update({"DATA": data})
                self.result.update({"FOOTER": footer})
        elif(self.req_type == 'select'):
            if(self.database and self.table and self.fields):
                header.update({"DATABASE": self.database})
                header.update({"TABLE_NAME": self.table})
                header.update({"REQUEST_TYPE": self.req_type})
                data.update({"FIELDS": self.fields})
                data.update({"WHERE": self.where})
                footer.update({"DEP": self.dep})
                footer.update({"UPDATE": self.update})
                self.result.update({"HEADER": header})
                self.result.update({"DATA": data})
                self.result.update({"FOOTER": footer})
        elif(self.req_type == 'update'):
            if(self.database and self.table and self.fields):
                header.update({"DATABASE": self.database})
                header.update({"TABLE_NAME": self.table})
                header.update({"REQUEST_TYPE": self.req_type})
                data.update({"FIELDS": self.fields})
                data.update({"SET": self.set_field})
                data.update({"WHERE": self.where})
                footer.update({"DEP": self.dep})
                footer.update({"UPDATE": self.update})
                self.result.update({"HEADER": header})
                self.result.update({"DATA": data})
                self.result.update({"FOOTER": footer})
        elif(self.req_type == 'describe'):
            header.update({"DATABASE": self.database})
            header.update({"TABLE_NAME": self.table})
            header.update({"REQUEST_TYPE": self.req_type})
            self.result.update({"HEADER": header})
        elif(self.req_type == 'delete'):
            if(self.database and self.table and self.fields):
                header.update({"DATABASE": self.database})
                header.update({"TABLE_NAME": self.table})
                header.update({"REQUEST_TYPE": self.req_type})
                data.update({"WHERE": self.where})
                footer.update({"DEP": self.dep})
                footer.update({"UPDATE": self.update})
                self.result.update({"HEADER": header})
                self.result.update({"DATA": data})
                self.result.update({"FOOTER": footer})
        elif(self.req_type == 'alter'):
            pass
        elif(self.req_type == 'show'):
            header.update({"REQUEST_TYPE": self.req_type})
            self.result.update({"HEADER": header})

    def get_query(self):
        return self.result.copy()

    def to_json(self):
        return json.dumps(self.result)


if __name__ == "__main__":
    pass
else:
    pass
