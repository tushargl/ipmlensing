import os
import kivy
kivy.require('1.0.6')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.button import Button
from time import time
from kivy.app import App
from os.path import dirname, join
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen

from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior


import pandas as pd
chunksize = 10 ** 8


STAR_DATAFRAME = None



def print_full(x):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 2000)
    pd.set_option('display.float_format', '{:20,.2f}'.format)
    pd.set_option('display.max_colwidth', None)
    print(x)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
    pd.reset_option('display.width')
    pd.reset_option('display.float_format')
    pd.reset_option('display.max_colwidth')



class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class ErrorDialog(FloatLayout):
    okay = ObjectProperty(None)



class TextInputPopup(Popup):
    obj = ObjectProperty(None)
    obj_text = StringProperty("")

    def __init__(self, obj, **kwargs):
        super(TextInputPopup, self).__init__(**kwargs)
        self.obj = obj
        self.obj_text = obj.text


class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
                                  RecycleGridLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableButton(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Button '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(rv, index, data)

    # def on_touch_down(self, touch):
    #     ''' Add selection on touch down '''
    #     if super(SelectableButton, self).on_touch_down(touch):
    #         return True
    #     if self.collide_point(*touch.pos) and self.selectable:
    #         return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected

    # def on_press(self):
    #     popup = TextInputPopup(self)
    #     popup.open()

    # def update_changes(self, txt):
    #     self.text = txt

Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)
Factory.register('ErrorDialog', cls=ErrorDialog)
Factory.register('SelectableRecycleGridLayout', cls=SelectableRecycleGridLayout)





class CruxScreen(Screen):
    fullscreen = BooleanProperty(False)
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    data_items = ListProperty([])
    n_cols = NumericProperty()
    n_items = NumericProperty()
    n_rows = NumericProperty()
    column_names = ListProperty([])

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_error(self):
        content = ErrorDialog(okay=self.dismiss_popup)

        self._popup = Popup(title="CRUX ERROR", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        self.dismiss_popup()
        selected_file = os.path.join(path, filename[0])
        print("/CRUX/LOG> LOADING FILE:",selected_file)


        if not selected_file.lower().endswith(('.csv', '.CSV')):
            # self.dismiss_popup()
            self.show_error()
            # return
            pass
        else:
            row_df = pd.read_csv(selected_file, header=None)
            print("/CRUX/LOG> LOADED DATAFRAME:",row_df)
            self.n_cols = row_df.shape[1]
            self.n_rows = row_df.shape[0]
            print("/CRUX/LOG> LOADED DATAFRAME SHAPE:",row_df.shape)
            # vals = row_df.values.tolist()
            # print(vals)
            # self.add_table(self,vals)
            STAR_DATAFRAME = row_df


    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.text_input.text)

        self.dismiss_popup()

    def add_widget(self, *args, **kwargs):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args, **kwargs)
        return super(CruxScreen, self).add_widget(*args, **kwargs)




class CruxApp(App):


    index = NumericProperty(-1)
    current_title = StringProperty()
    time = NumericProperty(0)
    show_sourcecode = BooleanProperty(False)
    sourcecode = StringProperty()
    screen_names = ListProperty([])
    hierarchy = ListProperty([])




    def build(self):
        self.title = 'Crux Astrometry Software v0.0.3'
        Clock.schedule_interval(self._update_clock, 1 / 60.)
        self.screens = {}
        self.available_screens = sorted([
        	'Data',
        	'LensingEvents',
        	'Filter'
       	])
        self.screen_names = self.available_screens
        curdir = dirname(__file__)
        self.available_screens = [join(curdir, 'data', 'screens',
            '{}.kv'.format(fn).lower()) for fn in self.available_screens]
        self.go_next_screen()
    def go_next_screen(self):
        self.index = (self.index + 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='left')
        self.current_title = screen.name
        self.update_sourcecode()

    def update_sourcecode(self):
        if not self.show_sourcecode:
            self.root.ids.sourcecode.focus = False
            return
        self.root.ids.sourcecode.text = self.read_sourcecode()
        self.root.ids.sv.scroll_y = 1

    def read_sourcecode(self):
        fn = self.available_screens[self.index]
        with open(fn) as fd:
            return fd.read()
    def _update_clock(self, dt):
        self.time = time()
    def load_screen(self, index):
        if index in self.screens:
            return self.screens[index]
        screen = Builder.load_file(self.available_screens[index])
        self.screens[index] = screen
        return screen

    def go_previous_screen(self):
        self.index = (self.index - 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='right')
        self.current_title = screen.name
        self.update_sourcecode()

    def go_next_screen(self):
        self.index = (self.index + 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='left')
        self.current_title = screen.name
        self.update_sourcecode()

    def go_screen(self, idx):
        self.index = idx
        self.root.ids.sm.switch_to(self.load_screen(idx), direction='left')
        self.update_sourcecode()

    def go_hierarchy_previous(self):
        ahr = self.hierarchy
        if len(ahr) == 1:
            return
        if ahr:
            ahr.pop()
        if ahr:
            idx = ahr.pop()
            self.go_screen(idx)
            
    def toggle_source_code(self):
        self.show_sourcecode = not self.show_sourcecode
        if self.show_sourcecode:
            height = self.root.height * .3
        else:
            height = 0

        Animation(height=height, d=.3, t='out_quart').start(
                self.root.ids.sv)

        self.update_sourcecode()

if __name__ == '__main__':
    CruxApp().run()
