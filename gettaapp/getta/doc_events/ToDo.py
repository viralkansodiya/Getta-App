import frappe
from urllib.parse import urlparse
from urllib.parse import urlencode, urlunparse

def validate(self, method):
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