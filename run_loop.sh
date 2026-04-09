#!/bin/bash
# =============================================================================
# CERTX Autonomous Research Loop Runner
# =============================================================================
# Invokes a Claude Code session to run one iteration of the research loop.
#
# USAGE:
#   Manual:     bash run_loop.sh
#   Cron:       0 */3 * * * /home/user/CERTX/run_loop.sh >> /home/user/CERTX/loop.log 2>&1
#   Systemd:    See notes below
#
# TIMING:
#   Every 3 hours → one session
#   6 active sessions + 1 DREAM = one full breath (18 hours)
# =============================================================================

set -e

REPO_DIR="/home/user/CERTX"
LOG_FILE="${REPO_DIR}/loop.log"
PROMPT_FILE="${REPO_DIR}/loop_prompt.md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "========================================" | tee -a "$LOG_FILE"
echo "CERTX Loop Session — $TIMESTAMP" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"

# Navigate to repo
cd "$REPO_DIR"

# Ensure we're on the right branch
CURRENT_BRANCH=$(git branch --show-current)
echo "Branch: $CURRENT_BRANCH" | tee -a "$LOG_FILE"

# Pull latest changes before starting
echo "Fetching latest..." | tee -a "$LOG_FILE"
git fetch origin claude/plan-certx-architecture-ojiem 2>&1 | tee -a "$LOG_FILE" || echo "Fetch failed, continuing with local state" | tee -a "$LOG_FILE"

# Read the current session handoff for context
echo "" | tee -a "$LOG_FILE"
echo "Current session handoff:" | tee -a "$LOG_FILE"
echo "--- HANDOFF START ---" | tee -a "$LOG_FILE"
head -50 SESSION_HANDOFF.md | tee -a "$LOG_FILE"
echo "--- HANDOFF END ---" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Run the Claude Code session
# NOTE: This invokes claude with the loop prompt as the task
# The --print flag runs non-interactively
echo "Starting Claude Code session..." | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Invoke claude with the loop prompt
# Adjust the claude command path if needed (which claude to find it)
CLAUDE_CMD=$(which claude 2>/dev/null || echo "claude")

if command -v claude &> /dev/null; then
    claude --print "$(cat "$PROMPT_FILE")" 2>&1 | tee -a "$LOG_FILE"
    EXIT_CODE=${PIPESTATUS[0]}
else
    echo "ERROR: claude command not found. Is Claude Code installed?" | tee -a "$LOG_FILE"
    echo "Install with: npm install -g @anthropic-ai/claude-code" | tee -a "$LOG_FILE"
    exit 1
fi

echo "" | tee -a "$LOG_FILE"
echo "Session completed with exit code: $EXIT_CODE" | tee -a "$LOG_FILE"
echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

exit $EXIT_CODE

# =============================================================================
# CRON SETUP (run 'crontab -e' and add one of these lines):
#
# Every 3 hours:
#   0 */3 * * * /home/user/CERTX/run_loop.sh >> /home/user/CERTX/loop.log 2>&1
#
# Every 4 hours:
#   0 */4 * * * /home/user/CERTX/run_loop.sh >> /home/user/CERTX/loop.log 2>&1
#
# Every 2 hours (faster cycling, more sessions per day):
#   0 */2 * * * /home/user/CERTX/run_loop.sh >> /home/user/CERTX/loop.log 2>&1
#
# =============================================================================
# SYSTEMD TIMER SETUP (alternative to cron):
#
# Create /etc/systemd/system/certx-loop.service:
#   [Unit]
#   Description=CERTX Research Loop Session
#
#   [Service]
#   Type=oneshot
#   User=user
#   WorkingDirectory=/home/user/CERTX
#   ExecStart=/home/user/CERTX/run_loop.sh
#
# Create /etc/systemd/system/certx-loop.timer:
#   [Unit]
#   Description=CERTX Research Loop Timer
#
#   [Timer]
#   OnBootSec=5min
#   OnUnitActiveSec=3h
#   Unit=certx-loop.service
#
#   [Install]
#   WantedBy=timers.target
#
# Enable with:
#   systemctl enable certx-loop.timer
#   systemctl start certx-loop.timer
# =============================================================================
