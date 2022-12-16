
# ------------------------------------------------- Imports ------------------------------------------------------------

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import messagebox as mbox
from yahoo_fin.stock_info import tickers_sp500
from PIL import Image
import threading
import customtkinter as ctk
import tech
import beta
import funda
import settings
import sqlite3
import hashlib

# ------------------------------------------------- Main Frame ---------------------------------------------------------


# Creating Main Frame to handle all frames
class Windows(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)

        self.title(settings.TITLE)
        self.geometry(settings.GEOMETRY)
        self.resizable(False, False)

        container = ctk.CTkFrame(self, width=settings.CONTAINER_WIDTH, height=settings.CONTAINER_HEIGHT)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        # Create a dictionary of frames
        self.frames = {}
        # Create the frames and add to a dictionary.
        for F in (SignUpPage, App, LoginPage):
            frame = F(parent=container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        # Using a method to switch frames
        self.show_frame(LoginPage)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

# ------------------------------------------------ Login Page ----------------------------------------------------------


# Creating Login Page Frame
class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.bg_image = ctk.CTkImage(Image.open("assets/bg_gradient.jpg"), size=(900, 500))
        self.bg_image_label = ctk.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)
        self.login_frame = ctk.CTkFrame(self, corner_radius=settings.CORNER_RADIUS)
        self.login_frame.grid(row=0, column=0, sticky="ns")
        self.login_label = ctk.CTkLabel(self.login_frame, text="Logga in", font=ctk.CTkFont(size=20, weight="bold"))
        self.login_label.grid(row=0, column=0, padx=30, pady=(150, 15))
        self.username_entry = ctk.CTkEntry(self.login_frame, width=settings.ENTRY_WIDTH, placeholder_text="username")
        self.username_entry.grid(row=1, column=0, padx=30, pady=(15, 15))
        self.username_entry.bind("<Return>", lambda e: self.fetch_db(controller))
        self.password_entry = ctk.CTkEntry(self.login_frame, width=settings.ENTRY_WIDTH, show="*", placeholder_text="password")
        self.password_entry.grid(row=2, column=0, padx=30, pady=(0, 15))
        self.password_entry.bind("<Return>", lambda e: self.fetch_db(controller))
        self.login_button = ctk.CTkButton(self.login_frame, text="Login", width=settings.ENTRY_WIDTH, command=lambda: self.fetch_db(controller))
        self.login_button.grid(row=3, column=0, padx=30, pady=(15, 15))
        self.signup_button = ctk.CTkButton(self.login_frame, text="Skapa Konto", width=settings.ENTRY_WIDTH, command=lambda: self.sign_up(controller))
        self.signup_button.grid(row=4, column=0, padx=30, pady=(15, 15))
    # Show sign up page

    @staticmethod
    def sign_up(controller):
        controller.show_frame(SignUpPage)
    # Verify Login inputs to the database

    def fetch_db(self, controller):
        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()

        auth = hashlib.sha256(self.password_entry.get().encode()).hexdigest()
        cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (self.username_entry.get(), auth))
        if cur.fetchall():
            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            controller.show_frame(App)
        else:
            mbox.showinfo("", "Invalid Username or Password!")
        conn.commit()

# ------------------------------------------------ Signup Page ---------------------------------------------------------


# Create Sign Up Page Frame
class SignUpPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.bg_image = ctk.CTkImage(Image.open("assets/bg_gradient.jpg"), size=(900, 500))
        self.bg_image_label = ctk.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)
        self.login_frame = ctk.CTkFrame(self, corner_radius=settings.CORNER_RADIUS)
        self.login_frame.grid(row=0, column=0, sticky="ns")
        self.login_label = ctk.CTkLabel(self.login_frame, text="Skapa Konto", font=ctk.CTkFont(size=20, weight="bold"))
        self.login_label.grid(row=0, column=0, padx=30, pady=(150, 15))
        self.username_entry = ctk.CTkEntry(self.login_frame, width=settings.ENTRY_WIDTH, placeholder_text="username")
        self.username_entry.grid(row=1, column=0, padx=30, pady=(15, 15))
        self.password_entry = ctk.CTkEntry(self.login_frame, width=settings.ENTRY_WIDTH, show="*", placeholder_text="password")
        self.password_entry.grid(row=2, column=0, padx=30, pady=(0, 15))
        self.signup_button = ctk.CTkButton(self.login_frame, text="Skapa Konto", width=settings.ENTRY_WIDTH, command=lambda: self.create_account(controller))
        self.signup_button.grid(row=3, column=0, padx=30, pady=(15, 15))

    # Get username anda password entry and puts it into database
    def create_account(self, controller):
        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()

        username, password = self.username_entry.get(), hashlib.sha256(self.password_entry.get().encode()).hexdigest()
        cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username, password))

        controller.show_frame(LoginPage)
        conn.commit()
    # ----------------------------------------------- Configuring App ------------------------------------------------------


# Creating the app
class App(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        # Configure grid

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        # Loading Images with light and dark mode
        self.logo_image = ctk.CTkImage(Image.open('P-Uppgift/assets/CustomTkinter_logo_single.png'), size=(35, 35))
        self.home_image = ctk.CTkImage(light_image=Image.open('home_dark.png'),
                                       dark_image=Image.open('home_light.png'), size=(25, 25))
        self.tech_image = ctk.CTkImage(light_image=Image.open('tech_analysis_icon_dark.png'),
                                       dark_image=Image.open('tech_analysis_icon_light.png'), size=(25, 25))
        self.funda_image = ctk.CTkImage(light_image=Image.open('funda_analysis_icon_dark.png'),
                                        dark_image=Image.open('funda_analysis_icon_light.png'), size=(25, 25))
        self.beta_image = ctk.CTkImage(light_image=Image.open('beta_icon_dark.png'),
                                       dark_image=Image.open('beta_icon_light.png'), size=(25, 25))
        self.exit_image = ctk.CTkImage(light_image=Image.open('exit_icon_dark.png'),
                                       dark_image=Image.open('exit_icon_light.png'), size=(25, 25))
        self.logout_image = ctk.CTkImage(light_image=Image.open('logout_icon_dark.png'),
                                         dark_image=Image.open('logout_icon_light.png'), size=(25, 25))
        self.bg_image = ctk.CTkImage(Image.open("bg_gradient.jpg"), size=(900, 500))
        self.search_image = ctk.CTkImage(light_image=Image.open('search_icon_dark.png'),
                                         dark_image=Image.open('search_icon_light.png'), size=(30, 30))

# ----------------------------------------------- String Variables -----------------------------------------------------

        # String variables for the beta combo boxes
        self.chosen_ticker = ctk.StringVar()
        self.stock_1 = ctk.StringVar()
        self.stock_2 = ctk.StringVar()
        self.stock_3 = ctk.StringVar()
        self.stock_4 = ctk.StringVar()
        self.stock_5 = ctk.StringVar()

        # Store the 5 stocks from beta value page, to collect the beta value from, to a list
        self.beta_stocks = [self.stock_1, self.stock_2, self.stock_3, self.stock_4, self.stock_5]

# ------------------------------------------------ Navigation Frame ----------------------------------------------------

        # Creating Navigation Frame
        self.navigation_frame = ctk.CTkFrame(
            self,
            corner_radius=settings.CORNER_RADIUS
        )
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(7, weight=1)

        self.icon_image = ctk.CTkLabel(
            self.navigation_frame,
            text="  Aktie-Analys",
            image=self.logo_image,
            compound="left",
            font=ctk.CTkFont(size=15, weight=settings.FONT_WEIGHT)
        )
        self.icon_image.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=settings.CORNER_RADIUS,
            border_spacing=settings.BORDER_SPACING,
            height=settings.HEIGHT,
            fg_color=settings.FG_COLOR,
            text_color=settings.TEXT_COLOR,
            hover_color=settings.HOVER_COLOR,
            font=ctk.CTkFont(size=settings.NAVIGATION_FONT_SIZE, weight=settings.FONT_WEIGHT),
            text="Home",
            anchor=settings.ANCHOR,
            image=self.home_image,
            command=self.home_button_event
        )
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.funda_button = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=settings.CORNER_RADIUS,
            border_spacing=settings.BORDER_SPACING,
            height=settings.HEIGHT,
            fg_color=settings.FG_COLOR,
            text_color=settings.TEXT_COLOR,
            hover_color=settings.HOVER_COLOR,
            font=ctk.CTkFont(size=settings.NAVIGATION_FONT_SIZE, weight=settings.FONT_WEIGHT),
            text="Fundamental Analys",
            anchor=settings.ANCHOR,
            image=self.funda_image,
            command=self.fundamental_button_event
        )
        self.funda_button.grid(row=2, column=0, sticky="ew")

        self.tech_button = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=settings.CORNER_RADIUS,
            border_spacing=settings.BORDER_SPACING,
            height=settings.HEIGHT,
            fg_color=settings.FG_COLOR,
            text_color=settings.TEXT_COLOR,
            hover_color=settings.HOVER_COLOR,
            font=ctk.CTkFont(size=settings.NAVIGATION_FONT_SIZE, weight=settings.FONT_WEIGHT),
            text="Teknisk Analys",
            anchor=settings.ANCHOR,
            image=self.tech_image,
            command=self.tech_button_event
        )
        self.tech_button.grid(row=3, column=0, sticky="ew")

        self.beta_button = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=settings.CORNER_RADIUS,
            border_spacing=settings.BORDER_SPACING,
            height=settings.HEIGHT,
            fg_color=settings.FG_COLOR,
            text_color=settings.TEXT_COLOR,
            hover_color=settings.HOVER_COLOR,
            font=ctk.CTkFont(size=settings.NAVIGATION_FONT_SIZE, weight=settings.FONT_WEIGHT),
            text="Rangordning",
            anchor=settings.ANCHOR,
            image=self.beta_image,
            command=self.beta_button_event
        )
        self.beta_button.grid(row=4, column=0, sticky="ew")

        self.logout_button = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=settings.CORNER_RADIUS,
            border_spacing=settings.BORDER_SPACING,
            height=settings.HEIGHT,
            fg_color=settings.FG_COLOR,
            text_color=settings.TEXT_COLOR,
            hover_color=settings.HOVER_COLOR,
            font=ctk.CTkFont(size=settings.NAVIGATION_FONT_SIZE, weight=settings.FONT_WEIGHT),
            text="Logga ut",
            anchor=settings.ANCHOR,
            image=self.logout_image,
            command=lambda: controller.show_frame(LoginPage)
        )
        self.logout_button.grid(row=5, column=0, sticky="ew")

        self.exit_button = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=settings.CORNER_RADIUS,
            border_spacing=settings.BORDER_SPACING,
            height=settings.HEIGHT,
            fg_color=settings.FG_COLOR,
            text_color=settings.TEXT_COLOR,
            hover_color=settings.HOVER_COLOR,
            font=ctk.CTkFont(size=settings.NAVIGATION_FONT_SIZE, weight=settings.FONT_WEIGHT),
            text="Avsluta",
            anchor=settings.ANCHOR,
            image=self.exit_image,
            command=self.quit
        )
        self.exit_button.grid(row=6, column=0, sticky="ew")

        self.appearance_mode = ctk.CTkOptionMenu(
            self.navigation_frame,
            values=["Dark", "Light", "System"],
            font=ctk.CTkFont(size=settings.NAVIGATION_FONT_SIZE, weight=settings.FONT_WEIGHT),
            command=self.set_appearance_mode_event
        )
        self.appearance_mode.grid(row=7, column=0, padx=20, pady=20, sticky="s")

# -------------------------------------------------- Home Frame --------------------------------------------------------

        # Creating Home Frame
        self.home_frame = ctk.CTkFrame(
            self,
            corner_radius=settings.CORNER_RADIUS,
            fg_color=settings.FG_COLOR
        )
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid_rowconfigure(0, weight=1)

        self.bg_image_label1 = ctk.CTkLabel(
            self.home_frame,
            image=self.bg_image,
            text="Välkommen till Aktie-Analyseraren som analyserar en\naktie från S&P500",
            font=ctk.CTkFont(size=25, weight=settings.FONT_WEIGHT)
        )
        self.bg_image_label1.grid(row=0, column=0, sticky="ns")

# --------------------------------------------- Fundamental Analysis Frame ---------------------------------------------

        # Creating Fundamental Analysis Frame
        self.fundamental_frame = ctk.CTkFrame(
            self,
            corner_radius=settings.CORNER_RADIUS,
            fg_color=settings.FG_COLOR
        )
        self.fundamental_frame.grid_columnconfigure(0, weight=1)
        self.fundamental_frame.grid_rowconfigure(0, weight=1)

        self.bg_image_label_funda = ctk.CTkLabel(
            self.fundamental_frame,
            image=self.bg_image,
            text="Välj Aktie för en\nFundamental Analys:",
            font=ctk.CTkFont(size=25, weight=settings.FONT_WEIGHT)
        )
        self.bg_image_label_funda.grid(row=0, column=0)

        self.combo_box_funda = ctk.CTkComboBox(
            self.fundamental_frame,
            variable=self.chosen_ticker,
            values=tickers_sp500()
        )
        self.combo_box_funda.grid(row=1, column=0, pady=10)
        self.combo_box_funda.bind("<KeyRelease>", self.funda_combo_box_new_values)
        self.combo_box_funda.bind("<Return>", self.funda_combo_box_selection)

        self.fundamental_button = ctk.CTkButton(
            self.fundamental_frame,
            image=self.search_image,
            text="  Sök \t",
            font=ctk.CTkFont(size=20, weight=settings.FONT_WEIGHT),
            command=lambda: threading.Thread(target=self.funda_combobox_value).start()
        )
        self.fundamental_button.grid(row=2, column=0, pady=10)

# -------------------------------------------- Technical Analysis Frame ------------------------------------------------

        # Creating Technical Analysis Frame
        self.tech_frame = ctk.CTkFrame(
            self,
            corner_radius=settings.CORNER_RADIUS,
            fg_color=settings.FG_COLOR
        )
        self.tech_frame.grid_columnconfigure(0, weight=1)
        self.tech_frame.grid_rowconfigure(0, weight=1)

        self.bg_image_label_funda = ctk.CTkLabel(
            self.tech_frame,
            image=self.bg_image,
            text="Välj Aktie för en\nTeknisk Analys:",
            font=ctk.CTkFont(size=25, weight=settings.FONT_WEIGHT)
        )
        self.bg_image_label_funda.grid(row=0, column=0)

        self.combo_box_tech = ctk.CTkComboBox(
            self.tech_frame,
            variable=self.chosen_ticker,
            values=tickers_sp500()
        )
        self.combo_box_tech.grid(row=1, column=0, pady=10)
        # Binding keyboard keys to call function
        self.combo_box_tech.bind("<KeyRelease>", self.tech_combo_box_new_values)
        self.combo_box_tech.bind("<Return>", self.tech_combo_box_selection)

        self.fundamental_button = ctk.CTkButton(
            self.tech_frame,
            image=self.search_image,
            text="  Sök \t",
            font=ctk.CTkFont(size=20, weight=settings.FONT_WEIGHT),
            command=self.tech_combobox_value
        )
        self.fundamental_button.grid(row=2, column=0, pady=10)

# ----------------------------------------------- Beta Value Frame -----------------------------------------------------

        # Creating Beta Value Frame
        self.beta_frame = ctk.CTkFrame(
            self,
            corner_radius=settings.CORNER_RADIUS,
            fg_color=settings.FG_COLOR
        )
        self.beta_frame.grid_columnconfigure(3, weight=1)

        self.bg_image_label_beta = ctk.CTkLabel(
            self.beta_frame,
            image=self.bg_image,
            text=""
        )
        self.bg_image_label_beta.place(relx=0.7, rely=0)

        self.beta_label = ctk.CTkLabel(
            self.beta_frame,
            text="Välj 5 Aktier för rangordning med\navseende på dess betavärde",
            font=ctk.CTkFont(size=25, weight=settings.FONT_WEIGHT)
        )
        self.beta_label.grid(row=0, column=0, padx=30, pady=20, columnspan=3)

        for i in range(0, 5):
            self.stock_num_label = ctk.CTkLabel(
                self.beta_frame,
                text="Aktie " + str(1 + i) + ":",
                font=ctk.CTkFont(size=20, weight=settings.FONT_WEIGHT)
            )
            self.stock_num_label.grid(row=1 + i, column=0, pady=3)

        for i in range(len(self.beta_stocks)):
            self.combo_box_beta = ctk.CTkComboBox(
                self.beta_frame,
                variable=self.beta_stocks[i],
                values=tickers_sp500(),
                justify="center",
                state="readonly",
                text_color="black",
                font=ctk.CTkFont(size=15, weight=settings.FONT_WEIGHT)
            )
            self.combo_box_beta.grid(row=1 + i, column=1, pady=10)

        self.rang_button = ctk.CTkButton(
            self.beta_frame,
            font=ctk.CTkFont(size=20, weight=settings.FONT_WEIGHT),
            text="Rangordna",
            command=lambda: threading.Thread(target=self.beta_combobox_value).start()
        )
        self.rang_button.grid(row=6, column=0, padx=10, pady=10)

# ---------------------------------------------- Show Beta Values Frame ------------------------------------------------

        # Create frame to show sorted beta values
        self.sorted_beta_frame = ctk.CTkFrame(
            self,
            corner_radius=settings.CORNER_RADIUS,
            fg_color=settings.FG_COLOR
        )
        self.sorted_beta_frame.grid_columnconfigure(0, weight=1)

        self.sorted_beta_label = ctk.CTkLabel(
            self.sorted_beta_frame,
            text="Detta är aktierna rangordnade från störst till minst",
            font=ctk.CTkFont(size=25, weight=settings.FONT_WEIGHT),
        )
        self.sorted_beta_label.grid(row=0, column=0, padx=10, pady=20)

# ------------------------------------------- Show Fundamental Data Frame ----------------------------------------------

        # Create frame to show fundamental data for selected stock
        self.show_funda_data_frame = ctk.CTkFrame(
            self,
            corner_radius=settings.CORNER_RADIUS,
            fg_color=settings.FG_COLOR
        )
        self.show_funda_data_frame.grid_columnconfigure(0, weight=1)
        self.show_funda_data_frame.grid(row=0, column=0, sticky="ns")

# -------------------------------------------- Show Technical Data Frame -----------------------------------------------

        # Create frame to show technical data for selected stock
        self.show_tech_data_frame = ctk.CTkFrame(
            self,
            corner_radius=settings.CORNER_RADIUS,
            fg_color=settings.FG_COLOR
        )
        self.show_tech_data_frame.grid_columnconfigure(0, weight=1)
        self.show_tech_data_frame.grid_rowconfigure(0, weight=1)

# ---------------------------------------------- Initialized Frame -----------------------------------------------------

        # Show default frame named home
        self.select_frame_by_name("home")

# --------------------------------------------- Beta Combo Box Value ---------------------------------------------------

    # If any of the beta combo boxes is empty button click will do nothing, else gather beta values
    def beta_combobox_value(self):
        if self.combo_box_beta.get() == "":
            mbox.showinfo("", "Enter valid tickers")
        elif self.combo_box_beta.get().upper() not in tickers_sp500():
            mbox.showwarning("", "One or more invalid tickers")
        else:
            self.gather_beta_data()

# ---------------------------------------- Fundamental Combo Box Value -------------------------------------------------

    # If combo box is empty button click will do nothing, else gather fundamental data
    def funda_combobox_value(self):
        if self.combo_box_tech.get() == "":
            mbox.showinfo("", "Enter a valid ticker")
        elif self.combo_box_tech.get().upper() not in tickers_sp500():
            mbox.showwarning("", "Not a valid ticker!")
        else:
            self.gather_funda_data()

# ----------------------------------------- Technical Combo Box Value --------------------------------------------------

    # If combo box is empty button click will do nothing, else gather technical data
    def tech_combobox_value(self):
        if self.combo_box_tech.get() == "":
            mbox.showinfo("", "Enter a valid ticker")
        elif self.combo_box_tech.get().upper() not in tickers_sp500():
            mbox.showwarning("", "Not a valid ticker!")
        else:
            self.gather_tech_data()

# --------------------------------------------- Gather Beta Values -----------------------------------------------------

    # Gather beta values and put the values into labels
    def gather_beta_data(self):
        beta_label = []
        tickers = [self.stock_1.get(), self.stock_2.get(), self.stock_3.get(),
                   self.stock_4.get(), self.stock_5.get()]

        sorted_beta_list = beta.gather_beta_data(tickers)

        # Loop through sorted list and create labels for each sorted beta value
        for i in range(len(sorted_beta_list)):
            beta_label.append(ctk.CTkLabel(
                self.sorted_beta_frame,
                text=sorted_beta_list[i],
                font=ctk.CTkFont(size=20, weight=settings.FONT_WEIGHT),
            ))
            beta_label[i].grid(row=1 + i, column=0, padx=30, pady=15, sticky="ns")

        self.rang_button_event()

# -------------------------------------------- Gather Fundamental Data -------------------------------------------------

    # Gather fundamental data and put the values into a label for user
    def gather_funda_data(self):
        funda_info = funda.gather_funda_info(self.chosen_ticker.get())

        bg_image_label_funda1 = ctk.CTkLabel(
            self.show_funda_data_frame,
            image=self.bg_image,
            text="",
            font=ctk.CTkFont(size=25, weight=settings.FONT_WEIGHT)
        )
        bg_image_label_funda1.grid(row=0, column=0)

        funda_data_label = ctk.CTkLabel(
            self.show_funda_data_frame,
            text=f"Aktie: {funda_info['company']}\n\n\nEfterföljande P/E: {funda_info['t_ppe']}\n\nTerminspris P/E: {funda_info['f_ppe']}\n\nPris per Aktie P/S: {funda_info['pps']}",
            font=ctk.CTkFont(size=20, weight=settings.FONT_WEIGHT)
        )
        funda_data_label.grid(row=0, column=0, padx=20, pady=15, sticky="nsew")

        self.show_fundamental_data()

# --------------------------------------------- Gather Technical Data --------------------------------------------------

    # Gather Technical data by downloading data from yahoo finance
    def gather_tech_data(self):
        data = tech.gather_tech_data(self.chosen_ticker.get())

        # Put the chart on top of ctk frame
        chart = FigureCanvasTkAgg(data['fig'], self.show_tech_data_frame)
        chart.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        # Creating toolbar for the diagram to be able to move it around
        toolbar = NavigationToolbar2Tk(chart, self.show_tech_data_frame, pack_toolbar=False)
        toolbar.grid(row=2, column=0, sticky="ew")

        # Creating frame for technical info and putting labels on the frame
        stock_info_frame = ctk.CTkFrame(
            self.show_tech_data_frame,
            corner_radius=0,
            fg_color=settings.FG_COLOR
        )
        stock_info_frame.grid(row=0, column=1, sticky="ne")

        price_change_label = ctk.CTkLabel(
            stock_info_frame,
            text=f"Kursutveckling(30 dagar): {data['price_change']}%",
            font=ctk.CTkFont(size=12, weight=settings.FONT_WEIGHT)

        )
        price_change_label.grid(row=0, column=1, padx=10, pady=10)

        price_high_label = ctk.CTkLabel(
            stock_info_frame,
            text=f"Högsta kurs(30 dagar): {data['stock_price_high']}",
            font=ctk.CTkFont(size=12, weight=settings.FONT_WEIGHT)
        )
        price_high_label.grid(row=1, column=1, padx=10, pady=10)

        price_low_label = ctk.CTkLabel(
            stock_info_frame,
            text=f"Lägsta kurs(30 dagar): {data['stock_price_low']}",
            font=ctk.CTkFont(size=12, weight=settings.FONT_WEIGHT)
        )
        price_low_label.grid(row=2, column=1, padx=10, pady=10)

        self.show_tech_data()

# ----------------------------------------------- Button FG Color ------------------------------------------------------

    # Switch button fg color when pressed
    def select_frame_by_name(self, name):
        self.home_button.configure(
            fg_color=settings.BUTTON_FG_COLOR if name == "home" else settings.FG_COLOR
        )
        self.funda_button.configure(
            fg_color=settings.BUTTON_FG_COLOR if name == "fundamental_frame" else settings.FG_COLOR
        )
        self.tech_button.configure(
            fg_color=settings.BUTTON_FG_COLOR if name == "tech_frame" else settings.FG_COLOR
        )
        self.beta_button.configure(
            fg_color=settings.BUTTON_FG_COLOR if name == "beta_frame" else settings.FG_COLOR
        )

# ------------------------------------------------- Switch frame -------------------------------------------------------

        # If statements to switch frames based on frame name
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()

        if name == "fundamental_frame":
            self.fundamental_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fundamental_frame.grid_forget()

        if name == "tech_frame":
            self.tech_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.tech_frame.grid_forget()

        if name == "beta_frame":
            self.beta_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.beta_frame.grid_forget()

        if name == "sorted_beta_frame":
            self.sorted_beta_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.sorted_beta_frame.grid_forget()

        if name == "show_funda_data":
            self.show_funda_data_frame.grid(row=0, column=1, sticky="ew")
        else:
            self.show_funda_data_frame.grid_forget()

        if name == "show_tech_data":
            self.show_tech_data_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.show_tech_data_frame.grid_forget()

# -----------------------------------------------Show selected frame ---------------------------------------------------

    # Functions to show the selected frame based on pressed button
    def home_button_event(self):
        self.select_frame_by_name("home")

    def fundamental_button_event(self):
        self.select_frame_by_name("fundamental_frame")

    def tech_button_event(self):
        self.select_frame_by_name("tech_frame")

    def beta_button_event(self):
        self.select_frame_by_name("beta_frame")

    def rang_button_event(self):
        self.select_frame_by_name("sorted_beta_frame")

    def show_fundamental_data(self):
        self.select_frame_by_name("show_funda_data")

    def show_tech_data(self):
        self.select_frame_by_name("show_tech_data")

# ------------------------------------------- Set new values in combo box ----------------------------------------------

    def funda_combo_box_new_values(self, event):
        value = event.widget.get()
        if value == "":
            self.combo_box_funda.configure(values=tickers_sp500())
        else:
            data = []
            for item in tickers_sp500():
                if value.lower() in item.lower():
                    data.append(item)
            self.combo_box_funda.configure(values=data)

    def tech_combo_box_new_values(self, event):
        value = event.widget.get()
        if value == "":
            self.combo_box_tech.configure(values=tickers_sp500())
        else:
            data = []
            for item in tickers_sp500():
                if value.lower() in item.lower():
                    data.append(item)
            self.combo_box_tech.configure(values=data)

# --------------------------------------------- Event bind Return key --------------------------------------------------

    def funda_combo_box_selection(self, event):
        value = event.widget.get()
        if value == "":
            mbox.showinfo("", "Enter a valid ticker")
        elif value.upper() not in tickers_sp500():
            mbox.showwarning("", "Not a valid ticker!")
        else:
            self.gather_funda_data()

    def tech_combo_box_selection(self, event):
        value = event.widget.get()
        if value == "":
            mbox.showinfo("", "Enter a valid ticker")
        elif value.upper() not in tickers_sp500():
            mbox.showwarning("", "Not a valid ticker!")
        else:
            self.gather_tech_data()

# --------------------------------------------- Appearance mode of GUI -------------------------------------------------

    # Set the appearance mode of the GUI
    @staticmethod
    def set_appearance_mode_event(appearance_mode):
        ctk.set_appearance_mode(appearance_mode)

# ------------------------------------------------- quit program -------------------------------------------------------

    # Exits the program correctly
    def quit(self):
        self.destroy()
        app.destroy()

# ------------------------------------------------- Start Program ------------------------------------------------------


# Only start program if it is started as a script and not imported
if __name__ == "__main__":
    app = Windows()
    app.mainloop()
