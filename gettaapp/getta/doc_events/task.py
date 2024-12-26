
import frappe
import json

@frappe.whitelist()
def get_task_data(start , end , filters = None):
    filters = json.loads(filters)
    
    conditions = ''
    from frappe.desk.calendar import get_event_conditions
    conditions = get_event_conditions("Task", filters)
    data = frappe.db.sql(f""" SELECT subject, name, 
                         project, 
                         color, 
                         exp_start_date, 
                         exp_end_date, 
                         status, 
                         description, 
                         priority, 
                         creation, 
                         owner,
                         assset, 
                         project
                         From `tabTask` 
                         where 1=1 {conditions}
                          """, as_dict = 1)
    
    return data