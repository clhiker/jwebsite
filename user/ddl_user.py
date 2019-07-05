# from django.db import models
# from django.contrib import admin
#
#
# class DDL:
#     def __init__(self):
#         pass
#
#
# def create_model(name,
#                  fields=None,
#                  app_label='',
#                  module='',
#                  options=None,
#                  admin_opts=None):
#     """
#     Create specified model
#     """
#     class Meta:
#         pass
#
#     if app_label:
#         setattr(Meta, 'app_label', app_label)
#     if options is not None:
#         for key, value in options.iteritems():
#             setattr(Meta, key, value)
#     attrs = {'__module__': module, 'Meta': Meta}
#     if fields:
#         attrs.update(fields)
#     model = type(name, (models.Model,), attrs)
#     if admin_opts is not None:
#         class Admin(admin.ModelAdmin):
#             pass
#         for key, value in admin_opts:
#             setattr(Admin, key, value)
#         admin.site.register(model, Admin)
#
#     return model
#
#
# def install(model):
#     from django.db import connection
#
#     with connection.schema_editor() as editor:
#         editor.create_model(model)
#
#
# class MysqlDDL(DDL):
#     def addUserTable(self, name):
#         fields = {
#             'virtual_path': models.CharField('文件虚拟地址', max_length=256),
#             'df_type': models.CharField('类型', max_length=256),
#             'name': models.CharField('文件名', max_length=256),
#             'size': models.CharField('文件大小', max_length=256),
#             'true_path': models.CharField('文件实际地址', max_length=256),
#             'change_time': models.CharField('文件修改日期', max_length=256),
#             'hash_code': models.CharField('文件哈希', max_length=256),
#             'form_type': models.CharField('文件类型', max_length=256),
#         }
#         user_file_model = create_model(
#             name=name,
#             fields=fields,
#             app_label='bpcloud',
#             module='jwebsite.bpcloud.no_models'
#         )
#         install(user_file_model)
#


import pymysql


class FileDDL:
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='7155293',
            db='bpcloud',
            charset='utf8'
        )
        self.cursor = self.connection.cursor()

    def createTable(self, table):
        # 使用 execute() 方法执行 SQL，如果表存在则删除
        # self.cursor.execute("DROP TABLE IF EXISTS {table}".format(table=self.table))
        # 使用预处理语句创建表
        sql = """CREATE TABLE {table} (
                up_path varchar(256) primary key ,
                df_type char(1),
                name varchar(256),
                size varchar(256),
                true_path varchar(256),
                change_time varchar(256),
                hash_code varchar(256),
                form_type varchar(256),
                delete_time varchar(256),
                 )""".format(
            table=table
        )

        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            print('create table error!')
            self.connection.rollback()
        self.connection.close()


if __name__ == '__main__':
    ddl = FileDDL()
    ddl.createTable('test')