from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.clock import Clock # ऑटो-क्लिकरसाठी महत्त्वाचे

class AutoClickerMoneyApp(App):
    def build(self):
        self.money = 0
        self.money_per_click = 10
        self.auto_value = 0 # दर सेकंदाला वाढणारे पैसे
        self.upgrade_cost = 500
        self.auto_clicker_cost = 1000
        
        Window.clearcolor = (0.05, 0.05, 0.1, 1) # अजून डार्क प्रीमियम लुक
        
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        
        # डिस्प्ले लेबल
        self.money_label = Label(
            text=f"{self.money} RS",
            font_size='60sp',
            bold=True,
            color=(0.2, 1, 0.5, 1)
        )
        
        # १. मुख्य टॅप बटण
        self.click_btn = Button(
            text="TAP & EARN",
            size_hint=(1, 0.4),
            font_size='35sp',
            background_normal='',
            background_color=(0.1, 0.5, 0.8, 1)
        )
        self.click_btn.bind(on_press=self.add_money)
        
        # २. मॅन्युअल अपग्रेड (Double Money)
        self.upgrade_btn = Button(
            text=f"Double Power (Cost: {self.upgrade_cost})",
            size_hint=(1, 0.15),
            background_color=(0.7, 0.4, 0.1, 1)
        )
        self.upgrade_btn.bind(on_press=self.buy_upgrade)
        
        # ३. ऑटो-क्लिकर बटण
        self.auto_btn = Button(
            text=f"Buy Auto-Clicker (Cost: {self.auto_clicker_cost})\n(+10 RS Every Second)",
            size_hint=(1, 0.15),
            background_color=(0.4, 0.1, 0.6, 1)
        )
        self.auto_btn.bind(on_press=self.buy_auto_clicker)
        
        self.layout.add_widget(self.money_label)
        self.layout.add_widget(self.click_btn)
        self.layout.add_widget(self.upgrade_btn)
        self.layout.add_widget(self.auto_btn)
        
        # ऑटो-क्लिकर फंक्शन दर १ सेकंदाला चालवण्यासाठी सेटिंग
        Clock.schedule_interval(self.auto_update, 1)
        
        return self.layout

    def add_money(self, instance):
        self.money += self.money_per_click
        self.update_label()

    def buy_upgrade(self, instance):
        if self.money >= self.upgrade_cost:
            self.money -= self.upgrade_cost
            self.money_per_click *= 2
            self.upgrade_cost *= 2
            self.upgrade_btn.text = f"Double Power (Cost: {self.upgrade_cost})"
            self.update_label()

    def buy_auto_clicker(self, instance):
        if self.money >= self.auto_clicker_cost:
            self.money -= self.auto_clicker_cost
            self.auto_value += 10 # दर सेकंदाला १० रुपये वाढणार
            self.auto_clicker_cost *= 2
            self.auto_btn.text = f"Auto-Clicker (Cost: {self.auto_clicker_cost})\n(+10 RS/sec)"
            self.update_label()

    def auto_update(self, dt):
        # हे फंक्शन दर सेकंदाला आपोआप पैसे वाढवेल
        if self.auto_value > 0:
            self.money += self.auto_value
            self.update_label()

    def update_label(self):
        self.money_label.text = f"{self.money} RS"

AutoClickerMoneyApp().run()

import os
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.clock import Clock

class SaveMoneyApp(App):
    def build(self):
        # फाईलचे नाव जिथे पैसे सेव्ह होतील
        self.save_file = "gamedata.txt"
        
        # आधीचे सेव्ह केलेले पैसे लोड करणे
        self.load_data()
        
        self.money_per_click = 10
        self.auto_value = 0
        self.upgrade_cost = 500
        self.auto_clicker_cost = 1000
        
        Window.clearcolor = (0.05, 0.05, 0.1, 1)
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        
        self.money_label = Label(text=f"{self.money} RS", font_size='60sp', bold=True, color=(0.2, 1, 0.5, 1))
        
        self.click_btn = Button(text="TAP & EARN", size_hint=(1, 0.4), font_size='35sp', background_color=(0.1, 0.5, 0.8, 1))
        self.click_btn.bind(on_press=self.add_money)
        
        self.upgrade_btn = Button(text=f"Double Power (Cost: {self.upgrade_cost})", size_hint=(1, 0.15), background_color=(0.7, 0.4, 0.1, 1))
        self.upgrade_btn.bind(on_press=self.buy_upgrade)
        
        self.auto_btn = Button(text=f"Auto-Clicker (Cost: {self.auto_clicker_cost})", size_hint=(1, 0.15), background_color=(0.4, 0.1, 0.6, 1))
        self.auto_btn.bind(on_press=self.buy_auto_clicker)
        
        self.layout.add_widget(self.money_label)
        self.layout.add_widget(self.click_btn)
        self.layout.add_widget(self.upgrade_btn)
        self.layout.add_widget(self.auto_btn)
        
        Clock.schedule_interval(self.auto_update, 1)
        # दर ५ सेकंदाला आपोआप डेटा सेव्ह करण्यासाठी
        Clock.schedule_interval(self.save_data, 5)
        
        return self.layout

    def add_money(self, instance):
        self.money += self.money_per_click
        self.update_label()

    def buy_upgrade(self, instance):
        if self.money >= self.upgrade_cost:
            self.money -= self.upgrade_cost
            self.money_per_click *= 2
            self.upgrade_cost *= 2
            self.upgrade_btn.text = f"Double Power (Cost: {self.upgrade_cost})"
            self.save_data()
            self.update_label()

    def buy_auto_clicker(self, instance):
        if self.money >= self.auto_clicker_cost:
            self.money -= self.auto_clicker_cost
            self.auto_value += 10
            self.auto_clicker_cost *= 2
            self.auto_btn.text = f"Auto-Clicker (Cost: {self.auto_clicker_cost})"
            self.save_data()
            self.update_label()

    def auto_update(self, dt):
        if self.auto_value > 0:
            self.money += self.auto_value
            self.update_label()

    def update_label(self):
        self.money_label.text = f"{self.money} RS"

    def save_data(self, *args):
        # पैसे फाईलमध्ये लिहून ठेवणे
        with open(self.save_file, "w") as f:
            f.write(str(self.money))

    def load_data(self):
        # फाईलवरून जुने पैसे वाचणे
        if os.path.exists(self.save_file):
            with open(self.save_file, "r") as f:
                self.money = int(f.read())
        else:
            self.money = 0

SaveMoneyApp().run()

import os
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.clock import Clock

class MillionaireApp(App):
    def build(self):
        # फाईल जिथे पैसे सेव्ह होतील
        self.save_file = "money_data.txt"
        
        # आधीचे पैसे लोड करणे
        self.load_data()
        
        self.money_per_click = 10
        self.auto_value = 0
        self.upgrade_cost = 500
        self.auto_cost = 1000
        
        Window.clearcolor = (0.05, 0.05, 0.1, 1)
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        
        self.money_label = Label(text=f"{self.money} RS", font_size='60sp', bold=True, color=(0.2, 1, 0.5, 1))
        
        self.click_btn = Button(text="TAP TO EARN", size_hint=(1, 0.4), font_size='30sp', background_color=(0.1, 0.5, 0.8, 1))
        self.click_btn.bind(on_press=self.add_money)
        
        self.upgrade_btn = Button(text=f"Double Power ({self.upgrade_cost} RS)", size_hint=(1, 0.15), background_color=(0.7, 0.4, 0.1, 1))
        self.upgrade_btn.bind(on_press=self.buy_upgrade)
        
        self.auto_btn = Button(text=f"Auto-Clicker ({self.auto_cost} RS)", size_hint=(1, 0.15), background_color=(0.4, 0.1, 0.6, 1))
        self.auto_btn.bind(on_press=self.buy_auto)
        
        self.layout.add_widget(self.money_label)
        self.layout.add_widget(self.click_btn)
        self.layout.add_widget(self.upgrade_btn)
        self.layout.add_widget(self.auto_btn)
        
        # ऑटो-क्लिकर आणि ऑटो-सेव्ह चं टायमिंग
        Clock.schedule_interval(self.auto_update, 1)
        Clock.schedule_interval(self.save_data, 10) # दर १० सेकंदाला आपोआप सेव्ह होईल
        
        return self.layout

    def add_money(self, instance):
        self.money += self.money_per_click
        self.money_label.text = f"{self.money} RS"

    def buy_upgrade(self, instance):
        if self.money >= self.upgrade_cost:
            self.money -= self.upgrade_cost
            self.money_per_click *= 2
            self.upgrade_cost *= 2
            self.upgrade_btn.text = f"Double Power ({self.upgrade_cost} RS)"
            self.save_data()
            self.money_label.text = f"{self.money} RS"

    def buy_auto(self, instance):
        if self.money >= self.auto_cost:
            self.money -= self.auto_cost
            self.auto_value += 10
            self.auto_cost *= 2
            self.auto_btn.text = f"Auto-Clicker ({self.auto_cost} RS)"
            self.save_data()
            self.money_label.text = f"{self.money} RS"

    def auto_update(self, dt):
        if self.auto_value > 0:
            self.money += self.auto_value
            self.money_label.text = f"{self.money} RS"

    def save_data(self, *args):
        with open(self.save_file, "w") as f:
            f.write(str(self.money))

    def load_data(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, "r") as f:
                content = f.read()
                self.money = int(content) if content else 0
        else:
            self.money = 0

MillionaireApp().run()