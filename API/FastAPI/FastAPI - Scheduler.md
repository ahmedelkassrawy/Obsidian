In the api py file.
```python
scheduler = BackgroundScheduler()
scheduler.add_job(run_eval,"interval",minutes = 60)
scheduler.add_job(dashboard.change_data,"interval",days = 60)
scheduler.start()
```