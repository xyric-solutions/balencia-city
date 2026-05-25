#!/usr/bin/env python3
"""
Send Python code to the running Blender instance via the MCP addon socket (port 9876).
Usage: python3 blender_send.py <script_file.py>
       python3 blender_send.py --code "import bpy; print(len(bpy.data.objects))"
       python3 blender_send.py --scene-info
       python3 blender_send.py --screenshot
"""
import socket
import json
import sys
import base64

HOST = '127.0.0.1'
PORT = 9876
TIMEOUT = 30


def send_command(cmd_type, params=None):
    """Send a command to Blender MCP addon and return the response."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.settimeout(TIMEOUT)

    command = {"type": cmd_type}
    if params:
        command["params"] = params

    payload = json.dumps(command)
    sock.sendall(payload.encode('utf-8'))

    data = b''
    while True:
        try:
            chunk = sock.recv(65536)
            if not chunk:
                break
            data += chunk
            # Try to parse JSON to see if we have a complete response
            try:
                json.loads(data.decode('utf-8'))
                break  # Valid JSON received
            except json.JSONDecodeError:
                continue  # Incomplete, keep reading
        except socket.timeout:
            break

    sock.close()
    response = json.loads(data.decode('utf-8'))
    return response


def execute_code(code):
    """Execute Python code in Blender."""
    return send_command("execute_code", {"code": code})


def get_scene_info():
    """Get scene information from Blender."""
    return send_command("get_scene_info")


def get_screenshot():
    """Get a viewport screenshot from Blender."""
    return send_command("get_viewport_screenshot")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 blender_send.py <script.py> | --code 'code' | --scene-info | --screenshot")
        sys.exit(1)

    if sys.argv[1] == "--scene-info":
        result = get_scene_info()
        print(json.dumps(result, indent=2)[:5000])
    elif sys.argv[1] == "--screenshot":
        result = get_screenshot()
        if result.get("status") == "success":
            img_data = result.get("result", "")
            # Save base64 image
            if img_data:
                with open("/tmp/blender_screenshot.png", "wb") as f:
                    f.write(base64.b64decode(img_data))
                print("Screenshot saved to /tmp/blender_screenshot.png")
            else:
                print("No image data in response")
        else:
            print(f"Error: {result.get('message', 'unknown')}")
    elif sys.argv[1] == "--code":
        code = sys.argv[2]
        result = execute_code(code)
        print(json.dumps(result, indent=2)[:5000])
    else:
        # Read script file
        with open(sys.argv[1], 'r') as f:
            code = f.read()
        result = execute_code(code)
        print(json.dumps(result, indent=2)[:5000])
