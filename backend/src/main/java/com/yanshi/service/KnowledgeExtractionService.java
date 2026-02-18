package com.yanshi.service;

import com.yanshi.dto.ExtractionProgressDTO;
import com.yanshi.dto.ExtractionResultDTO;
import com.yanshi.dto.MergeResultDTO;
import com.yanshi.entity.KnowledgePoint;

import java.util.List;

/**
 * AI知识点抽取服务接口
 */
public interface KnowledgeExtractionService {

    /**
     * 从文章中抽取知识点
     */
    List<KnowledgePoint> extractFromArticle(Long articleId);

    /**
     * 批量抽取（用于定时任务）
     */
    ExtractionResultDTO extractBatch(List<Long> articleIds);

    /**
     * 去重并保存知识点
     */
    MergeResultDTO deduplicateAndSave(List<KnowledgePoint> points, Long articleId);

    /**
     * 获取抽取进度
     */
    ExtractionProgressDTO getProgress();
}
