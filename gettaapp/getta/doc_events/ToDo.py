import frappe
from urllib.parse import urlparse
from urllib.parse import urlencode, urlunparse
from frappe.utils import get_link_to_form
from frappe import _
import request

def validate(self, method):
    notify_user(self)
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
            frappe.db.get_value("User", self.allocated_to, "full_name"), self.description, frappe.db.get_value("User", self.assigned_by, "full_name"), self.date, frappe.db.get_value("User", self.assigned_by, "full_name"), get_link_to_form("ToDo", self.name)
        )

        frappe.sendmail(
			recipients=[self.allocated_to],
			subject="ToDo Assignment",
			message = message
		)
        self.is_email_sent = 1