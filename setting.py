# setup

def init():
    global eyeState
    global prev_edata
    global max_edata
    global thresh_percent
    eyeState = 0 # 0=waiting, 1=dropping, 2=eye_closed
    prev_edata = 0
    max_edata = 0
    thresh_percent = 0.5