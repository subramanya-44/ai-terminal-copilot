from typing import Dict, Any
import shlex

def parse_command(command_str: str) -> Dict[str, Any]:
    """Parse a shell command string into structured format."""
    try:
        # Use shlex to properly handle quoted arguments and escapes
        args = shlex.split(command_str)
        
        if not args:
            return {
                "success": False,
                "error": "Empty command",
                "command": command_str
            }
        
        command_info = {
            "success": True,
            "command": args[0],  # The actual command
            "args": args[1:],    # Command arguments
            "raw": command_str,  # Original command string
            "is_sudo": args[0] == "sudo"
        }
        
        # If it's a sudo command, adjust the command info
        if command_info["is_sudo"] and len(args) > 1:
            command_info["command"] = args[1]
            command_info["args"] = args[2:]
        
        return command_info
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "command": command_str
        }

def is_dangerous_command(command_info: Dict[str, Any]) -> bool:
    """Check if a command is potentially dangerous."""
    dangerous_commands = {
        "rm": "-rf" in command_info.get("args", []) or "--force" in command_info.get("args", []),
        "chmod": "777" in command_info.get("args", []),
        "dd": True,  # dd is always considered potentially dangerous
        "mkfs": True,
        "fdisk": True
    }
    
    return dangerous_commands.get(command_info["command"], False)