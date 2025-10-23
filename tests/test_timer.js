/**
 * Unit tests for PomodoroTimer
 * Tests timer functionality and state management
 */

const PomodoroTimer = require('../timer.js');

describe('PomodoroTimer', () => {
    let timer;

    beforeEach(() => {
        timer = new PomodoroTimer(25, 5);
    });

    afterEach(() => {
        if (timer) {
            timer.pause();
        }
    });

    test('should initialize with correct default values', () => {
        expect(timer.workDuration).toBe(25 * 60);
        expect(timer.breakDuration).toBe(5 * 60);
        expect(timer.currentTime).toBe(25 * 60);
        expect(timer.isRunning).toBe(false);
        expect(timer.isWorkSession).toBe(true);
    });

    test('should initialize with custom durations', () => {
        const customTimer = new PomodoroTimer(30, 10);
        expect(customTimer.workDuration).toBe(30 * 60);
        expect(customTimer.breakDuration).toBe(10 * 60);
        expect(customTimer.currentTime).toBe(30 * 60);
    });

    test('should start the timer', () => {
        timer.start();
        expect(timer.isRunning).toBe(true);
        expect(timer.isActive()).toBe(true);
    });

    test('should pause the timer', () => {
        timer.start();
        timer.pause();
        expect(timer.isRunning).toBe(false);
        expect(timer.isActive()).toBe(false);
    });

    test('should not start if already running', () => {
        timer.start();
        const firstIntervalId = timer.intervalId;
        timer.start();
        expect(timer.intervalId).toBe(firstIntervalId);
    });

    test('should reset timer to current session duration', () => {
        timer.currentTime = 100;
        timer.reset();
        expect(timer.currentTime).toBe(25 * 60);
        expect(timer.isRunning).toBe(false);
    });

    test('should decrement time on tick', () => {
        const initialTime = timer.currentTime;
        timer.tick();
        expect(timer.currentTime).toBe(initialTime - 1);
    });

    test('should return correct current time', () => {
        expect(timer.getCurrentTime()).toBe(25 * 60);
        timer.currentTime = 100;
        expect(timer.getCurrentTime()).toBe(100);
    });

    test('should format time correctly', () => {
        timer.currentTime = 125; // 2 minutes 5 seconds
        expect(timer.getFormattedTime()).toBe('02:05');
        
        timer.currentTime = 3661; // 61 minutes 1 second
        expect(timer.getFormattedTime()).toBe('61:01');
        
        timer.currentTime = 0;
        expect(timer.getFormattedTime()).toBe('00:00');
    });

    test('should return work session status', () => {
        expect(timer.isWorkTime()).toBe(true);
        timer.isWorkSession = false;
        expect(timer.isWorkTime()).toBe(false);
    });

    test('should switch to break session when work timer completes', () => {
        timer.currentTime = 0;
        timer.onTimerComplete();
        expect(timer.isWorkSession).toBe(false);
        expect(timer.currentTime).toBe(5 * 60);
        expect(timer.isRunning).toBe(false);
    });

    test('should switch to work session when break timer completes', () => {
        timer.isWorkSession = false;
        timer.currentTime = 0;
        timer.onTimerComplete();
        expect(timer.isWorkSession).toBe(true);
        expect(timer.currentTime).toBe(25 * 60);
        expect(timer.isRunning).toBe(false);
    });

    test('should set work duration and update current time if in work session', () => {
        timer.setWorkDuration(30);
        expect(timer.workDuration).toBe(30 * 60);
        expect(timer.currentTime).toBe(30 * 60);
    });

    test('should set work duration but not update current time if in break session', () => {
        timer.isWorkSession = false;
        timer.currentTime = 5 * 60;
        timer.setWorkDuration(30);
        expect(timer.workDuration).toBe(30 * 60);
        expect(timer.currentTime).toBe(5 * 60);
    });

    test('should set break duration and update current time if in break session', () => {
        timer.isWorkSession = false;
        timer.currentTime = 5 * 60;
        timer.setBreakDuration(10);
        expect(timer.breakDuration).toBe(10 * 60);
        expect(timer.currentTime).toBe(10 * 60);
    });

    test('should set break duration but not update current time if in work session', () => {
        timer.setBreakDuration(10);
        expect(timer.breakDuration).toBe(10 * 60);
        expect(timer.currentTime).toBe(25 * 60);
    });

    test('should handle multiple start/pause cycles', () => {
        timer.start();
        expect(timer.isRunning).toBe(true);
        
        timer.pause();
        expect(timer.isRunning).toBe(false);
        
        timer.start();
        expect(timer.isRunning).toBe(true);
        
        timer.pause();
        expect(timer.isRunning).toBe(false);
    });

    test('should maintain time across pause/resume', () => {
        timer.currentTime = 100;
        timer.start();
        timer.pause();
        expect(timer.currentTime).toBe(100);
        
        timer.start();
        expect(timer.currentTime).toBe(100);
    });
});
