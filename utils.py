import wmi


def get_pk_field_for_computer(computer: wmi.WMI) -> str:
    """
    todo change to
    from uuid import getnode as get_mac
    mac = get_mac()
    h = iter(hex(mac)[2:].zfill(12))
    return ":".join(i + next(h) for i in h)
    """
    mother = computer.Win32_BaseBoard(["SerialNumber"])[0]
    return mother.serialnumber
