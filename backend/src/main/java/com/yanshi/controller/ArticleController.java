package com.yanshi.controller;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.yanshi.common.Result;
import com.yanshi.dto.ArticleQueryDTO;
import com.yanshi.dto.ArticleStatisticsDTO;
import com.yanshi.entity.Article;
import com.yanshi.service.ArticleService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

/**
 * 文章控制器
 */
@RestController
@RequestMapping("/articles")
@Tag(name = "文章管理", description = "文章相关接口")
public class ArticleController {

    private static final Logger log = LoggerFactory.getLogger(ArticleController.class);

    private final ArticleService articleService;

    public ArticleController(ArticleService articleService) {
        this.articleService = articleService;
    }

    @GetMapping
    @Operation(summary = "分页查询文章列表")
    public Result<IPage<Article>> getArticlePage(ArticleQueryDTO query) {
        log.info("查询文章列表: {}", query);
        IPage<Article> page = articleService.getArticlePage(query);
        return Result.success(page);
    }

    @GetMapping("/{id}")
    @Operation(summary = "查询文章详情")
    public Result<Article> getArticleById(@PathVariable Long id) {
        log.info("查询文章详情: id={}", id);
        Article article = articleService.getArticleById(id);
        if (article == null) {
            return Result.error("文章不存在");
        }
        return Result.success(article);
    }

    @GetMapping("/recent")
    @Operation(summary = "获取最新文章")
    public Result<List<Article>> getRecentArticles(
            @RequestParam(defaultValue = "10") Integer limit) {
        log.info("获取最新文章: limit={}", limit);
        List<Article> articles = articleService.getRecentArticles(limit);
        return Result.success(articles);
    }

    @GetMapping("/statistics")
    @Operation(summary = "获取文章统计信息")
    public Result<ArticleStatisticsDTO> getStatistics() {
        log.info("获取文章统计信息");
        ArticleStatisticsDTO statistics = articleService.getStatistics();
        return Result.success(statistics);
    }

    @GetMapping("/statistics/source")
    @Operation(summary = "按来源统计文章")
    public Result<List<Map<String, Object>>> countBySource() {
        log.info("按来源统计文章");
        List<Map<String, Object>> result = articleService.countBySource();
        return Result.success(result);
    }

    @GetMapping("/statistics/category")
    @Operation(summary = "按分类统计文章")
    public Result<List<Map<String, Object>>> countByCategory() {
        log.info("按分类统计文章");
        List<Map<String, Object>> result = articleService.countByCategory();
        return Result.success(result);
    }

    @GetMapping("/statistics/date")
    @Operation(summary = "按日期统计文章")
    public Result<List<Map<String, Object>>> countByDate(
            @RequestParam(required = false) String startDate,
            @RequestParam(required = false) String endDate) {
        log.info("按日期统计文章: startDate={}, endDate={}", startDate, endDate);
        List<Map<String, Object>> result = articleService.countByDate(startDate, endDate);
        return Result.success(result);
    }
}
