import pymysql
import time


class FileDML:
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='7155293',
            db='bpcloud',
            charset='utf8'
        )
        self.table = ''
        self.cursor = self.connection.cursor()

    def setTable(self, table):
        self.table = table

    def insert(self,
               up_path,
               name,
               change_time,
               size='',
               true_path='',
               df_type='D',
               hash_code='',               
               delete_time='',
               form_type='',
               ):
        sql = '''INSERT INTO {table}
                (up_path,df_type,name,size,true_path,
                change_time,hash_code,form_type, delete_time)
                VALUES 
                ('{up_path}','{df_type}','{name}','{size}','{true_path}',
                '{change_time}','{hash_code}', '{form_type}','{delete_time}');
                '''.format(
            table=self.table,
            up_path=up_path,
            df_type=df_type,
            name=name,
            size=size,
            true_path=true_path,
            change_time=change_time,
            hash_code=hash_code,
            form_type=form_type,
            delete_time=delete_time,
        )
        self.cursor.execute(sql)
        # try:
        #     self.cursor.execute(sql)
        #     return True
        # except:
        #     print('insert error!')
        #     self.connection.rollback()
        #     return False

    # 新建文件夹
    def createDir(self, up_path, name, change_time):
        self.insert(up_path, name, change_time)

    # 放入回收站：回收站中的文件夹是无法打开的
    def delete(self, up_path, name, df_type, now_time):        
        sql = '''UPDATE {table} SET delete_time='{now_time}'
                WHERE up_path = '{up_path}' 
                and name = '{name}' 
                and df_type = '{df_type}'
                and delete_time='' 
                '''.format(
            table=self.table,
            now_time=now_time,
            up_path=up_path,
            name=name,
            df_type=df_type
        )
        if df_type == 'F':
            try:
                self.cursor.execute(sql)
            except:
                print('update error!')
                self.connection.rollback()
                return False
            return True
        # 如果是文件夹
        else:
            old_up_path = up_path + name + '/'
            sql_2 = '''UPDATE {table} SET delete_time='closed'
                      WHERE instr(up_path,'{old_up_path}') = 1 and delete_time=''
                    '''.format(
                table=self.table,
                old_up_path=old_up_path,
            )
            try:
                self.cursor.execute(sql)
                self.cursor.execute(sql_2)
                
            except:
                print('update error!')
                self.connection.rollback()
                return False
            return True

    # 彻底删除
    def deleteComplete(self, up_path, name, df_type):
        sql = '''DELETE FROM {table}
                WHERE up_path = '{up_path}' 
                and name = '{name}' 
                and df_type = '{df_type}'                
                '''.format(
            table=self.table,
            up_path=up_path,
            name=name,
            df_type=df_type,
        )
        if df_type == 'F':
            try:
                self.cursor.execute(sql)
                
                return True
            except:
                print('insert error!')
                self.connection.rollback()
                return False
        else:
            old_up_path = up_path + name + '/'
            sql_2 = '''DELETE FROM {table}
                      WHERE instr(up_path,'{old_up_path}') = 1                       
                    '''.format(
                table=self.table,
                old_up_path=old_up_path,
            )
            try:
                self.cursor.execute(sql)
                self.cursor.execute(sql_2)
                
            except:
                print('update error!')
                self.connection.rollback()
                return False
            return True

    # 传递一个查找条件目录，返回一个元组包含一列信息（即目录下所有的对象）
    def queryAll(self, up_path):
        print(up_path)
        sql = '''select * 
                from {table}
                where up_path='{up_path}' and delete_time=''
                '''.format(
            table=self.table,
            up_path=up_path,
        )
        try:
            self.cursor.execute(sql)
        except:
            print('query all error!')
            self.connection.rollback()
            return None
        result = self.cursor.fetchall()
        return result

    def queryDustbin(self):
        sql = '''select * 
                from {table}
                where delete_time!='' and delete_time != 'closed'
                '''.format(
            table=self.table,
        )
        try:
            self.cursor.execute(sql)
        except:
            print('query dustbin error!')
            self.connection.rollback()
            return None
        result = self.cursor.fetchall()

        return result

    # 移动
    def update(self, up_path, name, df_type, to_path):
        sql = '''UPDATE {table} SET up_path='{new_path}'
                WHERE up_path = '{up_path}' 
                and name = '{name}'
                and df_type = '{df_type}' 
                and delete_time=''
                '''.format(
            table=self.table,
            new_path=to_path,
            up_path=up_path,
            name=name,
            df_type=df_type,
        )
        if df_type == 'F':
            try:
                self.cursor.execute(sql)
                
            except:
                print('update error!')
                self.connection.rollback()
                return False
            return True
        # 如果是文件夹
        else:
            old_up_path = up_path + name + '/'
            new_up_path = to_path + name + '/'
            sql_2 = '''UPDATE {table} SET up_path=insert(
                        up_path, 
                        1, 
                        length('{old_up_path}'),
                        '{new_up_path}')
                      WHERE instr(up_path,'{old_up_path}') = 1 
                      and delete_time=''
                    '''.format(
                table=self.table,
                new_up_path=new_up_path,
                old_up_path=old_up_path,
            )
            try:
                self.cursor.execute(sql)
                self.cursor.execute(sql_2)
                
            except:
                print('update error!')
                self.connection.rollback()
                return False
            return True

    def insertCopy(self, new_up_path, up_path, name, df_type):
        sql = '''INSERT INTO {table}(up_path,df_type,name,size,
                        true_path,change_time,hash_code)                                 
                        (select '{new_up_path}',df_type,name,size,
                        true_path,change_time,hash_code
                        from {table}
                        WHERE up_path = '{up_path}' 
                        and name = '{name}'
                        and df_type = '{df_type}' 
                        and delete_time='')
                        '''.format(
            table=self.table,
            new_up_path=new_up_path,
            up_path=up_path,
            name=name,
            df_type=df_type,
        )
        try:
            self.cursor.execute(sql)
            
        except:
            print('copy error!')
            self.connection.rollback()
            return False

    def recuCopy(self, old_up_path, new_up_path):
        children = self.queryAll(old_up_path)       # 把所有的子类拿出来
        for item in children:
            if item[1] == 'D':
                dir_name = item[0] + item[2] + '/'
                dir_new_up_path = new_up_path + item[2] + '/'
                self.insertCopy(new_up_path, old_up_path, item[2], 'D')
                self.recuCopy(dir_name, dir_new_up_path)
            else:
                self.insertCopy(new_up_path, old_up_path, item[2], 'F')

    # 复制
    def copy(self, up_path, name, df_type, to_path):
        if df_type == 'F':
            return self.insertCopy(to_path, up_path, name, 'F')
        # 如果是文件夹
        else:
            old_up_path = up_path + name + '/'
            new_up_path = to_path + name + '/'
            self.insertCopy(to_path, up_path, name, 'D')
            self.recuCopy(old_up_path, new_up_path)

    # 重命名
    def rename(self, up_path, name, df_type, new_name):
        sql = '''UPDATE {table} SET name='{new_name}'
                WHERE up_path = '{up_path}' 
                and name = '{name}'
                and df_type = '{df_type}' 
                and delete_time=''
                '''.format(
            table=self.table,
            new_name=new_name,
            up_path=up_path,
            name=name,
            df_type=df_type
        )
        if df_type == 'F':
            try:
                self.cursor.execute(sql)
                
            except:
                print('update error!')
                self.connection.rollback()
                return False
            return True
        # 如果是文件夹
        else:
            old_up_path = up_path + name + '/'
            new_up_path = up_path + new_name + '/'
            sql_2 = '''UPDATE {table} SET up_path=insert(
                        up_path, 
                        1, 
                        length('{old_up_path}'),
                        '{new_up_path}')
                      WHERE instr(up_path,'{old_up_path}') = 1  and delete_time=''
                    '''.format(
                table=self.table,
                new_up_path=new_up_path,
                old_up_path=old_up_path,
            )
            try:
                self.cursor.execute(sql)
                self.cursor.execute(sql_2)
                
            except:
                print('update error!')
                self.connection.rollback()
                return False
            return True

    # 恢复之前要先检查，如果有一个新的文件在哪里，需要解决冲突
    def queryRecoveryConflict(self, name, df_type, delete_time):
        sql = '''select name 
                from {table}
                WHERE name = '{name}' 
                and df_type = '{df_type}'
                and delete_time='{delete_time}' 
                and concat(up_path,name,'/') in (
                select concat(up_path,name,'/')
                from {table}
                WHERE delete_time='' 
                )
                '''.format(
            table=self.table,
            delete_time=delete_time,
            name=name,
            df_type=df_type,
        )
        try:
            self.cursor.execute(sql)
        except:
            print('query recovery conflict error!')
            self.connection.rollback()
            return None

        answer = self.cursor.fetchall()
        if answer == ():
            return None
        return answer[0][0]

    # 恢复
    def queryUpPath(self, dir_path):
        sql = '''select *
                from {table}
                where concat(up_path,name,'/') = '{dir_path}';
                '''.format(
            table=self.table,
            dir_path=dir_path,
        )
        try:
            self.cursor.execute(sql)
        except:
            print('query up path error!')
            self.connection.rollback()
            return None
        return self.cursor.fetchall()

    def createUpPath(self, up_path):
        if up_path == '/':
            return
        if not self.queryUpPath(up_path):
            up_path = up_path[:up_path.rfind('/')]
            name = up_path[up_path.rfind('/')+1:]
            upper_path = up_path[: up_path.rfind('/')-1]
            self.createDir(upper_path, name,
                           time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        else:
            up_path = up_path[:up_path.rfind('/')]
            upper_path = up_path[: up_path.rfind('/') - 1]
            self.createUpPath(upper_path)

    def recovery(self, name, df_type, delete_time):
        # 首先要检查是否已经将其所在的文件夹删除了，
        # 如果删除了要新建
        recovery_up_path = self.queryOne('up_path', name, df_type, delete_time)
        self.createUpPath(recovery_up_path)

        sql = '''UPDATE {table} SET delete_time=''
                        WHERE name = '{name}' 
                        and df_type = '{df_type}'
                        and delete_time='{delete_time}' 
                        '''.format(
            table=self.table,
            delete_time=delete_time,
            name=name,
            df_type=df_type,
        )
        if df_type == 'F':
            try:
                self.cursor.execute(sql)
            except:
                print('update error!')
                self.connection.rollback()
                return False
            return True
        # 如果是文件夹
        else:
            old_up_path = recovery_up_path + name + '/'
            sql_2 = '''UPDATE {table} SET delete_time=''
                              WHERE instr(up_path,'{old_up_path}') = 1 
                              and delete_time != ''
                            '''.format(
                table=self.table,
                delete_time=delete_time,
                old_up_path=old_up_path,
            )
            try:
                self.cursor.execute(sql)
                self.cursor.execute(sql_2)
            except:
                print('update error!')
                return False
            return True

    def queryTruePath(self, up_path, name):
        sql = '''select true_path
                from {table}
                where up_path = '{up_path}'
                and name = '{name}'  
                and df_type='F' 
                and delete_time='';
                '''.format(
            table=self.table,
            up_path=up_path,
            name=name,
        )
        try:
            self.cursor.execute(sql)
        except:
            print('query true path error!')
            self.connection.rollback()
            return None
        answer = self.cursor.fetchall()
        if len(answer) == 0:
            return None
        return answer[0][0]

    def queryOne(self, thing, name, df_type, delete_time):
        sql = '''select {thing}
                from {table}
                where name = '{name}'  
                and df_type='{df_type}' 
                and delete_time='{delete_time}';
                '''.format(
            thing=thing,
            table=self.table,
            name=name,
            df_type=df_type,
            delete_time=delete_time
        )
        try:
            self.cursor.execute(sql)
        except:
            print('query one error!')
            self.connection.rollback()
            return None
        answer = self.cursor.fetchall()
        if len(answer) == 0:
            return None
        return answer[0][0]

    def queryTable(self):
        sql = '''select *
                from {table}                    
            '''.format(
            table=self.table,
        )
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        for item in result:
            print(item)

    def queryConflict(self, to_path):
        sql = '''select name, df_type
                from {table}
                where up_path = '{to_path}';
                '''.format(
            table=self.table,
            to_path=to_path,
        )
        try:
            self.cursor.execute(sql)
        except:
            print('query conflict error!')
            self.connection.rollback()
            return None
        return self.cursor.fetchall()
    
    def commit(self):
        self.connection.commit()

    def closeConnect(self):
        self.connection.close()


if __name__ == '__main__':
    dml = FileDML()
    dml.setTable('test')
    dml.insert('/A/', 'd.mp3', '2019-5-17', '100M',
               '/home/ddd.mp3', 'F', 'today is happy', '')
    # print(dml.queryAll('/'))
    # now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # dml.delete('/A/', 'B', 'D', now_time)
    # dml.recover('B', 'D', '2019-06-29 14:22:09')
    # dml.deleteComplete('/A/', 'c.txt', 'F')
    # dml.createDir('/', 'name', '2018-8-12',)
    # dml.delete('/', 'C', 'D')
    # dml.update('/', '/A', 'D', 'test')
    # dml.copy('/A/', 'C', '/', 'D')
    # dml.rename('/A/', 'C', 'B', 'D')
    # dml.queryTable()

    dml.closeConnect()