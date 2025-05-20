from django.shortcuts import render
from datetime import datetime

# Create your views here.
def index(request):
    mon = datetime.now().month
    day = datetime.now().day
    ans = "No"
    if day==1 and mon==1:
        ans="Yes"

    return render(request, 'newyear/index.html', {
        'ans' :ans
    })