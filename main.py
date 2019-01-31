import kivy.app
import kivy.uix.boxlayout
import kivy.uix.textinput
import kivy.uix.label
import kivy.uix.button
from kivy.uix.image import Image

import app
import cv2

class SimpleApp(kivy.app.App):

    def build(self):
        self.title = "Car Number Plate Detector"
        self.i = 1
        self.j = 1
        self.textInput = kivy.uix.textinput.TextInput(size_hint=(1, None),height=30,multiline=False)
        self.start_button = kivy.uix.button.Button(text="next",pos=(200, 200),size_hint = (1,.1))
        self.choose_button = kivy.uix.button.Button(text="choose from directory (fill path below)",pos=(500, 500),size_hint = (1,.1))
        self.image = Image(source="Output/plates/" + str(self.i) + "/" + str(self.j) + ".jpg")
        self.start_button.bind(on_press=self.start_callback)
        self.choose_button.bind(on_press=self.custome_callback)
        self.boxLayout = kivy.uix.boxlayout.BoxLayout(orientation="vertical")
        self.boxLayout.add_widget(self.start_button)
        self.boxLayout.add_widget(self.choose_button)
        self.boxLayout.add_widget(self.textInput)
        self.boxLayout.add_widget(self.image)
        return self.boxLayout

    def start_callback(self, btn):
        # app.run()
        self.iterate()
        img_test = cv2.imread("Output/plates/" + str(self.i) + "/" + str(self.j) + ".jpg")
        if img_test is None:
            self.iterate()
        print(self.i, self.j)
        self.image.source = "Output/plates/" + str(self.i) + "/" + str(self.j) + ".jpg"

    def custome_callback(self, btn):
        src = app.run(self.textInput.text)
        self.image.source = "custom.jpg"

    def iterate(self):
        if (self.i == 1 ):
            if (self.j > 31):
                self.i = self.i + 1
                self.j = 1
            else:
                self.j = self.j + 1
        if (self.i == 2 ):
            if (self.j > 124):
                self.i = 0
                self.j = 0
            else:
                self.j = self.j + 1
        img_test = cv2.imread("Output/plates/" + str(self.i) + "/" + str(self.j) + ".jpg")
        if img_test is None:
            self.iterate()


if __name__ == "__main__":
    simpleApp = SimpleApp()
    simpleApp.run()
