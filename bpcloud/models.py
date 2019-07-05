from django.db import models
# Create your models here.


class HashFiles(models.Model):
    # 主键
    # virtual_path = models.CharField('文件虚拟地址', max_length=256)
    # df_type = models.CharField('类型', max_length=256)
    # name = models.CharField('文件名', max_length=256)
    size = models.CharField('文件大小', max_length=256)
    # change_time = models.CharField('文件修改日期', max_length=256)
    hash_code = models.CharField('文件哈希', max_length=32, primary_key=True)
    # form_type = models.CharField('文件类型', max_length=256)
    true_path = models.FileField('文件路径', upload_to='storage/')