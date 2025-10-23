/**
 * API Communication Module
 * Handles all API calls to the backend server for progress data management
 */

const API = {
    /**
     * Base URL for API endpoints
     */
    baseURL: '/api',

    /**
     * Save progress data to the server
     * @param {Object} progressData - The progress data to save
     * @param {number} progressData.completed_count - Number of completed pomodoros
     * @param {number} progressData.total_focus_time - Total focus time in minutes
     * @returns {Promise<Object>} - Response from the server
     */
    async saveProgress(progressData) {
        try {
            const response = await fetch(`${this.baseURL}/progress`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(progressData)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log('Progress saved successfully:', data);
            return data;
        } catch (error) {
            console.error('Error saving progress:', error);
            throw error;
        }
    },

    /**
     * Get current progress data from the server
     * @returns {Promise<Object>} - Current progress data
     */
    async getProgress() {
        try {
            const response = await fetch(`${this.baseURL}/progress`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log('Progress retrieved successfully:', data);
            return data;
        } catch (error) {
            console.error('Error getting progress:', error);
            throw error;
        }
    },

    /**
     * Reset progress data on the server
     * @returns {Promise<Object>} - Response from the server
     */
    async resetProgress() {
        try {
            const response = await fetch(`${this.baseURL}/progress/reset`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log('Progress reset successfully:', data);
            return data;
        } catch (error) {
            console.error('Error resetting progress:', error);
            throw error;
        }
    }
};

// Export for use in other modules (if using module system)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = API;
}
