from datetime import timedelta
from django.utils import timezone
from django.db.models import Avg, Max
from temp.models import History, Entry
#import temp.views
#import django

def update_avg(self, start, end):
        entries_for_period = Entry.objects.filter(time__gte=start, time__lte=end)
        avg_values = ['shedcur', 'outscur', 'gpuavg']
        average_value = entries_for_period.aggregate(*[Avg(x) for x in avg_values])
        return {x:average_value['%s__avg' % x] for x in avg_values}



def update_high(self, start, end):
        entries_for_period2 = Entry.objects.filter(time__gte=start, time__lte=end)
        high_values = ['shedcur', 'outscur', 'gpuhigh']
        high_value = entries_for_period2.aggregate(*[Max(x) for x in high_values])
        return {x:high_value['%s__max' % x] for x in high_values}


current_day = timezone.now()    
previous_day = current_day - timedelta(hours=24)
date_entry = previous_day.date()

avg_choice = update_avg(date_entry,previous_day,current_day)
high_choice = update_high(date_entry,previous_day,current_day)


history = History(date=date_entry, avgshed=round(avg_choice['shedcur'],2),highshed=round(high_choice['shedcur'],2),avgouts=round(avg_choice['outscur'],2),highouts=high_choice['outscur'],avggpu=avg_choice['gpuavg'],highgpu=high_choice['gpuhigh'],starttime=previous_day,endtime=current_day)
history.save()
