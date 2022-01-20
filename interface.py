import os
os.environ["KIVY_NO_CONSOLELOG"] = "1"

import kivy
import kivymd
from kivy.app import App
from kivymd.app import MDApp
from kivy.clock import Clock
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.list import IconLeftWidget
from kivy.config import Config
import socket, struct
from aggregator import Aggregator
#graficos
import matplotlib.pyplot as plt
import numpy as np
from numpy import random as rd
from matplotlib import use as mpl_use
import matplotlib.animation as animation
from matplotlib import style

from kivy.garden.graph import SmoothLinePlot, Graph

Config.set('kivy','window_icon','icon.png')
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

# Clock.max_iteration = 5

def ipLongToString(value):
    return socket.inet_ntoa(struct.pack('!L', value))
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
        self.call_list = []
        Clock.schedule_interval(self.update,intervals)
    
    def update(self, *args):
        if App.currentPage != 'main':
            return
        for call in self.call_list:
            call()
    
    def add_item(self, parameters = {}):
        btn = IconItem()
        btn.start(parameters)
        self.add_widget(btn)
        self.call_list.append(btn.update)

class IconItem(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.button = ThreeLineListItem(text= '', secondary_text='0 B')

        self.button.bind(on_press=self.on_press)
        self.add_widget(self.button)
        self.bind(on_press=self.on_press)
        # Clock.schedule_interval(self.update,intervals)

    def update(self, *args):
        sizeText = ['B','KB','MB','GB','TB']
        accumulated = self.get_value()['accumulated']
        data = accumulated['number']
        size = accumulated['multiplier']
        while(data > 1000):
            data = data/1000
            size+=1

        self.button.secondary_text = str(round(data,1)) + ' ' + sizeText[size]
    
    def start(self, params):
        self.button.text = params['name']
        self.get_value = params['caller']
    
    def on_press(self, *args, **kwargs):
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


# class GeneralGraph(BoxLayout):
#     def __init__(self,**kwargs):
#         super().__init__(**kwargs)

#         #internas
#         self.graphType = 'direcional'
#         #grafico
#         self.fig, self.ax1 = plt.subplots()
#         self.ax1.plot([1,2,3],[1,2,3], label='a')
#         self.ax1.legend(loc='upper left')
#         self.fig.set_facecolor('white')
#         self.ax1.set_facecolor('white')
#         self.graphCanvas = self.fig.canvas
#         self.add_widget(self.graphCanvas)
#         Clock.schedule_interval(self.update,intervals)
        
#     def changeGraph(self,graph):
#         self.graphType = graph
#         self.update()

#     def fluxo(self):
#         ys = {
#             'total': aggr.values['total']['total']
#         }
#         for prog in aggr.values['programs']:
#             ys[prog] = aggr.values['programs'][prog]['total']['total']
        
#         return ys
    
#     def pacotes(self):
#         ys = {
#             'total': aggr.values['package']['total']
#         }
#         for prog in aggr.values['programs']:
#             ys[prog] = aggr.values['programs'][prog]['package']['total']
        
#         return ys

#     def direcional(self):
#         ys = {
#             'incoming': aggr.values['total']['incoming'],
#             'outgoing': aggr.values['total']['outgoing']
    #     }
    #     return ys


    # def update(self,*args):
    #     if App.currentPage != 'main':
    #         return
    #     graphTypes = {
    #         'fluxo': self.fluxo,
    #         'direcional': self.direcional,
    #         'pacotes': self.pacotes
    #     }
    #     ys = graphTypes[self.graphType]()
    #     keys = list(ys.keys())
    #     length = len(ys[keys[0]])
    #     xs = [i for i in range(length)]
    #     self.ax1.clear()
    #     current_color = 0
    #     for key in ys:
    #         if(length < len(ys[key])):
    #             diff = len(ys[key]) - length
    #             ys[key] = ys[key][: -diff]
            
    #         self.ax1.plot(xs,ys[key],label=key, color = pallete[current_color])        
    #         current_color+=1
        
    #     self.yValues = ys
    #     self.ax1.legend(loc='upper left')
    #     self.graphCanvas.draw_idle()



class GeneralGraph(BoxLayout):
    def __init__(self,**kwargs):
        
        super().__init__(**kwargs)
        self.rgb_pallete = [[rd.random(),rd.random(),rd.random()] for i in range(100)]
        self.my_graph = Graph(
        xlabel='Tempo',
        ylabel='Fluxo',
        y_ticks_major=100,
        y_grid_label=True,
        x_grid_label=True,
        padding=4,
        xlog=False,
        ylog=False,
        x_grid=True,
        y_grid=True,
        ymin=0,
        ymax=1000,
        xmax=60,
        )
        self.graphType = 'fluxo'

        self.add_widget(self.my_graph)
        Clock.schedule_interval(self.update,intervals)

    def changeGraph(self,graph):
        self.graphType = graph
        self.update()

    def fluxo(self):
        ys = {
            'total': aggr.values['total']['total']
        }
        for prog in aggr.values['programs']:
            ys[prog] = aggr.values['programs'][prog]['total']['total']
        
        return ys
    
    def pacotes(self):
        ys = {
            'total': aggr.values['package']['total']
        }
        for prog in aggr.values['programs']:
            ys[prog] = aggr.values['programs'][prog]['package']['total']
        
        return ys

    def direcional(self):
        ys = {
            'incoming': aggr.values['total']['incoming'],
            'outgoing': aggr.values['total']['outgoing']
        }
        return ys

    def update(self, *args):
        graphTypes = {
            'fluxo': self.fluxo,
            'direcional': self.direcional,
            'pacotes': self.pacotes
        }
        graphTypes = {
            'fluxo': self.fluxo,
            'direcional': self.direcional,
            'pacotes': self.pacotes
        }
        ys = graphTypes[self.graphType]()
        keys = list(ys.keys())
        length = len(ys[keys[0]])
        xs = list(range(length))
        current_color = 0

        for plot in self.my_graph.plots:
            self.my_graph.remove_plot(plot)
        max_value = 1
        for key in ys:
            plot = SmoothLinePlot(color=self.rgb_pallete[current_color])
            max_y = max(ys[key])
            max_value = max(max_value,max_y)
            current_color+=1
            plot.points = list(zip(xs,ys[key]))
            self.my_graph.add_plot(plot)
        
        self.my_graph.ymax = max_value
        


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
        self.call_list = []
        Clock.schedule_interval(self.update,intervals)

    def update(self, *args):
        if App.currentPage != 'specific':
            return
        for call in self.call_list:
            call()
    
    def add_item(self, parameters):
        btn = IconSpecificItem()
        btn.start(parameters)
        self.add_widget(btn)
        self.call_list.append(btn.update)
    
    def do_items(self):
        self.clear_widgets()
        self.call_list = []
        appName = App.specificName
        for conn in aggr.values['programs'][App.specificName]['connections']:
            def creator(conn_name):
                def caller():
                    return aggr.values['programs'][appName]['connections'][conn_name]
                return caller

            self.add_item({
                'name': ipLongToString(conn),
                'id': conn,
                'caller': creator(conn),
                'program': App.specificName
            })

class IconSpecificItem(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.button = ThreeLineListItem(text= '', secondary_text='0 B')
        self.add_widget(self.button)

    def update(self, *args):
        sizeText = ['B','KB','MB','GB','TB']
        data = self.get_value()
        accumulated = data['accumulated']
        data = accumulated['number']
        size = accumulated['multiplier']

        self.button.secondary_text = str(round(data,1)) + ' ' + sizeText[size]
    
    def start(self, params):
        self.button.text = params['name']
        self.id = params['id']
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
        self.graphType = 'direcional'
        #grafico
        self.fig, self.ax1 = plt.subplots()
        self.ax1.plot([1,2,3],[1,2,3])
        self.fig.set_facecolor('white')
        self.ax1.set_facecolor('white')
        self.graphCanvas = self.fig.canvas
        self.add_widget(self.graphCanvas)
        Clock.schedule_interval(self.update,intervals)
        
    def changeGraph(self,graph):
        self.graphType = graph
        self.update()

    def fluxo(self):
        ys = {
            'total': aggr.values['programs'][App.specificName]['total']['total']
        }
        current_color = 0
        for conn in aggr.values['programs'][App.specificName]['connections']:
            ip = int(conn)
            
            ys[ipLongToString(ip)] = aggr.values['programs'][App.specificName]['connections'][conn]['total']['total']
        
        return ys
    
    def pacotes(self):
        ys = {
            'total': aggr.values['programs'][App.specificName]['package']['total']
        }
        for conn in aggr.values['programs'][App.specificName]['connections']:
            ip = int(conn)
            ys[ipLongToString(ip)] = aggr.values['programs'][App.specificName]['connections'][conn]['package']['total']
        
        return ys
    def direcional(self):
        return {
            'incoming': aggr.values['programs'][App.specificName]['total']['incoming'],
            'outgoing': aggr.values['programs'][App.specificName]['total']['outgoing']
        }

    def update(self,*args):
        if App.currentPage != 'specific':
            return
        
        graphTypes = {
            'fluxo': self.fluxo,
            'pacotes': self.pacotes,
            'direcional': self.direcional,

        }
        ys = graphTypes[self.graphType]()
        keys = list(ys.keys())
        length = len(ys[keys[0]])
        xs = [i for i in range(length)]
        self.ax1.clear()
        current_color = 0
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
        self.title = 'Web Sniffer'
        self.icon = 'icon.png'
        self.load_kv('interface.kv')
        sc = ScreenManager()
        self.main = MainPageScreen(name='mainPage')
        self.specific = SpecificPageScreen(name='specificPage')
        sc.add_widget(self.main)
        sc.add_widget(self.specific)
        return sc

        

App = MainPageAPP()
App.run()

