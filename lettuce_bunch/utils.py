def every(pred, seq):
    for i in seq:
        if not pred(i): return False
    return True

def any(pred, seq):
    for i in seq:
        if pred(i): return True
    return False
