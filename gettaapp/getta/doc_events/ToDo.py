import frappe
from urllib.parse import urlparse
from urllib.parse import urlencode, urlunparse
from frappe.utils import get_link_to_form
from frappe import _
def validate(self, method):
    notify_user(self)
    WS = frappe.get_doc("WhatsApp Settings")
    if not WS.enabled:
        return
    if self.allocated_to:
        to =  frappe.db.get_value("User", self.allocated_to, "mobile_no") or frappe.db.get_value("User", self.allocated_to, "phone") 
        reference_doctype = self.reference_type
        reference_name = self.reference_name
        from urllib.parse import quote

        # Original URL
        original_url = f"https://web3.gettaproperties.com/app/{reference_doctype}/{reference_name}"

        # Split the base URL and path
        base_url, path = original_url.split(f"/app/{reference_doctype}/", 1)

        # Encode the path
        encoded_path = quote(path)

        # Construct the final URL
        final_url = f"{base_url}/app/item/{encoded_path}"



        if to:
            if self.status == "Open":
                message = f"""
                    *Assignment of {self.reference_name}*\n\nHi {frappe.db.get_value('User', self.allocated_to, 'full_name')},\n\nYou have been assigned a new {self.reference_type}. Please review the details and follow up promptly.\n\n*{self.reference_type} ID:* {self.reference_name}\n\nView Lead Details: "{final_url}"
                """
            
            if self.status == "Cancelled":
                message = f"""
                    *Assignment Removed {self.reference_name}*\n\nHi {frappe.db.get_value('User', self.allocated_to, 'full_name')},\n\nAssignment has been removed from {self.reference_type} {self.reference_name}. .\n\n*{self.reference_type} ID:* {self.reference_name}\n\nView Details: "{final_url}"
                """
            if reference_doctype and reference_name:
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
    
def notify_user(self):
    if self.is_email_sent:
        return
    if not self.allocated_to:
        return
    if not self.reference_type and not self.reference_name:
        message = """
            <body style="background-color: #f8f9fa; padding: 20px;">
            <div class="container">
                <div class="card shadow">
                <div class="card-header bg-success text-white text-center row">
                    <h1>ToDo Assignment</h1>
                </div>
                <div class="card-body row">
                    <p>Dear <strong>{0}</strong>,</p>
                    <p>You have been assigned a new task. Please find the details below: {5}</p>
                    <div class="table-responsive row">
                    <table class="table table-bordered">
                        <tbody>
                        <tr>
                            <th scope="row">Description</th>
                            <td>{1}</td>
                        </tr>
                        <tr>
                            <th scope="row">Assigned By</th>
                            <td>{2}</td>
                        </tr>
                        <tr>
                            <th scope="row">Deadline</th>
                            <td>{3}</td>
                        </tr>
                        </tbody>
                    </table>
                    </div>
                    <p>Please ensure the task is completed by the specified deadline. Feel free to reach out if you have any questions or need further clarification.</p>
                    <p>Best regards,</p>
                    <p><strong>{4}</strong></p>
                </div>
                <div class="card-footer text-muted text-center row">
                    <small>This is an automated email. Please do not reply directly to this email.</small>
                </div>
                </div>
            </div>


              """.format(
            self.allocated_to, self.description, self.assigned_by, self.date, frappe.db.get_value("User", self.assigned_by, "full_name"), get_link_to_form("ToDo", self.name)
        )

        frappe.sendmail(
			recipients=[self.allocated_to],
			subject="ToDo Assignment",
			message = message
		)
        self.is_email_sent = 1