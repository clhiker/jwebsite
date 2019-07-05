from bpcloud.dml_file import FileDML
import time


class Deal:
    def __init__(self):
        self.file_dml = FileDML()

    def setTable(self, table):
        self.file_dml.setTable(table)

    # 返回当前页面的所有Line
    def getPageInfo(self, now_path):
        info = self.file_dml.queryAll(now_path)
        result = {}
        for item in info:
            info_dict = {}
            # info_dict['up_path']        = item[0]
            info_dict['df_type']        = item[1]
            info_dict['name']           = item[2]
            info_dict['size']           = item[3]
            # info_dict['true_path']      = item[4]
            info_dict['change_time']    = item[5]
            # info_dict['hash_code']      = item[6]
            # info_dict['form_type']      = item[7]
            # info_dict['delete_time']    = item[8]
            result[info.index(item)] = info_dict

        # self.file_dml.closeConnect()
        return result

    # 获取回收站页面信息
    def getDustbinInfo(self):
        info = self.file_dml.queryDustbin()
        result = {}
        for item in info:
            info_dict = {}
            # info_dict['up_path']        = item[0]
            info_dict['df_type']        = item[1]
            info_dict['name']           = item[2]
            info_dict['size']           = item[3]
            # info_dict['true_path']      = item[4]
            info_dict['change_time']    = item[5]
            # info_dict['hash_code']      = item[6]
            info_dict['form_type']      = item[7]
            # info_dict['delete_time']    = item[8]
            result[info.index(item)] = info_dict
        return result

    # 增删拷移
    def operateDFile(self, key, now_path, name, info, df_type):
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 新建文件夹
        if key == 'create':
            if self.file_dml.createDir(now_path, info, now_time):
                return True
        # 放入回收站
        elif key == 'delete':
            if self.file_dml.delete(now_path, name, df_type, now_time):
                return True
        # 彻底删除
        elif key == 'delCom':
            if self.file_dml.deleteComplete(now_path, name, df_type):
                return True
        # 移动到
        elif key == 'moveTo':
            if self.file_dml.update(now_path, name, df_type, to_path=info):
                return True
        # 复制到
        elif key == 'copyTo':
            if self.file_dml.copy(now_path, name, df_type, to_path=info):
                return True
        # 重命名
        elif key == 'rename':
            # if self.file_dml.rename(now_path, name, df_type, new_name=info):
            #     return True
            return True
        # 恢复, 还是不要放在一起吧
        elif key == 'recovery':
            if self.file_dml.recovery(name, df_type, delete_time=info):
                return True
        return False

    def addInfo(self, now_path, name, file_size, true_path, df_type, keep_time, hash_code, form_type):
        self.file_dml.insert(now_path,
                             name,
                             keep_time,
                             file_size,
                             true_path,
                             df_type,
                             hash_code,
                             '',
                             form_type)

    def getRealPath(self, now_path, name):
        return self.file_dml.queryTruePath(now_path, name)

    def checkConflict(self, name, df_type, to_path):
        to_path_name_tuple = self.file_dml.queryConflict(to_path)
        if (name, df_type) in to_path_name_tuple:
            return True
        else:
            return False

    def checkBeforeRecovery(self, name, df_type, delete_time):
        conflict_name = self.file_dml.queryRecoveryConflict(name, df_type, delete_time)
        return conflict_name

    def commit(self):
        self.file_dml.commit()


if __name__ == '__main__':
    deal = Deal()
    deal.setTable('test')
    print(deal.checkConflict('b.txt', 'D', '/A/B/'))