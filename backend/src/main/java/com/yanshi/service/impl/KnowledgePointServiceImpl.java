package com.yanshi.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.yanshi.entity.ArticleKnowledgeRelation;
import com.yanshi.entity.KnowledgePoint;
import com.yanshi.mapper.KnowledgePointMapper;
import com.yanshi.service.KnowledgePointService;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * 知识点服务实现
 */
@Service
public class KnowledgePointServiceImpl extends ServiceImpl<KnowledgePointMapper, KnowledgePoint>
        implements KnowledgePointService {

    private final KnowledgePointMapper knowledgePointMapper;
    private final com.yanshi.mapper.ArticleKnowledgeRelationMapper relationMapper;

    public KnowledgePointServiceImpl(KnowledgePointMapper knowledgePointMapper,
                                       com.yanshi.mapper.ArticleKnowledgeRelationMapper relationMapper) {
        this.knowledgePointMapper = knowledgePointMapper;
        this.relationMapper = relationMapper;
    }

    @Override
    public List<KnowledgePoint> getAll() {
        return knowledgePointMapper.selectList(null);
    }

    @Override
    public List<KnowledgePoint> getByCategory(String category) {
        return knowledgePointMapper.selectList(
            new LambdaQueryWrapper<KnowledgePoint>()
                .eq(KnowledgePoint::getCategory, category)
                .orderByDesc(KnowledgePoint::getImportanceScore)
        );
    }

    @Override
    public List<KnowledgePoint> getTopLevel() {
        return knowledgePointMapper.selectList(
            new LambdaQueryWrapper<KnowledgePoint>()
                .isNull(KnowledgePoint::getParentId)
                .orderByDesc(KnowledgePoint::getImportanceScore)
        );
    }

    @Override
    public KnowledgePoint getById(Long id) {
        return knowledgePointMapper.selectById(id);
    }

    @Override
    public IPage<KnowledgePoint> getPage(Page<KnowledgePoint> page, String type, String category) {
        return knowledgePointMapper.selectPage(page,
            new LambdaQueryWrapper<KnowledgePoint>()
                .eq(type != null && !type.isEmpty(), KnowledgePoint::getType, type)
                .eq(category != null && !category.isEmpty(), KnowledgePoint::getCategory, category)
                .orderByDesc(KnowledgePoint::getImportanceScore)
        );
    }

    @Override
    public IPage<KnowledgePoint> search(Page<KnowledgePoint> page, String keyword, String type, String category) {
        return knowledgePointMapper.search(page, keyword, type, category);
    }

    @Override
    public List<ArticleKnowledgeRelation> getArticlesByPointId(Long pointId) {
        return relationMapper.getByKnowledgePointId(pointId);
    }

    @Override
    public List<KnowledgePoint> getByArticleId(Long articleId) {
        return knowledgePointMapper.getByArticleId(articleId);
    }

    @Override
    public List<KnowledgePoint> getTopPoints(int limit) {
        return knowledgePointMapper.getTopPoints(limit);
    }

    @Override
    public List<KnowledgePoint> countByCategory() {
        return knowledgePointMapper.countByCategory();
    }
}
