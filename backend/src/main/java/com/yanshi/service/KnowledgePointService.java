package com.yanshi.service;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.yanshi.entity.KnowledgePoint;
import com.yanshi.entity.ArticleKnowledgeRelation;

import java.util.List;

/**
 * 知识点服务接口
 */
public interface KnowledgePointService {

    // 基础查询
    List<KnowledgePoint> getAll();

    List<KnowledgePoint> getByCategory(String category);

    List<KnowledgePoint> getTopLevel();

    KnowledgePoint getById(Long id);

    // 分页查询
    IPage<KnowledgePoint> getPage(Page<KnowledgePoint> page,
                                    String type,
                                    String category);

    // 搜索
    IPage<KnowledgePoint> search(Page<KnowledgePoint> page,
                                   String keyword,
                                   String type,
                                   String category);

    // 获取知识点关联的文章
    List<ArticleKnowledgeRelation> getArticlesByPointId(Long pointId);

    // 获取文章的知识点
    List<KnowledgePoint> getByArticleId(Long articleId);

    // 获取热门知识点
    List<KnowledgePoint> getTopPoints(int limit);

    // 按分类统计
    List<KnowledgePoint> countByCategory();
}
