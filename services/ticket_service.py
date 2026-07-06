def valid_phone(phone):

    return (
        phone.isdigit()
        and len(phone) == 10
    )


def valid_priority(priority):

    return priority in [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]


def valid_status(status):

    return status in [
        "Open",
        "In Progress",
        "Resolved",
        "Closed"
    ]
