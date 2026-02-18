package com.yanshi.dto;

/**
 * 抽取进度DTO
 */
public class ExtractionProgressDTO {
    private int pendingCount;
    private int processingCount;
    private int completedCount;
    private int failedCount;

    public ExtractionProgressDTO() {
        this.pendingCount = 0;
        this.processingCount = 0;
        this.completedCount = 0;
        this.failedCount = 0;
    }

    public int getPendingCount() { return pendingCount; }
    public void setPendingCount(int pendingCount) { this.pendingCount = pendingCount; }

    public int getProcessingCount() { return processingCount; }
    public void setProcessingCount(int processingCount) { this.processingCount = processingCount; }

    public int getCompletedCount() { return completedCount; }
    public void setCompletedCount(int completedCount) { this.completedCount = completedCount; }

    public int getFailedCount() { return failedCount; }
    public void setFailedCount(int failedCount) { this.failedCount = failedCount; }
}
