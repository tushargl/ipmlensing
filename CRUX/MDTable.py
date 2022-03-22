from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.label import MDLabel
from kivy.uix.button import Button
from kivy.properties import NumericProperty, ListProperty,StringProperty
from kivy.graphics import Color
from kivy.metrics import dp

Builder.load_string('''
#:import MDLabel kivymd.label.MDLabel
<Table>
    orientation:'vertical'  
    size_hint_y:0.9
    GridLayout:
        id:header
        spacing:2
        padding:[10,10,10,10]
        size_hint_y:None
        height:dp(48)
    ScrollView:
        size_hint_y:1       
        GridLayout:
            id:body
            spacing:2
            padding:[10,10,10,10]
            size_hint_y:None
            #spacing:dp(2)
            height:self.minimum_height

    # GridLayout:
    #     id:footer
    #     height:dp(48)
    #     pos_hint:{'center_y':0.1}

<Header>
    padding:[10,10,10,10]
    canvas.before:
        Color:
            rgba: app.theme_cls.accent_dark
        Rectangle:
            pos: self.pos
            size: self.size
    size_hint_y:None
    size_hint_x:header.size_hint_x
    height:dp(48)
    MDLabel:
        id:header
        text:root.text
<Cell>
    padding:[10,10,10,10]
    canvas.before:
        Color:
            rgba: app.theme_cls.accent_color
        Rectangle:
            pos: self.pos
            size: self.size
    size_hint_y:None
    size_hint_x:cell.size_hint_x
    height:dp(48)
    MDLabel:
        id:cell
        text:root.text               
''')

class Header(BoxLayout):
    text = StringProperty()



class Cell(BoxLayout):
    text = StringProperty()




class Table(BoxLayout):
    cols = NumericProperty(1)
    table_content = ListProperty([{"col 1":"row 11","col 2":"row 21"},{"col 1":"row 12","col 2":"row 22"}],allownone=True)
    thead = ListProperty()
    tbody = ListProperty()
    color = [128, 0, 2, 0.8]



    def __init__(self, **kwargs):
        super(Table, self).__init__(**kwargs)

        for i in self.table_content:
            self.thead =[]
            for j in i.keys():
                self.thead.append(j)
        self.ids['header'].cols = len(self.thead)
        self.ids['body'].cols = len(self.thead)
        for i in self.thead:
            head = Header(text=i.upper())
            self.ids['header'].add_widget(head)
        for i in self.table_content:
            for j in i.keys():
                body = Cell(text=i[j])
                self.ids['body'].add_widget(body)
