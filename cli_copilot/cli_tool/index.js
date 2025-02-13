require('dotenv').config();
const axios = require('axios');
const chalk = require('chalk');

const API_URL = process.env.API_URL || 'http://localhost:8000';

async function analyzeCommand(command) {
    if (!command) {
        console.error(chalk.red('Error: No command provided'));
        return;
    }

    // Add command correction suggestions
    const commonCommands = {
        'la': 'ls',
        'pop': 'pip',
        'gti': 'git',
        'sl': 'ls'
    };

    // Check for common typos
    const firstWord = command.split(' ')[0];
    if (commonCommands[firstWord]) {
        const correctedCommand = command.replace(firstWord, commonCommands[firstWord]);
        console.log(chalk.yellow('\n⚠️  Did you mean:'), chalk.green(correctedCommand), '?');
        command = correctedCommand;
    }

    try {
        const response = await axios.post(`${API_URL}/process_command`, {
            command,
            context: {
                cwd: process.cwd(),
                shell: process.env.SHELL
            }
        });

        if (response.data.success) {
            console.log(chalk.bold('\n🤖 AI Terminal Assistant'));
            console.log(chalk.gray('━'.repeat(40)));
            console.log(formatResponse(response.data.analysis));
            console.log(chalk.gray('━'.repeat(40)));
        } else {
            console.log(chalk.red('\n❌ Error:'), response.data.error);
        }
    } catch (error) {
        if (error.code === 'ECONNREFUSED') {
            console.log(chalk.red('\n❌ Error: Backend server is not running'));
            console.log(chalk.yellow('💡 Start the server with: uvicorn main:app --reload'));
        } else {
            console.error(chalk.red('\n❌ Error:'), error.message);
        }
    }
}

function formatResponse(analysis) {
    const sections = analysis.split(/\n(?=\d️⃣)/);
    return sections.map(section => {
        const [title, ...content] = section.split('\n');
        return `${chalk.green(title)}\n${chalk.blue(content.join('\n'))}`;
    }).join('\n\n');
}

// Get the command from command line arguments
const command = process.argv[2];
analyzeCommand(command);

module.exports = { analyzeCommand };