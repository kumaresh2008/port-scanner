from flask import Flask, render_template, request
import socket
from datetime import datetime

app = Flask(__name__)

# Safe demo ports for local testing
PORTS = [21, 22, 80, 443, 5000]


def scan_ports(target):
    results = []

    for port in PORTS:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)

        try:
            status = sock.connect_ex((target, port))

            if status == 0:
                state = "OPEN"
            else:
                state = "CLOSED"

        except Exception:
            state = "ERROR"

        finally:
            sock.close()

        results.append({
            "port": port,
            "status": state
        })

    return results


@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    target = "127.0.0.1"
    scanned_at = None

    if request.method == "POST":
        target = request.form.get("target", "127.0.0.1").strip()

        # Keep the project limited to local testing
        if target not in ["127.0.0.1", "localhost"]:
            results = [{
                "port": "-",
                "status": "Only localhost testing is allowed"
            }]
        else:
            if target == "localhost":
                target = "127.0.0.1"

            results = scan_ports(target)
            scanned_at = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    return render_template(
        "index.html",
        target=target,
        results=results,
        scanned_at=scanned_at
    )


if __name__ == "__main__":
    app.run(debug=True)