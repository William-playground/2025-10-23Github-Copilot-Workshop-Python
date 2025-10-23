/**
 * Pomodoro Timer Module
 * Handles timer logic and integrates with API for progress tracking
 */

class PomodoroTimer {
    constructor() {
        this.POMODORO_TIME = 25 * 60; // 25 minutes in seconds
        this.timeRemaining = this.POMODORO_TIME;
        this.isRunning = false;
        this.timerInterval = null;
        
        // Progress tracking
        this.completedCount = 0;
        this.totalFocusTime = 0; // in minutes
        
        // UI elements
        this.timerDisplay = document.getElementById('timer-display');
        this.startButton = document.getElementById('start-button');
        this.resetButton = document.getElementById('reset-button');
        this.completedCountDisplay = document.getElementById('completed-count');
        this.focusTimeDisplay = document.getElementById('focus-time');
        
        this.initializeEventListeners();
        this.loadProgress();
    }

    /**
     * Initialize button event listeners
     */
    initializeEventListeners() {
        if (this.startButton) {
            this.startButton.addEventListener('click', () => this.toggleTimer());
        }
        
        if (this.resetButton) {
            this.resetButton.addEventListener('click', () => this.resetTimer());
        }
    }

    /**
     * Load progress data from server on page load
     */
    async loadProgress() {
        try {
            const data = await API.getProgress();
            this.completedCount = data.completed_count || 0;
            this.totalFocusTime = data.total_focus_time || 0;
            this.updateProgressDisplay();
        } catch (error) {
            console.error('Failed to load progress:', error);
        }
    }

    /**
     * Toggle timer start/pause
     */
    toggleTimer() {
        if (this.isRunning) {
            this.pauseTimer();
        } else {
            this.startTimer();
        }
    }

    /**
     * Start the timer
     */
    startTimer() {
        this.isRunning = true;
        if (this.startButton) {
            this.startButton.textContent = '一時停止';
        }
        
        this.timerInterval = setInterval(() => {
            this.timeRemaining--;
            this.updateTimerDisplay();
            
            if (this.timeRemaining <= 0) {
                this.completePomodoro();
            }
        }, 1000);
    }

    /**
     * Pause the timer
     */
    pauseTimer() {
        this.isRunning = false;
        if (this.startButton) {
            this.startButton.textContent = '開始';
        }
        clearInterval(this.timerInterval);
    }

    /**
     * Reset the timer
     */
    resetTimer() {
        this.pauseTimer();
        this.timeRemaining = this.POMODORO_TIME;
        this.updateTimerDisplay();
    }

    /**
     * Handle timer completion
     */
    async completePomodoro() {
        this.pauseTimer();
        this.timeRemaining = this.POMODORO_TIME;
        
        // Update progress
        this.completedCount++;
        this.totalFocusTime += 25; // 25 minutes per pomodoro
        
        // Update UI
        this.updateTimerDisplay();
        this.updateProgressDisplay();
        
        // Save progress to server
        try {
            await API.saveProgress({
                completed_count: this.completedCount,
                total_focus_time: this.totalFocusTime
            });
            console.log('Pomodoro completed and progress saved!');
        } catch (error) {
            console.error('Failed to save progress:', error);
            alert('進捗の保存に失敗しました。');
        }
    }

    /**
     * Update timer display
     */
    updateTimerDisplay() {
        if (!this.timerDisplay) return;
        
        const minutes = Math.floor(this.timeRemaining / 60);
        const seconds = this.timeRemaining % 60;
        this.timerDisplay.textContent = 
            `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }

    /**
     * Update progress display
     */
    updateProgressDisplay() {
        if (this.completedCountDisplay) {
            this.completedCountDisplay.textContent = this.completedCount;
        }
        
        if (this.focusTimeDisplay) {
            this.focusTimeDisplay.textContent = `${this.totalFocusTime}分`;
        }
    }
}

// Initialize timer when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.pomodoroTimer = new PomodoroTimer();
});
