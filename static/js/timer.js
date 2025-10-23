// タイマークラス
class PomodoroTimer {
    constructor() {
        // DOM要素の取得
        this.timerDisplay = document.getElementById('timerDisplay');
        this.timerProgress = document.getElementById('timerProgress');
        this.startBtn = document.getElementById('startBtn');
        this.resetBtn = document.getElementById('resetBtn');
        
        // タイマー設定（25分 = 1500秒）
        this.totalTime = 25 * 60; // 25分を秒で表現
        this.timeRemaining = this.totalTime;
        this.isRunning = false;
        this.intervalId = null;
        
        // 円の円周（半径90の円）
        this.circleCircumference = 2 * Math.PI * 90; // 565.48
        
        // イベントリスナーの設定
        this.setupEventListeners();
        
        // 初期表示の更新
        this.updateDisplay();
        this.updateProgress();
    }
    
    // イベントリスナーの設定
    setupEventListeners() {
        this.startBtn.addEventListener('click', () => this.toggleTimer());
        this.resetBtn.addEventListener('click', () => this.reset());
    }
    
    // タイマーの開始・一時停止
    toggleTimer() {
        if (this.isRunning) {
            this.pause();
        } else {
            this.start();
        }
    }
    
    // タイマー開始
    start() {
        this.isRunning = true;
        this.startBtn.textContent = '一時停止';
        this.startBtn.classList.add('paused');
        
        this.intervalId = setInterval(() => {
            this.timeRemaining--;
            
            if (this.timeRemaining <= 0) {
                this.complete();
            } else {
                this.updateDisplay();
                this.updateProgress();
            }
        }, 1000);
    }
    
    // タイマー一時停止
    pause() {
        this.isRunning = false;
        this.startBtn.textContent = '開始';
        this.startBtn.classList.remove('paused');
        
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
    }
    
    // タイマーリセット
    reset() {
        this.pause();
        this.timeRemaining = this.totalTime;
        this.updateDisplay();
        this.updateProgress();
        this.startBtn.textContent = '開始';
    }
    
    // タイマー完了
    complete() {
        this.pause();
        this.timeRemaining = 0;
        this.updateDisplay();
        this.updateProgress();
        alert('ポモドーロ完了！お疲れ様でした！');
    }
    
    // 表示の更新
    updateDisplay() {
        const minutes = Math.floor(this.timeRemaining / 60);
        const seconds = this.timeRemaining % 60;
        
        // 2桁表示にフォーマット
        const formattedMinutes = String(minutes).padStart(2, '0');
        const formattedSeconds = String(seconds).padStart(2, '0');
        
        this.timerDisplay.textContent = `${formattedMinutes}:${formattedSeconds}`;
    }
    
    // 円グラフの進捗更新
    updateProgress() {
        // 残り時間の割合を計算
        const progress = this.timeRemaining / this.totalTime;
        
        // stroke-dashoffsetを計算（残り時間に応じて円を描画）
        const offset = this.circleCircumference * (1 - progress);
        
        this.timerProgress.style.strokeDashoffset = offset;
    }
}

// DOMが読み込まれたらタイマーを初期化
document.addEventListener('DOMContentLoaded', () => {
    new PomodoroTimer();
});
