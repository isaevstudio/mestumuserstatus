import peewee as pw
from userstatus import pg_db


pg_db.connect()

class UserInfo(pw.Model):
    id = pw.PrimaryKeyField()
    first_name = pw.CharField(max_length=100, null=False)
    last_name = pw.CharField(max_length=100, null=False)
    email = pw.CharField(max_length=100, null=False)
    phone_num = pw.CharField(max_length=100, null=False)

    class Meta:
        database = pg_db

class StreamingStatus(pw.Model):
    id = pw.PrimaryKeyField()
    user_id = pw.ForeignKeyField(UserInfo, backref='StreamingStatus', null=False)
    streaming = pw.CharField(max_length=100, null=False)
    time = pw.DateTimeField(null=False)
    status = pw.IntegerField(null=False)

    class Meta:
        database = pg_db

if __name__ == '__main__':
    UserInfo.create_table()
    StreamingStatus.create_table()