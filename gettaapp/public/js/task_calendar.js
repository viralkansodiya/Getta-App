// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.views.calendar["Task"] = {
	field_map: {
		start: "exp_start_date",
		end: "exp_start_date",
		id: "subject",
		title: "subject",
		allDay: "allDay",
		progress: "progress",
	},
	gantt: true,
	filters: [
		
	],
	get_events_method: "gettaapp.getta.doc_events.task.get_task_data",
	get_css_class: function (data) {
		if (data.status === "Completed") {
			return "success";
		} else if (data.status === "In Process") {
			return "warning";
		} else {
			return "danger";
		}
	},
};
