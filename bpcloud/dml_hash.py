from bpcloud.models import HashFiles


class DML:
    def __init__(self):
        pass


class DMLHash(DML):

    def queryHash(self, hash_code):
        files_db = HashFiles.objects.filter(hash_code=hash_code)
        if files_db.exists():
            return True
        else:
            return False

    def queryHashFiles(self, size, true_path, hash_code):
        files_db = HashFiles.objects.filter(hash_code=hash_code)
        if not files_db.exists():
            # 添加文件
            self.addHashFile(size, true_path, hash_code)
            return None
        else:
            # 返回文件信息
            files_db = HashFiles.objects.get(hash_code=hash_code)
            return {'size': files_db.size,
                    'true_path': files_db.true_path,
                    'hash_code': files_db.hash_code,
                    }

    def addHashFile(self, size, true_path, hash_code):
        HashFiles.objects.create(size=size, true_path=true_path, hash_code=hash_code)

    def updateHashFiles(self, size, new_true_path):
        HashFiles.objects.filter(size=size).update(true_path=new_true_path)

    def deleteHashFile(self, size):
        HashFiles.objects.get(size=size).delete()