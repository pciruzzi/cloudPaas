from django_cron import CronJobBase, Schedule
from containers.models import Container
from django.contrib.auth.models import User

class Monitoring(CronJobBase):
	RUN_EVERY_MINS = 0

	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
	code = 'cron.Monitoring'    # a unique code

	def do(self):
		message = 'Active users: %d' % User.objects.count()
		print(message)
		print("in the cron job")    # do your thing here