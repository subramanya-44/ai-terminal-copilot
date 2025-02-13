#!/bin/zsh

# Function to intercept commands
command_intercept() {
    local command="$1"
    
    # Skip empty commands, comments, or commands starting with space
    if [[ -z "$command" ]] || \
       [[ "$command" =~ ^[[:space:]]*([#]|$) ]] || \
       [[ "$command" == "command_intercept"* ]] || \
       [[ "$command" == "ai_terminal_assistant"* ]]; then
        return
    fi
    
    # Get the directory where the script is located
    SCRIPT_DIR="${0:A:h}"
    
    # Extract the actual command without comments
    local actual_command=$(echo "$command" | sed 's/[[:space:]]*#.*//g')
    
    # Call the Node.js CLI tool to process the command
    echo "🔍 Analyzing command: $actual_command"
    node "$SCRIPT_DIR/index.js" "$actual_command"
}

# Set up the preexec hook for Zsh
autoload -Uz add-zsh-hook
add-zsh-hook preexec command_intercept

# Print setup message
echo "🤖 AI Terminal Assistant is now active!"
echo "💡 Tip: Add a space before a command to skip AI analysis"