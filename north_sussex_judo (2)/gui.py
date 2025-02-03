import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import database as db
import models as md

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("600x500")
        self.resizable(False, False)
        self.configure(bg="#f0f0f0")
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure('TLabel', background="#f0f0f0", font=('Helvetica', 10))
        self.style.configure('TButton', font=('Helvetica', 10))
        self.style.configure('TEntry', font=('Helvetica', 10))

        self.username_label = ttk.Label(self, text="Username:")
        self.username_label.pack(pady=5)

        self.username_entry = ttk.Entry(self)
        self.username_entry.pack(pady=5)

        self.password_label = ttk.Label(self, text="Password:")
        self.password_label.pack(pady=5)

        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = ttk.Button(self, text="Login", command=self.login)
        self.login_button.pack(pady=10)
        self.create_user_button = ttk.Button(self, text="Create User", command=self.create_user)
        self.create_user_button.pack(pady=10)
        self.login_success = False

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username and password:
            user = db.login(username, password)
            if user:
                messagebox.showinfo("Success", f"Login successful, welcome {user['username']}")
                self.login_success = True
                self.destroy()
            else:
                messagebox.showerror("Error", "Login failed, please check your username and password.")
        else:
           messagebox.showerror("Error", "Please enter a username and a password.")

    def create_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username and password:
            if db.create_user(username, password):
               messagebox.showinfo("Success", "User Created, please log in.")
            else:
                messagebox.showerror("Error", "Failed to create user, please check details.")
        else:
           messagebox.showerror("Error", "Please enter a username and a password.")

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.logout_button = ttk.Button(self, text="Logout", command=self.logout)
        self.logout_button.pack(side=tk.BOTTOM, pady=10)
        self.title("North Sussex Judo Management")
        self.minsize(800, 600)
        self.maxsize(1600, 1200)
        self.configure(bg="#f0f0f0")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure('TLabel', background="#f0f0f0", font=('Helvetica', 10))
        self.style.configure('TButton', font=('Helvetica', 10))
        self.style.configure('TEntry', font=('Helvetica', 10))
        self.style.configure('TCombobox', font=('Helvetica', 10))

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.athlete_tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.athlete_tab, text="Athletes")
        self.setup_athlete_tab()

        self.training_tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.training_tab, text="Training Plans")
        self.setup_training_tab()

        self.competition_tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.competition_tab, text="Competitions")
        self.setup_competition_tab()

        self.report_tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.report_tab, text="Reports")
        self.setup_report_tab()
        self.bind("<Configure>", self.on_resize)

    def setup_athlete_tab(self):
        add_athlete_frame = ttk.Frame(self.athlete_tab, padding="10")
        add_athlete_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        add_athlete_frame.columnconfigure(0, weight=1)
        add_athlete_frame.columnconfigure(1, weight=1)
        add_athlete_frame.columnconfigure(2, weight=1)
        add_athlete_frame.columnconfigure(3, weight=1)
        add_athlete_frame.columnconfigure(4, weight=1)

        ttk.Label(add_athlete_frame, text="Athlete Name:").grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.athlete_name_entry = ttk.Entry(add_athlete_frame)
        self.athlete_name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(add_athlete_frame, text="Training Plan:").grid(row=0, column=2, sticky="ew", padx=5, pady=5)
        self.athlete_training_plan_combo = ttk.Combobox(add_athlete_frame, values=db.fetch_training_plans())
        self.athlete_training_plan_combo.grid(row=0, column=3, sticky="ew", padx=5, pady=5)

        ttk.Label(add_athlete_frame, text="Current Weight (kg):").grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.athlete_weight_entry = ttk.Entry(add_athlete_frame)
        self.athlete_weight_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(add_athlete_frame, text="Competition Weight Category:").grid(row=1, column=2, sticky="ew", padx=5, pady=5)
        self.athlete_weight_category_combo = ttk.Combobox(add_athlete_frame, values=db.fetch_weight_categories())
        self.athlete_weight_category_combo.grid(row=1, column=3, sticky="ew", padx=5, pady=5)

        add_athlete_button = ttk.Button(add_athlete_frame, text="Add Athlete", command=self.add_athlete)
        add_athlete_button.grid(row=1, column=4, sticky="ew", padx=5, pady=5)

        update_athlete_button = ttk.Button(add_athlete_frame, text="Update Athlete", command=self.update_athlete)
        update_athlete_button.grid(row=2, column=4, sticky="ew", padx=5, pady=5)

        delete_athlete_button = ttk.Button(add_athlete_frame, text="Delete Athlete", command=self.delete_athlete)
        delete_athlete_button.grid(row=3, column=4, sticky="ew", padx=5, pady=5)

        self.athlete_listbox_frame = ttk.Frame(self.athlete_tab)
        self.athlete_listbox_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.athlete_tab.rowconfigure(2, weight=1)
        self.athlete_tab.columnconfigure(0, weight=1)
        self.athlete_listbox_frame.rowconfigure(0, weight=1)
        self.athlete_listbox_frame.columnconfigure(0, weight=1)

        self.athlete_listbox = tk.Listbox(self.athlete_listbox_frame)
        self.athlete_listbox.grid(row=0, column=0, sticky="nsew")

        self.athlete_scrollbar = ttk.Scrollbar(self.athlete_listbox_frame, orient="vertical", command=self.athlete_listbox.yview)
        self.athlete_scrollbar.grid(row=0, column=1, sticky="ns")
        self.athlete_listbox.config(yscrollcommand=self.athlete_scrollbar.set)
        self.refresh_athlete_list()

    def update_athlete(self):
        selected = self.athlete_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select an athlete to update.")
            return
    
        athlete_info = self.athlete_listbox.get(selected[0])
        athlete_id = int(athlete_info.split(":")[0])

        name = self.athlete_name_entry.get()
        training_plan = self.athlete_training_plan_combo.get()
        try:
            weight = float(self.athlete_weight_entry.get())
            if weight <= 0:
                messagebox.showerror("Error", "Weight must be a positive value.")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid weight input. Must be a number.")
            return
    
        weight_category = self.athlete_weight_category_combo.get()
    
        if name and training_plan and weight and weight_category:
            if db.update_athlete(athlete_id, name, training_plan, weight, weight_category):
                messagebox.showinfo("Success", "Athlete updated successfully.")
                self.refresh_athlete_list()
            else:
                messagebox.showerror("Error", "Failed to update athlete.")
        else:
            messagebox.showerror("Error", "Please fill all fields to update an athlete.")



    def delete_athlete(self):
        selected = self.athlete_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select an athlete to delete.")
            return

        athlete_info = self.athlete_listbox.get(selected[0])
        athlete_id = int(athlete_info.split(":")[0])

        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this athlete?")
        if confirm:
            if db.delete_athlete(athlete_id):
                messagebox.showinfo("Success", "Athlete deleted successfully.")
                self.refresh_athlete_list()
            else:
                messagebox.showerror("Error", "Failed to delete athlete.")

    def delete_training_plan(self):
        selected = self.training_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select a training plan to delete.")
            return

        plan_name = self.training_listbox.get(selected[0])
        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete the training plan '{plan_name}'?")
        if confirm:
            if db.delete_training_plan(plan_name):
                messagebox.showinfo("Success", "Training plan deleted successfully.")
                self.refresh_training_list()
            else:
                messagebox.showerror("Error", "Failed to delete training plan.")

    def delete_competition(self):
        selected = self.competition_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select a competition to delete.")
            return

        competition_info = self.competition_listbox.get(selected[0])
        competition_id = int(competition_info.split(":")[0])

        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete this competition?")
        if confirm:
            if db.delete_competition(competition_id):
                messagebox.showinfo("Success", "Competition deleted successfully.")
                self.refresh_competition_list()
            else:
                messagebox.showerror("Error", "Failed to delete competition.")

    def delete_report(self):
        athlete_info = self.report_athlete_combo.get()
        if not athlete_info:
            messagebox.showerror("Error", "Please select an athlete to delete the report.")
            return

        try:
            athlete_id = int(athlete_info.split(":")[0])
        except ValueError:
            messagebox.showerror("Error", "Invalid athlete ID.")
            return

        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete the report for this athlete?")
        if confirm:
            if db.delete_report(athlete_id):
                messagebox.showinfo("Success", "Report deleted successfully.")
                self.report_text.delete(1.0, tk.END)
            else:
                messagebox.showerror("Error", "Failed to delete report.")

    def logout(self):
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to logout?")
        if confirm:
            self.destroy()



    def setup_training_tab(self):
       add_training_frame = ttk.Frame(self.training_tab, padding="10")
       add_training_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
       delete_training_button = ttk.Button(add_training_frame, text="Delete Training Plan", command=self.delete_training_plan)
       delete_training_button.grid(row=2, column=4, sticky="ew", padx=5, pady=5)
       add_training_frame.columnconfigure(0, weight=1)
       add_training_frame.columnconfigure(1, weight=1)
       add_training_frame.columnconfigure(2, weight=1)
       add_training_frame.columnconfigure(3, weight=1)

       ttk.Label(add_training_frame, text="Training Plan Name:").grid(row=0, column=0, sticky="ew", padx=5, pady=5)
       self.training_name_entry = ttk.Entry(add_training_frame)
       self.training_name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

       ttk.Label(add_training_frame, text="Weekly Fee (£):").grid(row=0, column=2, sticky="ew", padx=5, pady=5)
       self.training_fee_entry = ttk.Entry(add_training_frame)
       self.training_fee_entry.grid(row=0, column=3, sticky="ew", padx=5, pady=5)

       add_training_button = ttk.Button(add_training_frame, text="Add Training Plan", command=self.add_training_plan)
       add_training_button.grid(row=0, column=4, sticky="ew", padx=5, pady=5)

       self.training_listbox_frame = ttk.Frame(self.training_tab)
       self.training_listbox_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
       self.training_tab.rowconfigure(1, weight=1)
       self.training_tab.columnconfigure(0, weight=1)
       self.training_listbox_frame.rowconfigure(0, weight=1)
       self.training_listbox_frame.columnconfigure(0, weight=1)

       self.training_listbox = tk.Listbox(self.training_listbox_frame)
       self.training_listbox.grid(row=0, column=0, sticky="nsew")
       self.training_scrollbar = ttk.Scrollbar(self.training_listbox_frame, orient="vertical", command=self.training_listbox.yview)
       self.training_scrollbar.grid(row=0, column=1, sticky="ns")
       self.training_listbox.config(yscrollcommand=self.training_scrollbar.set)
       self.refresh_training_list()


    def setup_competition_tab(self):
        add_competition_frame = ttk.Frame(self.competition_tab, padding="10")
        add_competition_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        delete_competition_button = ttk.Button(add_competition_frame, text="Delete Competition", command=self.delete_competition)
        delete_competition_button.grid(row=2, column=4, sticky="ew", padx=5, pady=5)
        add_competition_frame.columnconfigure(0, weight=1)
        add_competition_frame.columnconfigure(1, weight=1)
        add_competition_frame.columnconfigure(2, weight=1)
        add_competition_frame.columnconfigure(3, weight=1)


        ttk.Label(add_competition_frame, text="Competition Name:").grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.competition_name_entry = ttk.Entry(add_competition_frame)
        self.competition_name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(add_competition_frame, text="Entry Fee (£):").grid(row=0, column=2, sticky="ew", padx=5, pady=5)
        self.competition_fee_entry = ttk.Entry(add_competition_frame)
        self.competition_fee_entry.grid(row=0, column=3, sticky="ew", padx=5, pady=5)

        ttk.Label(add_competition_frame, text="Date (YYYY-MM-DD):").grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.competition_date_entry = ttk.Entry(add_competition_frame)
        self.competition_date_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        add_competition_button = ttk.Button(add_competition_frame, text="Add Competition", command=self.add_competition)
        add_competition_button.grid(row=1, column=2, sticky="ew", padx=5, pady=5)

        add_athlete_competition_frame = ttk.Frame(self.competition_tab, padding="10")
        add_athlete_competition_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        add_athlete_competition_frame.columnconfigure(0, weight=1)
        add_athlete_competition_frame.columnconfigure(1, weight=1)
        add_athlete_competition_frame.columnconfigure(2, weight=1)
        add_athlete_competition_frame.columnconfigure(3, weight=1)


        ttk.Label(add_athlete_competition_frame, text="Athlete:").grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.athlete_combo = ttk.Combobox(add_athlete_competition_frame, values=[f"{athlete['id']}: {athlete['name']}" for athlete in db.fetch_athletes()])
        self.athlete_combo.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(add_athlete_competition_frame, text="Competition:").grid(row=0, column=2, sticky="ew", padx=5, pady=5)
        self.competition_combo = ttk.Combobox(add_athlete_competition_frame, values=[f"{competition['id']}: {competition['competition_name']}" for competition in db.fetch_competitions()])
        self.competition_combo.grid(row=0, column=3, sticky="ew", padx=5, pady=5)

        add_athlete_competition_button = ttk.Button(add_athlete_competition_frame, text="Add Athlete to Competition", command=self.add_athlete_to_competition)
        add_athlete_competition_button.grid(row=0, column=4, sticky="ew", padx=5, pady=5)

        self.competition_listbox_frame = ttk.Frame(self.competition_tab)
        self.competition_listbox_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
        self.competition_tab.rowconfigure(3, weight=1)
        self.competition_tab.columnconfigure(0, weight=1)
        self.competition_listbox_frame.rowconfigure(0, weight=1)
        self.competition_listbox_frame.columnconfigure(0, weight=1)

        self.competition_listbox = tk.Listbox(self.competition_listbox_frame)
        self.competition_listbox.grid(row=0, column=0, sticky="nsew")
        self.competition_scrollbar = ttk.Scrollbar(self.competition_listbox_frame, orient="vertical", command=self.competition_listbox.yview)
        self.competition_scrollbar.grid(row=0, column=1, sticky="ns")
        self.competition_listbox.config(yscrollcommand=self.competition_scrollbar.set)
        self.refresh_competition_list()

    def setup_report_tab(self):
        report_frame = ttk.Frame(self.report_tab, padding="10")
        report_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        delete_report_button = ttk.Button(report_frame, text="Delete Report", command=self.delete_report)
        delete_report_button.grid(row=0, column=3, sticky="ew", padx=5, pady=5)
        report_frame.columnconfigure(0, weight=1)
        report_frame.columnconfigure(1, weight=1)
        report_frame.columnconfigure(2, weight=1)

        ttk.Label(report_frame, text="Athlete:").grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.report_athlete_combo = ttk.Combobox(report_frame, values=[f"{athlete['id']}: {athlete['name']}" for athlete in db.fetch_athletes()])
        self.report_athlete_combo.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        generate_report_button = ttk.Button(report_frame, text="Generate Report", command=self.generate_athlete_report)
        generate_report_button.grid(row=0, column=2, sticky="ew", padx=5, pady=5)

        self.report_text_frame = ttk.Frame(self.report_tab)
        self.report_text_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.report_tab.rowconfigure(1, weight=1)
        self.report_tab.columnconfigure(0, weight=1)
        self.report_text_frame.rowconfigure(0, weight=1)
        self.report_text_frame.columnconfigure(0, weight=1)


        self.report_text = scrolledtext.ScrolledText(self.report_text_frame, wrap=tk.WORD)
        self.report_text.grid(row=0, column=0, sticky="nsew")


    def refresh_athlete_list(self):
        self.athlete_listbox.delete(0, tk.END)
        for athlete in db.fetch_athletes():
          self.athlete_listbox.insert(tk.END, f"{athlete['id']}: {athlete['name']}")

    def refresh_training_list(self):
        self.training_listbox.delete(0, tk.END)
        for plan in db.fetch_training_plans():
            self.training_listbox.insert(tk.END, plan)

    def refresh_competition_list(self):
        self.competition_listbox.delete(0, tk.END)
        for competition in db.fetch_competitions():
           self.competition_listbox.insert(tk.END, f"{competition['id']}: {competition['competition_name']}")

    def refresh_athlete_combobox(self):
        self.athlete_training_plan_combo['values'] = db.fetch_training_plans()
        self.athlete_weight_category_combo['values'] = db.fetch_weight_categories()
        self.report_athlete_combo['values'] = [f"{athlete['id']}: {athlete['name']}" for athlete in db.fetch_athletes()]
        self.athlete_combo['values'] = [f"{athlete['id']}: {athlete['name']}" for athlete in db.fetch_athletes()]

    def refresh_competition_combobox(self):
         self.competition_combo['values'] = [f"{competition['id']}: {competition['competition_name']}" for competition in db.fetch_competitions()]


    def add_athlete(self):
        name = self.athlete_name_entry.get()
        training_plan = self.athlete_training_plan_combo.get()
        try:
            weight = float(self.athlete_weight_entry.get())
            if weight <= 0:
                messagebox.showerror("Error", "Weight must be a positive value.")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid weight input. Must be a number.")
            return
        weight_category = self.athlete_weight_category_combo.get()

        if name and training_plan and weight and weight_category:
            if db.add_athlete(name, training_plan, weight, weight_category):
                self.refresh_athlete_list()
                self.refresh_athlete_combobox()

        else:
            messagebox.showerror("Error", "Please fill all fields to add an athlete.")

    def add_training_plan(self):
        plan_name = self.training_name_entry.get()
        try:
            weekly_fee = float(self.training_fee_entry.get())
            if weekly_fee <= 0:
                messagebox.showerror("Error", "Fee must be a positive value.")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid fee input. Must be a number.")
            return

        if plan_name and weekly_fee:
            if db.add_training_plan(plan_name, weekly_fee):
                self.refresh_training_list()
                self.refresh_athlete_combobox()
            else:
                messagebox.showerror("Error", "Please fill all fields to add a training plan.")

    def add_competition(self):
        competition_name = self.competition_name_entry.get()
        try:
            entry_fee = float(self.competition_fee_entry.get())
            if entry_fee <= 0:
                 messagebox.showerror("Error", "Entry fee must be a positive value.")
                 return
        except ValueError:
             messagebox.showerror("Error", "Invalid fee input. Must be a number.")
             return
        date_str = self.competition_date_entry.get()
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
             messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD format.")
             return
        if competition_name and entry_fee and date_str:
           if db.add_competition(competition_name, entry_fee, date_str):
               self.refresh_competition_list()
               self.refresh_competition_combobox()

        else:
           messagebox.showerror("Error", "Please fill all fields to add a competition.")


    def add_athlete_to_competition(self):
        athlete_info = self.athlete_combo.get()
        competition_info = self.competition_combo.get()

        if not athlete_info or not competition_info:
           messagebox.showerror("Error", "Please select an athlete and competition.")
           return
        try:
           athlete_id = int(athlete_info.split(":")[0])
           competition_id = int(competition_info.split(":")[0])
        except ValueError:
          messagebox.showerror("Error", "Invalid athlete or competition ID.")
          return
        if db.add_athlete_to_competition(athlete_id, competition_id):
              messagebox.showinfo("Success", "Athlete added to competition.")
              self.refresh_athlete_combobox()

    def generate_athlete_report(self):
        athlete_info = self.report_athlete_combo.get()
        if not athlete_info:
           messagebox.showerror("Error", "Please select an athlete.")
           return
        try:
            athlete_id = int(athlete_info.split(":")[0])
        except ValueError:
          messagebox.showerror("Error", "Invalid athlete ID.")
          return
        report = db.get_athlete_report_data(athlete_id)
        self.report_text.delete(1.0, tk.END)
        if report:
            report = md.ReportData(**report)
            training_fee = report.weekly_fee * 4 if report.weekly_fee is not None else 0
            coaching_fee = report.total_coaching_hours * 9.50 if report.total_coaching_hours else 0
            competition_fee = report.competition_count * report.entry_fee if report.entry_fee and report.competition_count else 0
            total_fee = training_fee + coaching_fee + competition_fee
            report_str = f"Report for Athlete: {report.name}\n"
            report_str += f"Training Fee (4 weeks): £{training_fee:.2f}\n"
            if coaching_fee != 0:
                report_str += f"Private Coaching Fee: £{coaching_fee:.2f}\n"
            if competition_fee != 0:
                report_str += f"Competition Fee: £{competition_fee:.2f}\n"
            report_str += f"Total Monthly Fee: £{total_fee:.2f}\n"
            if report.current_weight > report.limit:
                report_str += f"Current weight is higher than the competition category.\n"
            elif report.current_weight == report.limit:
                 report_str += f"Current weight is equal to the upper weight limit.\n"
            else:
                 report_str += f"Current weight is within the competition weight category\n"

            self.report_text.insert(tk.END, report_str)
        else:
             self.report_text.insert(tk.END, "No report data available for this athlete.\n")

    def on_resize(self, event):
        width = self.winfo_width()
        base_font_size = 10
        if width < 800:
           font_size = max(base_font_size - 2, 8)
        elif width > 1200:
           font_size = min(base_font_size + 2, 12)
        else:
           font_size = base_font_size
        self.style.configure('TLabel', font=('Helvetica', font_size))
        self.style.configure('TButton', font=('Helvetica', font_size))
        self.style.configure('TEntry', font=('Helvetica', font_size))
        self.style.configure('TCombobox', font=('Helvetica', font_size))


    def run(self):
        self.mainloop()
# Main Application Class

# Main Function
def main():
    conn = db.create_connection()
    if not db.check_tables_exist():
        db.execute_sql_file(conn, "north_sussex_judo_schema.sql")
    conn.close()

    login_window = LoginWindow()
    login_window.mainloop()
    if login_window.login_success:
      app = MainApp()
      app.run()
    else:
        print("Login failed. Application will now close")
if __name__ == "__main__":
    main()