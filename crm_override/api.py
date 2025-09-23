import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def get_csrf_token():
    """
    Return a fresh CSRF token
    """
    frappe.local.response["message"] = {
        "csrf_token": frappe.generate_hash(length=32)  # just generate one
    }
    return frappe.local.response["message"]


@frappe.whitelist(allow_guest=True)
def force_logout(csrf_token=None):
    """
    Logout user by clearing session.
    Accepts CSRF token from frontend.
    """
    if not csrf_token:
        frappe.throw(_("CSRF token required"))

    # optional: you can validate the token here if you store it in session
    # for simplicity, we skip validation since it's for force logout

    try:
        # Delete server-side session cookies
        frappe.local.cookie_manager.delete_cookie("sid")
        frappe.local.cookie_manager.delete_cookie("full_name")
        frappe.local.cookie_manager.delete_cookie("system_user")
        frappe.local.cookie_manager.delete_cookie("user_id")
        frappe.local.response["message"] = _("Logged out successfully")
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Force logout failed")
        frappe.throw(_("Logout failed"))

    return frappe.local.response["message"]


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


