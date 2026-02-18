package com.yanshi.controller;

import com.yanshi.common.Result;
import com.yanshi.dto.ExtractionProgressDTO;
import com.yanshi.dto.ExtractionResultDTO;
import com.yanshi.entity.KnowledgePoint;
import com.yanshi.service.KnowledgeExtractionService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * AI知识抽取控制器
 */
@RestController
@RequestMapping("/knowledge-extraction")
@Tag(name = "AI知识抽取", description = "AI知识抽取相关接口")
public class KnowledgeExtractionController {

    private static final Logger log = LoggerFactory.getLogger(KnowledgeExtractionController.class);

    private final KnowledgeExtractionService extractionService;

    public KnowledgeExtractionController(KnowledgeExtractionService extractionService) {
        this.extractionService = extractionService;
    }

    @PostMapping("/extract/{articleId}")
    @Operation(summary = "从单篇文章抽取知识点")
    public Result<List<KnowledgePoint>> extract(@PathVariable Long articleId) {
        log.info("从文章抽取知识点: articleId={}", articleId);
        try {
            List<KnowledgePoint> points = extractionService.extractFromArticle(articleId);
            return Result.success(points);
        } catch (Exception e) {
            log.error("抽取失败", e);
            return Result.error("抽取失败: " + e.getMessage());
        }
    }

    @PostMapping("/extract/batch")
    @Operation(summary = "批量抽取知识点")
    public Result<ExtractionResultDTO> extractBatch(@RequestBody List<Long> articleIds) {
        log.info("批量抽取知识点: count={}", articleIds.size());
        try {
            ExtractionResultDTO result = extractionService.extractBatch(articleIds);
            return Result.success(result);
        } catch (Exception e) {
            log.error("批量抽取失败", e);
            return Result.error("批量抽取失败: " + e.getMessage());
        }
    }

    @GetMapping("/progress")
    @Operation(summary = "获取抽取进度")
    public Result<ExtractionProgressDTO> getProgress() {
        log.info("获取抽取进度");
        ExtractionProgressDTO progress = extractionService.getProgress();
        return Result.success(progress);
    }
}
