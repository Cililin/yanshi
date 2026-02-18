package com.yanshi.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;
import com.yanshi.dto.ExtractionProgressDTO;
import com.yanshi.dto.ExtractionResultDTO;
import com.yanshi.dto.MergeResultDTO;
import com.yanshi.entity.*;
import com.yanshi.mapper.*;
import com.yanshi.service.KnowledgeExtractionService;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.*;

/**
 * AI知识点抽取服务实现
 */
@Service
public class KnowledgeExtractionServiceImpl implements KnowledgeExtractionService {

    @Value("${ai.qwen.api-key}")
    private String apiKey;

    @Value("${ai.python.path:python}")
    private String pythonPath;

    @Value("${ai.script.path:crawler/ai_extract.py}")
    private String scriptPath;

    private final ArticleMapper articleMapper;
    private final KnowledgePointMapper knowledgePointMapper;
    private final ArticleKnowledgeRelationMapper relationMapper;
    private final ObjectMapper objectMapper;

    public KnowledgeExtractionServiceImpl(
            ArticleMapper articleMapper,
            KnowledgePointMapper knowledgePointMapper,
            ArticleKnowledgeRelationMapper relationMapper) {
        this.articleMapper = articleMapper;
        this.knowledgePointMapper = knowledgePointMapper;
        this.relationMapper = relationMapper;
        this.objectMapper = new ObjectMapper();
    }

    @Override
    @Transactional
    public List<KnowledgePoint> extractFromArticle(Long articleId) {
        // 1. 获取文章
        Article article = articleMapper.selectById(articleId);
        if (article == null) {
            return Collections.emptyList();
        }

        // 2. 调用Python脚本抽取
        List<Map<String, Object>> rawPoints = callPythonExtract(
            article.getTitle(),
            article.getContent()
        );

        // 3. 转换为实体对象
        List<KnowledgePoint> points = rawPoints.stream()
            .map(this::mapToKnowledgePoint)
            .collect(java.util.stream.Collectors.toList());

        // 4. 去重并保存
        deduplicateAndSave(points, articleId);

        return points;
    }

    @Override
    @Transactional
    public ExtractionResultDTO extractBatch(List<Long> articleIds) {
        ExtractionResultDTO result = new ExtractionResultDTO();
        result.setTotalCount(articleIds.size());

        for (Long articleId : articleIds) {
            try {
                extractFromArticle(articleId);
                result.setSuccessCount(result.getSuccessCount() + 1);
            } catch (Exception e) {
                result.setFailedCount(result.getFailedCount() + 1);
                result.getErrors().add("Article " + articleId + ": " + e.getMessage());
            }
        }

        return result;
    }

    @Override
    @Transactional
    public MergeResultDTO deduplicateAndSave(List<KnowledgePoint> points, Long articleId) {
        MergeResultDTO result = new MergeResultDTO();

        for (KnowledgePoint point : points) {
            // 1. 查找相似知识点
            List<KnowledgePoint> similar = knowledgePointMapper.findSimilarPoints(
                point.getName(),
                point.getCategory()
            );

            KnowledgePoint target;
            if (similar.isEmpty()) {
                // 新知识点，直接保存
                point.setFirstSeenAt(LocalDateTime.now());
                point.setLastSeenAt(LocalDateTime.now());
                point.setArticleCount(1);
                knowledgePointMapper.insert(point);
                target = point;
                result.incrementNew();
            } else {
                // 合并到已有知识点
                target = similar.get(0);
                mergeKnowledgePoint(target, point);
                knowledgePointMapper.updateById(target);
                result.incrementMerged();
            }

            // 2. 创建关联关系
            createRelation(articleId, target.getId());
        }

        return result;
    }

    @Override
    public ExtractionProgressDTO getProgress() {
        ExtractionProgressDTO progress = new ExtractionProgressDTO();
        // TODO: 从extraction_tasks表统计
        return progress;
    }

    private List<Map<String, Object>> callPythonExtract(String title, String content) {
        try {
            // 构建命令：python 脚本 api-key title content
            String command = String.format("%s %s %s \"%s\"",
                pythonPath,
                scriptPath,
                apiKey,
                escapeForShell(title),
                escapeForShell(content != null ? content.substring(0, 2000) : "")
            );

            Process process = Runtime.getRuntime().exec(command);

            BufferedReader reader = new BufferedReader(
                new InputStreamReader(process.getInputStream())
            );

            StringBuilder result = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                result.append(line);
            }

            process.waitFor();

            // 解析JSON
            return objectMapper.readValue(
                result.toString(),
                new TypeReference<List<Map<String, Object>>>() {}
            );

        } catch (Exception e) {
            throw new RuntimeException("AI抽取失败: " + e.getMessage(), e);
        }
    }

    private KnowledgePoint mapToKnowledgePoint(Map<String, Object> map) {
        KnowledgePoint point = new KnowledgePoint();
        point.setName((String) map.get("name"));
        point.setType((String) map.get("type"));
        point.setCategory((String) map.get("category"));
        point.setDescription((String) map.get("description"));

        // 重要性分数：将1-10转换为0-100
        Object importance = map.get("importance");
        if (importance instanceof Integer) {
            BigDecimal score = BigDecimal.valueOf((Integer) importance * 10.0);
            point.setImportanceScore(score);
        }

        return point;
    }

    private void mergeKnowledgePoint(KnowledgePoint existing, KnowledgePoint newPoint) {
        // 1. 更新出现次数
        existing.setArticleCount(existing.getArticleCount() + 1);

        // 2. 更新最后出现时间
        existing.setLastSeenAt(LocalDateTime.now());

        // 3. 取最大重要性
        if (newPoint.getImportanceScore().compareTo(existing.getImportanceScore()) > 0) {
            existing.setImportanceScore(newPoint.getImportanceScore());
        }

        // 4. 合并描述
        if (newPoint.getDescription() != null && !newPoint.getDescription().isEmpty()) {
            if (existing.getDescription() == null || existing.getDescription().isEmpty()) {
                existing.setDescription(newPoint.getDescription());
            }
        }
    }

    private void createRelation(Long articleId, Long knowledgePointId) {
        // 检查是否已存在关联
        ArticleKnowledgeRelation existing = relationMapper.selectOne(
            new LambdaQueryWrapper<ArticleKnowledgeRelation>()
                .eq(ArticleKnowledgeRelation::getArticleId, articleId)
                .eq(ArticleKnowledgeRelation::getKnowledgePointId, knowledgePointId)
        );

        if (existing == null) {
            // 创建新关联
            ArticleKnowledgeRelation relation = new ArticleKnowledgeRelation();
            relation.setArticleId(articleId);
            relation.setKnowledgePointId(knowledgePointId);
            relation.setRelevance(new BigDecimal("0.50"));
            relationMapper.insert(relation);
        }
    }

    private String escapeForShell(String input) {
        if (input == null) {
            return "";
        }
        // 简单的转义，实际项目中可能需要更完善的处理
        return input.replace("\"", "\\\"").replace("'", "\\'");
    }
}
