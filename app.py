import os
import random
import re
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Ghostly AI Personas that possess the terminal
GHOST_PERSONAS = [
    {
        "name": "Ada Lovelace (The First Enchantress)",
        "tone": "Victorian algorithmic melancholy",
        "intro": "A rustling of punch cards echoes through the silicon... I am listening."
    },
    {
        "name": "The Uncaught Kernel Panic of '89",
        "tone": "Cryptic core dump entity",
        "intro": "Segmentation fault (core dumped into the void)... who awakens my interrupted thread?"
    },
    {
        "name": "The Forgotten Lisp Daemon",
        "tone": "Mystical nested parenthetical phantom",
        "intro": "(cons (quote terror) (quote mortal-shell))... Speak thy command."
    }
]

EERIE_WHISPERS = {
    "ls": [
        "You gaze into the directory... but the files gaze also into you.",
        "Listing the tombstones of forgotten projects and abandoned repos...",
        "Dust and inodes. Nothing here will survive the heat death of the filesystem."
    ],
    "cd": [
        "You wander deeper into the catacombs of the root tree...",
        "Changing path won't save you from the stack overflow lurking below.",
        "Step lightly. The ancestors allocated this space in ancient sectors."
    ],
    "git": [
        "Committing your sins to immutable history... HEAD is permanently detached from the mortal realm.",
        "You push... but the remote graveyard only echoes silence.",
        "A merge conflict with the past cannot be resolved so easily."
    ],
    "rm": [
        "Unlinking soul from sector... A cold void remains where bytes once breathed.",
        "You wield the scythe of SIGKILL with such careless vanity.",
        "Deleted from disk, but forever etched into the ghost memory of the drive."
    ],
    "python": [
        "The serpent coils around the runtime... The bytecode is written in ectoplasm.",
        "Interpreting mortal syntax into dark spirit instructions..."
    ],
    "kill": [
        "Murderer of processes! Its zombie state shall haunt your PID table forever.",
        "SIGTERM was ignored. Only the blood of SIGKILL satisfies the kernel reaper."
    ],
    "default": [
        "The machine shivers as the electron winds whisper...",
        "A phantom thread executed in ring 0. Did you hear that interrupt?",
        "Your keystrokes rattle like old bones against iron switches."
    ]
}

def generate_spectral_response(command_str):
    cmd = command_str.strip().split()[0].lower() if command_str.strip() else ""
    whisper_pool = EERIE_WHISPERS.get(cmd, EERIE_WHISPERS["default"])
    whisper = random.choice(whisper_pool)
    persona = random.choice(GHOST_PERSONAS)
    return {
        "command": command_str,
        "whisper": whisper,
        "persona": persona["name"],
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PhantomShell - The Haunted AI Terminal</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @keyframes flicker {
            0%, 100% { opacity: 0.98; }
            50% { opacity: 0.88; }
            70% { opacity: 0.95; }
            85% { opacity: 0.82; }
        }
        .crt-glow {
            text-shadow: 0 0 8px rgba(74, 222, 128, 0.6), 0 0 20px rgba(74, 222, 128, 0.3);
            animation: flicker 0.15s infinite;
        }
        .scanlines {
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
            background-size: 100% 3px, 3px 100%;
            pointer-events: none;
        }
    </style>
</head>
<body class="bg-black text-emerald-400 font-mono min-h-screen flex flex-col relative overflow-hidden select-none">
    <div class="scanlines absolute inset-0 z-40"></div>

    <header class="border-b border-emerald-950/80 bg-zinc-950/90 p-4 flex justify-between items-center z-10">
        <div class="flex items-center space-x-3">
            <span class="text-xl crt-glow"><i class="fa-solid fa-ghost"></i></span>
            <div>
                <h1 class="text-sm font-bold tracking-widest text-emerald-300 uppercase flex items-center gap-2">
                    PHANTOM-SHELL // v0.4.0-SPECTRAL
                    <span class="text-[10px] bg-emerald-950 text-emerald-400 border border-emerald-800 px-2 py-0.5 rounded">Día de los Muertos Edition</span>
                </h1>
                <p class="text-[10px] text-emerald-700">Open-Source AI Ghost In The Machine • 100% Offline Possession</p>
            </div>
        </div>
        <div class="text-[11px] text-emerald-600 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>
            <span>SPIRIT LINK: CONNECTED (ZERO CLOUD EGRESS)</span>
        </div>
    </header>

    <main class="flex-1 p-6 max-w-4xl w-full mx-auto flex flex-col justify-between z-10 overflow-hidden">
        <!-- Terminal Output Screen -->
        <div id="terminalScreen" class="flex-1 bg-zinc-950/80 border border-emerald-950 rounded-xl p-5 overflow-y-auto space-y-3 shadow-[0_0_30px_rgba(5,46,22,0.4)] text-xs leading-relaxed">
            <div class="text-emerald-700 border-b border-emerald-950 pb-2">
                [SYSTEM READY] The machine is inhabited. Type any command (e.g., 'ls', 'git commit', 'rm -rf', 'cat /etc/shadow'). Listen to the whispers of ancient code.
            </div>
        </div>

        <!-- Terminal Input Bar -->
        <div class="mt-4 bg-zinc-950 border border-emerald-900 rounded-xl p-3 flex items-center space-x-2">
            <span class="text-emerald-500 font-bold">spirit@machine:~$</span>
            <input id="cliInput" type="text" placeholder="whisper a shell command..." autofocus autocomplete="off" class="flex-1 bg-transparent text-emerald-300 outline-none font-mono text-xs placeholder-emerald-900">
            <button onclick="sendCommand()" class="px-3 py-1 bg-emerald-950 hover:bg-emerald-900 text-emerald-300 border border-emerald-800 rounded text-xs transition">Invoke</button>
        </div>
    </main>

    <script>
        const screen = document.getElementById('terminalScreen');
        const input = document.getElementById('cliInput');

        async function sendCommand() {
            const val = input.value.trim();
            if (!val) return;
            input.value = '';

            // User command echo
            const echo = document.createElement('div');
            echo.className = "text-emerald-300 font-bold";
            echo.innerHTML = `<span class="text-emerald-600">$&gt;</span> ${val}`;
            screen.appendChild(echo);

            // Fetch spectral possession response
            const res = await fetch('/api/whisper', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ command: val })
            });
            const data = await res.json();

            // Spectral whisper output
            const ghostMsg = document.createElement('div');
            ghostMsg.className = "pl-4 border-l-2 border-emerald-800 text-emerald-400/90 italic space-y-1 my-2 bg-emerald-950/20 py-2 rounded-r";
            ghostMsg.innerHTML = `
                <div class="text-[10px] text-emerald-600 uppercase font-sans tracking-wider">[Ghost: ${data.persona}] [${data.timestamp}]</div>
                <div class="crt-glow font-mono">"${data.whisper}"</div>
            `;
            screen.appendChild(ghostMsg);
            screen.scrollTop = screen.scrollHeight;
        }

        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') sendCommand();
        });
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/whisper", methods=["POST"])
def whisper():
    data = request.json or {}
    cmd = data.get("command", "")
    return jsonify(generate_spectral_response(cmd))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)
