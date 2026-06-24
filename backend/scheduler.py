from apscheduler.schedulers.blocking import BlockingScheduler

from ingest_news import main

print("Running initial ingestion...")
main()

scheduler = BlockingScheduler()


scheduler.add_job(
    main,
    trigger="interval",
    minutes=30,
)

print("Scheduler started. Running news ingestion every 30 minutes.")


scheduler.start()