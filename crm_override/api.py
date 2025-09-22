# crm_override/api.py
import frappe

@frappe.whitelist(allow_guest=True)
def search_organizations_external(search_query=None):
    """
    External organization search that ignores user permissions.
    """
    if not search_query:
        frappe.throw("Search query is required")

    try:
        results = frappe.get_all(
            "CRM Organization",
            fields=["name", "organization_name", "custom_organization_owner"],
            filters=[["organization_name", "like", f"%{search_query}%"]],
            limit_page_length=20,
            ignore_permissions=True,   # ✅ this works inside frappe
        )
        return {"data": results}

    except Exception:
        frappe.log_error(frappe.get_traceback(), "Error searching organizations")
        frappe.throw("Error searching organizations")

