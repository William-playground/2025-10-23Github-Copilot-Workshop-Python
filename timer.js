/**
 * Pomodoro Timer Logic
 * Manages timer state and countdown functionality
 */

class PomodoroTimer {
    constructor(workDuration = 25, breakDuration = 5) {
        this.workDuration = workDuration * 60; // Convert to seconds
        this.breakDuration = breakDuration * 60; // Convert to seconds
        this.currentTime = this.workDuration;
        this.isRunning = false;
        this.isWorkSession = true;
        this.intervalId = null;
    }

    start() {
        if (!this.isRunning) {
            this.isRunning = true;
            this.intervalId = setInterval(() => this.tick(), 1000);
        }
    }

    pause() {
        if (this.isRunning) {
            this.isRunning = false;
            if (this.intervalId) {
                clearInterval(this.intervalId);
                this.intervalId = null;
            }
        }
    }

    reset() {
        this.pause();
        this.currentTime = this.isWorkSession ? this.workDuration : this.breakDuration;
    }

    tick() {
        if (this.currentTime > 0) {
            this.currentTime--;
        } else {
            this.onTimerComplete();
        }
    }

    onTimerComplete() {
        this.pause();
        this.isWorkSession = !this.isWorkSession;
        this.currentTime = this.isWorkSession ? this.workDuration : this.breakDuration;
    }

    getCurrentTime() {
        return this.currentTime;
    }

    getFormattedTime() {
        const minutes = Math.floor(this.currentTime / 60);
        const seconds = this.currentTime % 60;
        return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }

    isActive() {
        return this.isRunning;
    }

    isWorkTime() {
        return this.isWorkSession;
    }

    setWorkDuration(minutes) {
        this.workDuration = minutes * 60;
        if (this.isWorkSession) {
            this.currentTime = this.workDuration;
        }
    }

    setBreakDuration(minutes) {
        this.breakDuration = minutes * 60;
        if (!this.isWorkSession) {
            this.currentTime = this.breakDuration;
        }
    }
}

// Export for Node.js testing environment
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PomodoroTimer;
}
