/**
 * Node.js wrapper to run Python scraper
 * Usage: node run-scraper.js [--once|--export|--stats]
 */

import { exec } from 'child_process';
import { promisify } from 'util';

const execPromise = promisify(exec);

async function runScraper(args = []) {
    try {
        const pythonCmd = args.includes('--once')
            ? 'python scraper/main.py --once'
            : args.includes('--export')
                ? 'python scraper/exporter.py --all'
                : args.includes('--stats')
                    ? 'python scraper/exporter.py --stats'
                    : 'python scraper/main.py';

        console.log(`\n📡 Running: ${pythonCmd}\n`);

        const { stdout, stderr } = await execPromise(pythonCmd, {
            cwd: process.cwd(),
            maxBuffer: 10 * 1024 * 1024 // 10MB buffer
        });

        if (stdout) console.log(stdout);
        if (stderr) console.error(stderr);

        console.log('\n✅ Scraper completed!\n');
    } catch (error) {
        console.error('\n❌ Error:', error.message);
        process.exit(1);
    }
}

// Run the scraper
const args = process.argv.slice(2);
runScraper(args);
