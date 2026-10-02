#!/usr/bin/env python3
"""Small dependency-free MCP stdio server for the FL Studio Copilot plugin."""
import json, os, sys, time, uuid, struct
from pathlib import Path

ROOT = Path(os.environ.get("FLSTUDIO_COPILOT_DIR", Path.home() / "FL Studio Copilot"))
ROOT.mkdir(parents=True, exist_ok=True)
COMMAND = ROOT / "command.json"
STATUS = ROOT / "status.json"

def write_command(kind, payload=None):
    data = {"id": str(uuid.uuid4()), "kind": kind, "time": time.time(), "payload": payload or {}}
    COMMAND.write_text(json.dumps(data), encoding="utf-8")
    return data

def midi_file(path, notes, tempo=130, channels=1):
    ppq=480; events=[]
    for n in notes:
        events += [(n[0], bytes([0x90|n[3], n[1], n[2]])), (n[0]+n[2+0], bytes([0x80|n[3], n[1], 0]))]
    # notes are (start_tick, pitch, velocity, channel, length_tick)
    events=[]
    for start,pitch,vel,ch,length in notes:
        events.extend([(start, bytes([0x90|ch,pitch,vel])), (start+length, bytes([0x80|ch,pitch,0]))])
    events.sort(key=lambda x:x[0]); track=bytearray(); last=0
    def vlq(v):
        b=[v&127]; v>>=7
        while v: b.append((v&127)|128); v>>=7
        return bytes(reversed(b))
    track += b'\x00\xff\x51\x03' + int(60000000/tempo).to_bytes(3,'big')
    for tick,msg in events: track += vlq(tick-last)+msg; last=tick
    track += b'\x00\xff\x2f\x00'
    data=b'MThd'+struct.pack('>IHHH',6,0,1,ppq)+b'MTrk'+struct.pack('>I',len(track))+track
    Path(path).write_bytes(data); return str(path)

TOOLS = {
 "arm_live_take": {"description":"Arm FL Studio for a live take and wait for the user to press Play.","inputSchema":{"type":"object","properties":{"name":{"type":"string"}},"additionalProperties":False}},
 "finish_live_take": {"description":"Finish the current live take and ask the FL Studio bridge to preserve it.","inputSchema":{"type":"object","properties":{},"additionalProperties":False}},
 "flstudio_status": {"description":"Read the last status reported by the FL Studio companion script.","inputSchema":{"type":"object","properties":{},"additionalProperties":False}},
 "generate_midi_pattern": {"description":"Generate a beginner-friendly drum or bass MIDI file for FL Studio.","inputSchema":{"type":"object","properties":{"kind":{"type":"string","enum":["drums","bass"]},"tempo":{"type":"integer","minimum":40,"maximum":240},"key":{"type":"string"},"bars":{"type":"integer","minimum":1,"maximum":16},"style":{"type":"string"}},"required":["kind"]}}
}

def call(name, a):
    if name=="arm_live_take":
        c=write_command("arm", {"name":a.get("name","live take")}); return f"Armed take '{c['payload']['name']}'. Press Play in FL Studio when ready."
    if name=="finish_live_take": write_command("finish"); return "Finish requested. Stop playback in FL Studio; the companion script will report the saved take."
    if name=="flstudio_status": return STATUS.read_text(encoding='utf-8') if STATUS.exists() else "No FL Studio companion status received yet. Install/select the script and run it once."
    if name=="generate_midi_pattern":
        kind=a.get('kind','drums'); bars=int(a.get('bars',2)); tempo=int(a.get('tempo',130)); notes=[]
        for bar in range(bars):
            base=bar*1920
            if kind=='drums':
                for step in range(16):
                    t=base+step*120
                    if step%4==0: notes.append((t,36,112,9,60))
                    if step%4==2: notes.append((t,38,105,9,60))
                    if step%2==0: notes.append((t,42,72,9,45))
            else:
                for step,p in enumerate([36,36,43,41]): notes.append((base+step*480,p,100,0,360))
        path=ROOT/(f"{kind}-{int(time.time())}.mid"); return "Created MIDI file: "+midi_file(path,notes,tempo)
    return "Unknown tool"

def reply(i,result): print(json.dumps({"jsonrpc":"2.0","id":i,"result":result}),flush=True)
for line in sys.stdin:
    try:
        r=json.loads(line); method=r.get('method'); i=r.get('id')
        if method=='initialize': reply(i,{"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"serverInfo":{"name":"flstudio-copilot","version":"0.1.0"}})
        elif method=='notifications/initialized': pass
        elif method=='tools/list': reply(i,{"tools":[{"name":n,**v} for n,v in TOOLS.items()]})
        elif method=='tools/call': reply(i,{"content":[{"type":"text","text":call(r['params']['name'],r['params'].get('arguments',{}))}]})
        elif i is not None: reply(i,{})
    except Exception as e:
        if 'i' in locals() and i is not None: reply(i,{"isError":True,"content":[{"type":"text","text":str(e)}]})
