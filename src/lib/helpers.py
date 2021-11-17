def title(msg: str, ws: str = " ") -> str:
    """
    Perform a simplified and reduced version of str.title() for Micropython
    """

    return ws.join((word[0].upper() + word[1:].lower()) if word != "" else "" for word in msg.split(ws))
