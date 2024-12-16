import frappe
def before_naming(self, method):
    if self.is_new():
        self.item_name = self.item_code
        self.item_code = self.item_code + " - " + self.custom_type_of_property + " - " + self.custom_door_no + " - " +self.item_group