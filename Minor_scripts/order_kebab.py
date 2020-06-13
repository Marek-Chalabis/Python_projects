# interface that let you order a kebab
from tkinter import *


class KebabOrder(Frame):
    cheese_price = 2
    salad_price = 1
    fries_price = 4
    kebab_price_basic = 12
        
    def __init__(self, master):
        super(KebabOrder, self).__init__(master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):

        Label(self, text="Create your own kebab using this interface").grid(column=0, row=0, columnspan=3, sticky=W)

        Label(self, text="How you want to call your kebab?",).grid(column=0, row=1, columnspan=3, sticky=W)
        self.kebab_name = Entry(self)
        self.kebab_name.grid(row=2, column=0, sticky=W)

        Label(self, text="Ciasto").grid(column=0, row=3, sticky=W)
        self.dough = StringVar()
        self.dough.set(None)
        dough_type = ["loaf", "Tortilla", "Falafel"]
        row = 4
        for dough in dough_type:
            Radiobutton(self,
                        text=dough,
                        variable=self.dough,
                        value=dough
                        ).grid(row=row, column=0, sticky=W)
            row += 1

        Label(self, text="Sos:").grid(column=1, row=3, sticky=W)
        self.sos = StringVar()
        self.sos.set(None)
        sos_type = ["mild", "Mixed", "Spicy"]
        row = 4
        for sos in sos_type:
            Radiobutton(self,
                        text=sos,
                        variable=self.sos,
                        value=sos
                        ).grid(row=row, column=1, sticky=W)
            row += 1

        Label(self, text="Meat:",
              ).grid(column=2, row=3, sticky=W)
        self.meat = StringVar()
        self.meat.set(None)
        meat_type = ["Mutton", "Chicken", "Mutton i Chicken"]
        row = 4
        for meat in meat_type:
            Radiobutton(self,
                        text=meat,
                        variable=self.meat,
                        value=meat
                        ).grid(row=row, column=2, sticky=W)
            row += 1

        Label(self, text="Additives:",
              ).grid(column=0, row=7, sticky=W)

        self.is_cheese = BooleanVar()
        Checkbutton(self,
                    text="cheese +" + str(KebabOrder.cheese_price) + "zł",
                    variable=self.is_cheese
                    ).grid(row=8, column=0, sticky=W)

        self.is_salad = BooleanVar()
        Checkbutton(self,
                    text="Salad +" + str(KebabOrder.salad_price) + "zł",
                    variable=self.is_salad
                    ).grid(row=9, column=0, sticky=W)

        self.is_fries = BooleanVar()
        Checkbutton(self,
                    text="Fries +" + str(KebabOrder.fries_price) + "zł",
                    variable=self.is_fries
                    ).grid(row=10, column=0, sticky=W)

        Button(self,
               text="Submit",
               command=self.order
               ).grid(row=11, column=0, sticky=W)

        self.orderText = Text(self, width=30, height=10, wrap=WORD)
        self.orderText.grid(row=7, column=1, columnspan=2, rowspan=5)

        Button(self,
               text="Submit order",
               command=self.price
               ).grid(row=12, column=1, sticky=W)

        self.priceText = Text(self, width=30, height=5, wrap=WORD)
        self.priceText.grid(row=13, column=0, columnspan=2, rowspan=2)

    def order(self):
        kebab_name = self.kebab_name.get()
        dough = self.dough.get()
        sos = self.sos.get()
        meat = self.meat.get()
        topics = ""
        if self.is_cheese.get():
            topics += "\n-Cheese"
        if self.is_salad.get():
            topics += "\n-Salad"
        if self.is_fries.get():
            topics += "\n-Fries"
        if topics == "":
            topics = "No topics"

        info = "Name of your kebab: "
        info += kebab_name
        info += "\nDough: "
        info += dough
        info += "\nSos: "
        info += sos
        info += "\nMeat: "
        info += meat
        info += "\nTopics:"
        info += topics

        self.orderText.delete(0.0, END)
        self.orderText.insert(0.0, info)

    def price(self):
        kebab_name = self.kebab_name.get()
        topics = 0
        if self.is_cheese.get():
            topics += KebabOrder.cheese_price
        if self.is_salad.get():
            topics += KebabOrder.salad_price
        if self.is_fries.get():
            topics += KebabOrder.fries_price
        price = topics + KebabOrder.kebab_price_basic
           
        info = "Topics cost: \n"
        info += kebab_name
        info += "Cost of kebab without topics:"
        info += str(KebabOrder.kebab_price_basic)
        info += "\nWith chosen topics:\n"
        info += str(price)

        self.priceText.delete(0.0, END)
        self.priceText.insert(0.0, info)
        

root= Tk()
root.title("Order kebab")
root.geometry("400x430")
show=KebabOrder(root)
root.mainloop()
