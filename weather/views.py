from django import forms
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView

from .models import City
from .form import CityForm
import requests


# Create your views here.
class HomeView(TemplateView):
    template_name='weather.html'
    form_class = CityForm

    def get(self, request, *args, **kwargs):
        city_query = City.objects.all()

        if 'pk' in kwargs:
            self.deleteItem(kwargs['pk'])
            return redirect('home')
        
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=c72533cac4916e2e44a2424d2c081ebd'

        weather_data = []

        for i in city_query:
            data = requests.get(url.format(i.city)).json()
            dataset = {
                'id': i.id,
                'city' : i,
                'temperature' : data['main']['temp'],
                'icon' : data['weather'][0]['icon']
            }
            weather_data.append(dataset)
        
        context = {
            'weather_data': weather_data,
            'form': CityForm()
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = self.form_class(request.POST)
        if form.is_valid:
            form.save()
            return redirect('/')
        return render(request, self.template_name, {'form': form})

    def deleteItem(self, pk):
        try:
            del_item = City.objects.get(pk=pk)
            del_item.delete()
        except:
            return;