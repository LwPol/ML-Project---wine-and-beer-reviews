import tkinter as tk
from recognize import recognize, read_file
import json

class_mapping = json.loads(read_file('class_mapping.json'))

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.review = tk.Text(self, height=10, width=70)
        self.review.pack(fill=tk.X, pady=10)
        self.button = tk.Button(self)
        self.button['text'] = 'Predict'
        self.button['command'] = self.predict
        self.button.pack(pady=15)
        self.label = tk.Label(self)
        self.label.pack()

    def predict(self):
        prediction = recognize(self.review.get('1.0', 'end-1c'))
        self.label['text'] = f"{prediction} ({class_mapping[prediction]})"

root = tk.Tk()
root.title('We <3 wines and beers')
root.geometry('640x350')
app = Application(master=root)
app.mainloop()