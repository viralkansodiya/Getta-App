import frappe
from frappe.desk.form.assign_to import add as add_assignment, remove

def validate(self, method):
    if not frappe.db.exists("ToDo", {"reference_type" : self.doctype , "reference_name" : self.name , "allocated_to" : self.custom_assigned_to, "status" : "Open"}):
        if self.custom_assigned_to:
            add_assignment({"doctype": self.doctype, "name": self.name, "assign_to": [self.custom_assigned_to]})


def on_update(self, method):
    if not frappe.db.exists("ToDo", {"reference_type" : self.doctype , "reference_name" : self.name , "allocated_to" : self.custom_assigned_to, "status" : "Open"}):
        if self.custom_assigned_to:
            add_assignment({"doctype": self.doctype, "name": self.name, "assign_to": [self.custom_assigned_to]})
