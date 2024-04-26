import customtkinter as ctk
import customtkinter

customtkinter.set_appearance_mode("light")

def toggle_dark_mode():
    if dark_mode_button.get():
        ctk.set_appearance_mode("dark")
    else:
        ctk.set_appearance_mode("light")

def destroy_window():
    dashbord_BT.destroy()
    import login
    login.show_login()


dashbord_BT = ctk.CTk()
dashbord_BT.geometry("1200x700")
dashbord_BT.title("PAGE RECOVER PASSWORD - BUDGET-TRACKER")
dashbord_BT.iconbitmap("logo/badgettraker.ico")


Dec_button = ctk.CTkButton(master=dashbord_BT, text='DECONNEXION', command=destroy_window)
Dec_button.pack(side='top', anchor='ne', padx=20, pady=20)


label = ctk.CTkLabel(master=dashbord_BT, font=("", 20, 'bold'), text='---BUDGET-TRACKER---')
label.pack(pady=2, padx=10, fill='both')

frame2 = ctk.CTkFrame(master=dashbord_BT)
frame2.pack(side='right', pady=200, padx=15, fill='both')


frame1 = ctk.CTkFrame(master=dashbord_BT)
frame1.pack(side='left', pady=200, padx=15, fill='both')



frame = ctk.CTkFrame(master=dashbord_BT)
frame.pack(pady=100, padx=5, fill='both', expand=True)


dark_mode_button = ctk.CTkSwitch(dashbord_BT, onvalue=1, offvalue=0, text='Activer le mode sombre ou clair', command=toggle_dark_mode)
dark_mode_button.pack(pady=10)

Budjet_traker = ctk.CTkLabel(dashbord_BT, font=("", 10), text="© Budget-tracker 2024-2025 Conception et réalisation par Med-Mehdi ZMANTAR & Jassem BOUGHATAS. Tous droits réservés.")
Budjet_traker.pack(pady=10)

dashbord_BT.mainloop()
