import frappe
from frappe.desk.form.assign_to import add as add_assignment, remove


def validate(self, method):
    if not frappe.db.exists("ToDo", {"reference_type" : self.doctype , "reference_name" : self.name , "allocated_to" : self.custom_assigned_to, "status" : "Open"}):
        if self.custom_assigned_to:
            add_assignment({"doctype": self.doctype, "name": self.name, "assign_to": [self.custom_assigned_to]})
            message = f"""
                *Assignment of {self.name}*\n\nHi {frappe.db.get_value('User', self.custom_assigned_to, 'full_name')},\n\nYou have been assigned a new lead. Please review the details and follow up promptly.\n\n*Lead ID:* {self.name}\n\nView Lead Details: https://web3.gettaproperties.com/app/lead/{self.name}
            """
            to =  frappe.db.get_value("User", self.custom_assigned_to, "mobile_no") or frappe.db.get_value("User", self.custom_assigned_to, "phone") 
            reference_doctype = self.doctype
            reference_name = self.name
            send_template(to, reference_doctype, reference_name, message)


def send_template(to, reference_doctype, reference_name, message):
    try:
        doc = frappe.get_doc({
            "doctype": "WhatsApp Message",
            "to": to,
            "type": "Outgoing",
            "message_type": "Manual",
            "reference_doctype": reference_doctype,
            "reference_name": reference_name,
            "content_type": "text",
            "message" : message
        })

        doc.save()
    except Exception as e:
        raise e