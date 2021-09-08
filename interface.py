import kivy
import kivymd
from kivy.app import App
from kivymd.app import MDApp
from kivy.clock import Clock
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.list import IconLeftWidget

from aggregator import Aggregator
#graficos
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import use as mpl_use
import matplotlib.animation as animation
from matplotlib import style

mpl_use('module://kivy.garden.matplotlib.backend_kivy')
style.use('fivethirtyeight')
intervals = 1
aggr = Aggregator(intervals)
#Componentes
from kivy.uix.button import Button 

#Layouts
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView

#Screen
from kivy.uix.screenmanager import ScreenManager, Screen

pallete = open('pallete.txt').read().split('\n')[:-1]

Clock.max_iteration = 5
class InitialPage(BoxLayout):
    pass

class TableAndGraph(BoxLayout):
    pass

class MenuLine(BoxLayout):
    pass

class TableView(ScrollView):
    pass

class GraphAndButtons(BoxLayout):
    pass


class Table(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def add_item(self, parameters = {}):
        btn = IconItem()
        btn.start(parameters)
        self.add_widget(btn)
        

class IconItem(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.button = ThreeLineListItem(text= '', secondary_text='0 B/s')

        self.button.bind(on_press=self.on_press)
        self.add_widget(self.button)
        self.bind(on_press=self.on_press)
        Clock.schedule_interval(self.update,intervals)

    def update(self, *args):
        if App.currentPage != 'main':
            return
        sizeText = ['B','KB','MB','GB','TB']
        data = self.get_value()['total']['total'][-1]
        size = 0
        while(data > 1000):
            data = data/1000
            size+=1

        self.button.secondary_text = str(round(data,1)) + ' ' + sizeText[size] + '/s'
    
    def start(self, params):
        self.button.text = params['name']
        self.get_value = params['caller']
    
    def on_press(self, *args, **kwargs):
        print('entrou on_press')
        App.main.changePage(self.button.text)

    
class DownloadBullet(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.listItem = ThreeLineListItem(text='0',secondary_text='KB/s')
        icon = IconLeftWidget(icon='download',user_font_size='40sp',size=(200,200))
        self.add_widget(icon)
        self.add_widget(self.listItem)
        Clock.schedule_interval(self.update,intervals)
  
    def update(self,*args):
        if App.currentPage != 'main':
            return
        sizeText = ['B','KB','MB','GB','TB']
        data = aggr.values['total']['incoming'][-1]
        data = int(data)
        size = 0
        while(data > 1000):
            data = data/1000
            size+=1
        self.listItem.text = str(int(data))
        self.listItem.secondary_text = sizeText[size] + '/s'


class UploadBullet(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.listItem = ThreeLineListItem(text='20',secondary_text='KB/s')
        icon = IconLeftWidget(icon='upload',user_font_size='40sp',size=(200,200))
        self.add_widget(icon)      
        self.add_widget(self.listItem)
        Clock.schedule_interval(self.update,intervals)
    
    def update(self,*args):
        if App.currentPage != 'main':
            return
        sizeText = ['B','KB','MB','GB','TB']
        data = aggr.values['total']['outgoing'][-1]
        data = int(data)
        size = 0
        while(data > 1000):
            data = data/1000
            size+=1
        self.listItem.text = str(int(data))
        self.listItem.secondary_text = sizeText[size] + '/s'


class GeneralGraph(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        #internas
        self.graphType = 'Fluxo'
        #grafico
        self.fig, self.ax1 = plt.subplots()
        self.ax1.plot([1,2,3],[1,2,3], label='a')
        self.ax1.legend(loc='upper left')
        self.graphCanvas = self.fig.canvas
        self.add_widget(self.graphCanvas)
        Clock.schedule_interval(self.update,intervals)
        
    def changeGraph(self,**kwargs):
        self.graphType = kwargs['graph']
        self.update()

    def update(self,*args):
        if App.currentPage != 'main':
            return
        ys = {
            'total': aggr.values['total']['total']
        }
        current_color = 0
        for prog in aggr.values['programs']:
            ys[prog] = aggr.values['programs'][prog]['total']['total']
        
        length = len(ys['total'])
        xs = [i for i in range(length)]
        self.ax1.clear()
        for key in ys:
            if(length < len(ys[key])):
                diff = len(ys[key]) - length
                ys[key] = ys[key][: -diff]
            
            self.ax1.plot(xs,ys[key],label=key, color = pallete[current_color])        
            current_color+=1
        
        self.yValues = ys
        self.ax1.legend(loc='upper left')
        self.graphCanvas.draw_idle()


class ButtonLine(BoxLayout):
    pass


class DownloadSpecificBullet(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.listItem = ThreeLineListItem(text='0',secondary_text='KB/s')
        icon = IconLeftWidget(icon='download',user_font_size='40sp',size=(200,200))
        self.add_widget(icon)
        self.add_widget(self.listItem)
        Clock.schedule_interval(self.update,intervals)
  
    def update(self,*args):
        if App.currentPage != 'specific':
            return 

        if App.specificName == '':
            return 0

        sizeText = ['B','KB','MB','GB','TB']
        data = aggr.values['programs'][App.specificName]['total']['incoming'][-1]
        size = 0
        while(data > 1000):
            data = data/1000
            size+=1
        self.listItem.text = str(int(data))
        self.listItem.secondary_text = sizeText[size] + '/s'

class SpecificTable(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def add_item(self, parameters):
        btn = IconSpecificItem()
        btn.start(parameters)
        self.add_widget(btn)
    
    def do_items(self):
        self.clear_widgets()
        
        for conn in aggr.values['programs'][App.specificName]['connections']:
            def caller():
                return aggr.values['programs'][App.specificName]['connections']

            self.add_item({
                'name': str(conn),
                'caller': caller
            })

class IconSpecificItem(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.button = ThreeLineListItem(text= '', secondary_text='0 B/s')
        self.add_widget(self.button)
        Clock.schedule_interval(self.update,intervals)

    def update(self, *args):
        if App.currentPage != 'specific':
            return
        sizeText = ['B','KB','MB','GB','TB']
        data = self.get_value()
        if int(self.button.text) not in data:
            return
        data = data[int(self.button.text)]['total']['total'][-1]
        size = 0
        while(data > 1000):
            data = data/1000
            size+=1

        self.button.secondary_text = str(round(data,1)) + ' ' + sizeText[size] + '/s'
    
    def start(self, params):
        self.button.text = params['name']
        self.get_value = params['caller']
    
  

class UploadSpecificBullet(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.listItem = ThreeLineListItem(text='20',secondary_text='KB/s')
        icon = IconLeftWidget(icon='upload',user_font_size='40sp',size=(200,200))
        self.add_widget(icon)      
        self.add_widget(self.listItem)
        Clock.schedule_interval(self.update,intervals)
    
    def update(self,*args):
        if App.currentPage != 'specific':
            return 
        if App.specificName == '':
            return 0

        sizeText = ['B','KB','MB','GB','TB']
        data = aggr.values['programs'][App.specificName]['total']['outgoing'][-1]
        size = 0
        while(data > 1000):
            data = data/1000
            size+=1
        self.listItem.text = str(int(data))
        self.listItem.secondary_text = sizeText[size] + '/s'


class SpecificGraph(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        #internas
        self.graphType = 'Fluxo'
        #grafico
        self.fig, self.ax1 = plt.subplots()
        self.ax1.plot([1,2,3],[1,2,3])
        self.graphCanvas = self.fig.canvas
        self.add_widget(self.graphCanvas)
        Clock.schedule_interval(self.update,intervals)
        
    def changeGraph(self,**kwargs):
        self.graphType = kwargs['graph']
        self.update()

    def update(self,*args):
        if App.currentPage != 'specific':
            return
        ys = {
            'total': aggr.values['programs'][App.specificName]['total']['total']
        }
        current_color = 0
        for conn in aggr.values['programs'][App.specificName]['connections']:
            ip = int(conn)
            ip_name = ''
            while(ip > 1000):
                ip_name = '.'  + str(int(ip%1000)) + ip_name
                ip = int(ip/1000)
            ip_name = str(ip) + ip_name
            ys[ip_name] = aggr.values['programs'][App.specificName]['connections'][conn]['total']['total']
        
        length = len(ys['total'])
        xs = [i for i in range(length)]
        self.ax1.clear()
        for key in ys:
            if(length < len(ys[key])):
                diff = len(ys[key]) - length
                ys[key] = ys[key][: -diff]
            
            if(current_color < len(pallete)):
                self.ax1.plot(xs,ys[key],label=key, color = pallete[current_color])  
                current_color+=1      
            else:
                self.ax1.plot(xs,ys[key],label=key) 
        
        self.yValues = ys
        self.ax1.legend(loc='upper left')
        self.graphCanvas.draw_idle()
    

        

#Screens
class MainPageScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        aggr.define_function({'new_program': self.add_program})
        aggr.start()
    
    def changePage(self,prog):
        App.specificName = prog
        App.currentPage = 'specific'
        self.manager.transition.direction = 'left'
        self.manager.current = 'specificPage'
        
    
    def add_program(self, obj):
        self.ids['gen_table'].add_item(obj)


class SpecificPageScreen(Screen):
    def on_pre_enter(self, **kwargs):
        self.ids.spec_table.do_items()

    def changePage(self,**kwargs):
        App.currentPage = 'main'
        self.manager.transition.direction = 'right'
        self.manager.current = 'mainPage'











class MainPageAPP(MDApp):
    specificName = ''
    currentPage = 'main'
    def build(self, **kwargs):
        self.load_kv('interface.kv')
        sc = ScreenManager()
        self.main = MainPageScreen(name='mainPage')
        self.specific = SpecificPageScreen(name='specificPage')
        sc.add_widget(self.main)
        sc.add_widget(self.specific)
        return sc

        

App = MainPageAPP()
App.run()

