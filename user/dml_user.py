from user.models import User


class DML:
    def __init__(self):
        pass


class MysqlDML(DML):
    def queryUser(self, username, password):
        username_db = User.objects.filter(username=username)
        if not username_db.exists():
            return {'res': "用户名不存在"}
        else:
            password_in_db = User.objects.get(username=username)
            if password != password_in_db.password:
                return {'res': "密码不正确"}
            else:
                return {'res': "up200"}

    def addUser(self, username, password, email):
        username_db = User.objects.filter(username=username)
        if username_db.exists():
            return {'res': "用户名已存在"}
        else:
            User.objects.create(username=username, password=password, email=email)
            return {'res': "re200"}

    def updatePassword(self, username, new_password):
        User.objects.filter(username=username).update(password=new_password)

    def deleteUser(self, username):
        User.objects.get(username=username).delete()