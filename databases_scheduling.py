from apscheduler.schedulers.blocking import BlockingScheduler
from dboperations.mongooperations import MongoOperations
from feed_preparation.Feed_Formation import feed_formation


sched = BlockingScheduler()
mongo = MongoOperations('everything')
feed = feed_formation()


@sched.scheduled_job('interval', minutes=29)
def callTrending():        
    mongo.insertTrending()



@sched.scheduled_job('interval', minutes=67)
def callHeadlines():   
    mongo.insertHeadlines()
    #logging.info('API for Headlines called at : ')


@sched.scheduled_job('interval', minutes=70)
def callTopNews():
    mongo.insertTopNews()
    #logging.info('API for Top news called at : ')


@sched.scheduled_job('interval', minutes=93)
def callFeed():
    feed.feed_prepare()
    #logging.info('API for Everything called at : ')
    

@sched.scheduled_job('interval', minutes=180)
def callEverything():
    mongo.insertEverything()
    #logging.info('API for Everything called at : ')
    
    
sched.start()