import MySQLdb
import datetime
from celery import Celery
from celery import signals
app = Celery('mtn_tasks', broker='amqp://guest@localhost//')
db = MySQLdb.connect("127.0.0.1", "root", "13610522")



@app.task
def update_subscribe(subscriber, service_id, subscribed, status, shortcode):

    cursor = db.cursor()
    cursor.execute('''select idservices,mtn_id,name_slug,db_name from mtn_services.services where mtn_id=%s;''' % service_id)
    result = cursor.fetchone()
    str_sql = "update %s.mtn_service set is_enable=%s, date_modify=NOw() where subscriber = '%s';" % (result[2], subscribed, subscriber)
    update_selected_table.delay(result[2], str_sql)
    db.commit()
    # db.close()


@app.task()
def update_selected_table(db_name, string_sql):
    # db = MySQLdb.connect("127.0.0.1", "root", "13610522")
    cursor = db.cursor()
    result = cursor.execute(string_sql)
    WriteToFile.delay(db_name, string_sql)
    db.commit()
    # db.close()


@app.task
def WriteToFile(subscriber, Result):
    f = open('Log/myfile.out', 'a')
    f.write('update DataBase with name: %s Successfull:{%s} at :%s\n' % (
        subscriber, Result, datetime.datetime.now()))
    f.close()

