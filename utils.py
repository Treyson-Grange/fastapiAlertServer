def verify_alert(alert):
    criticalities = [0, 1, 2]
    if alert.criticality not in criticalities:
        return False

    if alert.clearAfter < 0:
        return False

    return True


def calc_criticality(day_diff, days_notice):
    percentage = day_diff / days_notice

    CRITICALITIES = {0: 0, 0.2: 1, 1: 2}

    for key in CRITICALITIES:
        if percentage <= key:
            return CRITICALITIES[key]

    return 0
