# name=FL Studio Copilot
# url=https://forum.image-line.com/viewforum.php?f=1994
import json, os, time
from pathlib import Path
import transport

ROOT = Path(os.environ.get('FLSTUDIO_COPILOT_DIR', str(Path.home() / 'FL Studio Copilot')))
COMMAND = ROOT / 'command.json'; STATUS = ROOT / 'status.json'; last_id = ''

def status(state, message, **extra):
    ROOT.mkdir(parents=True, exist_ok=True)
    data={'state':state,'message':message,'time':time.time(),**extra}
    STATUS.write_text(json.dumps(data), encoding='utf-8')

def OnInit(): status('ready','FL Studio Copilot connected')
def OnDeInit(): status('offline','FL Studio Copilot disconnected')
def OnIdle():
    global last_id
    try:
        if not COMMAND.exists(): return
        c=json.loads(COMMAND.read_text(encoding='utf-8'))
        if c.get('id') == last_id: return
        last_id=c.get('id',''); kind=c.get('kind')
        if kind=='arm':
            status('armed','Waiting for Play',take=c.get('payload',{}).get('name','live take'))
            # The user starts playback. Native FL Studio recording remains under their transport/filter settings.
        elif kind=='finish': status('finishing','Finish requested; stop playback to finalize the take')
    except Exception as e: status('error',str(e))
