package com.yanshi.controller;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.yanshi.common.Result;
import com.yanshi.entity.ArticleKnowledgeRelation;
import com.yanshi.entity.KnowledgePoint;
import com.yanshi.service.KnowledgePointService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 知识点控制器
 */
@RestController
@RequestMapping("/knowledge-points")
@Tag(name = "知识点管理", description = "知识点相关接口")
public class KnowledgePointController {

    private static final Logger log = LoggerFactory.getLogger(KnowledgePointController.class);

    private final KnowledgePointService knowledgePointService;

    public KnowledgePointController(KnowledgePointService knowledgePointService) {
        this.knowledgePointService = knowledgePointService;
    }

    @GetMapping
    @Operation(summary = "分页查询知识点")
    public Result<IPage<KnowledgePoint>> getPage(
            @RequestParam(defaultValue = "1") Integer page,
            @RequestParam(defaultValue = "20") Integer pageSize,
            @RequestParam(required = false) String type,
            @RequestParam(required = false) String category) {
        log.info("分页查询知识点: page={}, pageSize={}, type={}, category={}", page, pageSize, type, category);
        Page<KnowledgePoint> pageParam = new Page<>(page, pageSize);
        IPage<KnowledgePoint> result = knowledgePointService.getPage(pageParam, type, category);
        return Result.success(result);
    }

    @GetMapping("/search")
    @Operation(summary = "搜索知识点")
    public Result<IPage<KnowledgePoint>> search(
            @RequestParam String keyword,
            @RequestParam(defaultValue = "1") Integer page,
            @RequestParam(defaultValue = "20") Integer pageSize,
            @RequestParam(required = false) String type,
            @RequestParam(required = false) String category) {
        log.info("搜索知识点: keyword={}, page={}, pageSize={}", keyword, page, pageSize);
        Page<KnowledgePoint> pageParam = new Page<>(page, pageSize);
        IPage<KnowledgePoint> result = knowledgePointService.search(pageParam, keyword, type, category);
        return Result.success(result);
    }

    @GetMapping("/category/{category}")
    @Operation(summary = "根据分类查询知识点")
    public Result<List<KnowledgePoint>> getByCategory(@PathVariable String category) {
        log.info("根据分类查询知识点: category={}", category);
        List<KnowledgePoint> list = knowledgePointService.getByCategory(category);
        return Result.success(list);
    }

    @GetMapping("/top")
    @Operation(summary = "获取热门知识点")
    public Result<List<KnowledgePoint>> getTopPoints(@RequestParam(defaultValue = "20") Integer limit) {
        log.info("获取热门知识点: limit={}", limit);
        List<KnowledgePoint> list = knowledgePointService.getTopPoints(limit);
        return Result.success(list);
    }

    @GetMapping("/stats")
    @Operation(summary = "获取知识点统计")
    public Result<List<KnowledgePoint>> getStats() {
        log.info("获取知识点统计");
        List<KnowledgePoint> stats = knowledgePointService.countByCategory();
        return Result.success(stats);
    }

    @GetMapping("/{id}")
    @Operation(summary = "根据ID查询知识点")
    public Result<KnowledgePoint> getById(@PathVariable Long id) {
        log.info("根据ID查询知识点: id={}", id);
        KnowledgePoint point = knowledgePointService.getById(id);
        if (point == null) {
            return Result.error("知识点不存在");
        }
        return Result.success(point);
    }

    @GetMapping("/{id}/articles")
    @Operation(summary = "获取知识点关联的文章")
    public Result<List<ArticleKnowledgeRelation>> getArticles(@PathVariable Long id) {
        log.info("获取知识点关联的文章: id={}", id);
        List<ArticleKnowledgeRelation> relations = knowledgePointService.getArticlesByPointId(id);
        return Result.success(relations);
    }

    @GetMapping("/article/{articleId}")
    @Operation(summary = "获取文章的知识点")
    public Result<List<KnowledgePoint>> getByArticleId(@PathVariable Long articleId) {
        log.info("获取文章的知识点: articleId={}", articleId);
        List<KnowledgePoint> points = knowledgePointService.getByArticleId(articleId);
        return Result.success(points);
    }
}
