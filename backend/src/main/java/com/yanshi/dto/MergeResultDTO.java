package com.yanshi.dto;

/**
 * 合并结果DTO
 */
public class MergeResultDTO {
    private int newCount;
    private int mergedCount;

    public MergeResultDTO() {
        this.newCount = 0;
        this.mergedCount = 0;
    }

    public int getNewCount() { return newCount; }
    public void setNewCount(int newCount) { this.newCount = newCount; }

    public int getMergedCount() { return mergedCount; }
    public void setMergedCount(int mergedCount) { this.mergedCount = mergedCount; }

    public void incrementNew() { newCount++; }
    public void incrementMerged() { mergedCount++; }
}
