import frappe
from urllib.parse import quote
from frappe.utils import get_link_to_form, get_url
from frappe import _
import requests

def validate(self, method):
    notify_user(self)
    send_whatsapp_message(self)

def send_whatsapp_message(self):
    wh_setting = frappe.get_doc("Whatsapp Setting")
    if not wh_setting:
        return
    
    if self.allocated_to:
        to =  frappe.db.get_value("User", self.allocated_to, "mobile_no") or frappe.db.get_value("User", self.allocated_to, "phone") 
        if not to:
            frappe.throw("Please Update the phone number of the user , {0}".format(get_link_to_form("User", self.allocated_to)))
        
        number = validate_phone_number(to, self.allocated_to)
        reference_doctype = self.reference_type
        reference_name = self.reference_name
        
        original_url = f"{get_url()}/app/{reference_doctype}/{reference_name}"

        base_url, path = original_url.split(f"/app/{reference_doctype}/", 1)
        encoded_path = quote(path)
        final_url = f"{base_url}/app/{reference_doctype.lower()}/{encoded_path}"

        message_json = {
                "to": "{0}".format(number),
                "recipient_type": "individual",
                "type": "template",
                "template": {
                    "language": {
                        "policy": "deterministic",
                        "code": "en_US"
                    },
                    "name": "lead_assignment",
                    "components": [
                        {
                            "type": "body",
                            "parameters": [
                                {
                                    "type": "text",
                                    "text": "{0}".format(self.reference_name)
                                },
                                {
                                    "type": "text",
                                    "text": "{0}".format(frappe.db.get_value("User", self.allocated_to, "full_name"))
                                },
                                {
                                    "type": "text",
                                    "text": "{0}".format(self.reference_type)
                                },
                                {
                                    "type": "text",
                                    "text": "{0}".format(final_url)
                                }
                            ]
                        }
                    ]
                }
            }
        
        url = wh_setting.url
        token = wh_setting.token
        phone_id = wh_setting.phone_id
        version = wh_setting.version

        end_point_url = url  + "/" + version + "/" + phone_id + "/" + "messages"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        try:
            # Sending the POST request
            response = requests.post(end_point_url, headers=headers, json=message_json)

            # Check the response status
            if response.status_code == 200:
                print("Request was successful!")
                print("Response data:", response.json())
            else:
                frappe.log_error(response)
        except requests.exceptions.RequestException as e:
            frappe.log_error(e)
        



def validate_phone_number(number, allocated_to):
    if len(number) == 10:
        return "91" + number
    if len(number) == 12 and number[0:2] == "91":
        return number
    frappe.throw("Please update the valid phone number in User {0}".format(get_link_to_form("User", allocated_to)))

    
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