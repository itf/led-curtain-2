import requests
import time
try:
    import LocalConfig as Config
except:
    import Config


api= Config.openWeather.api
cityID=Config.openWeather.cityID

def timeCache(timeMinutes):
    cacheContainer=[None]
    previousTimeContainer=[time.time()]
    def cacheFunction(function):
        def cachedFunction(*args):
            if (cacheContainer[0]) and (previousTimeContainer[0]+timeMinutes*60 > time.time()):
                return cacheContainer[0]
            else:
                try:
                    result = function(*args)
                except:
                    result=cacheContainer[0]
                cacheContainer[0]=result
                previousTimeContainer[0]=time.time()
                return result
        return cachedFunction
    return cacheFunction

@timeCache(10)
def getOpenWeatherRequest():
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?id='+cityID+'&APPID='+api)
    return r.json()

def getTempNow():
    r=getOpenWeatherRequest()
    tKelvin=r['main']['temp']
    return round(tKelvin-273.15,2)

def getTempNowF():
    r=getOpenWeatherRequest()
    tKelvin=r['main']['temp']
    return round((tKelvin-273.15)*9/5.+32,2)
    
def getTempMax():
    r=getOpenWeatherRequest()
    tKelvin=r['main']['temp_max']
    return tKelvin-273.15

def getTempMin():
    r=getOpenWeatherRequest()
    tKelvin=r['main']['temp_min']
    return tKelvin-273.15

def getWeather():
    r=getOpenWeatherRequest()
    return r['weather'][0]['description']
