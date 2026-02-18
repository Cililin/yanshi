package com.yanshi.dto;

import java.util.List;

/**
 * 抽取结果DTO
 */
public class ExtractionResultDTO {
    private int totalCount;
    private int successCount;
    private int failedCount;
    private List<String> errors;

    public ExtractionResultDTO() {
        this.totalCount = 0;
        this.successCount = 0;
        this.failedCount = 0;
        this.errors = new java.util.ArrayList<>();
    }

    public int getTotalCount() { return totalCount; }
    public void setTotalCount(int totalCount) { this.totalCount = totalCount; }

    public int getSuccessCount() { return successCount; }
    public void setSuccessCount(int successCount) { this.successCount = successCount; }

    public int getFailedCount() { return failedCount; }
    public void setFailedCount(int failedCount) { this.failedCount = failedCount; }

    public List<String> getErrors() { return errors; }
    public void setErrors(List<String> errors) { this.errors = errors; }
}
