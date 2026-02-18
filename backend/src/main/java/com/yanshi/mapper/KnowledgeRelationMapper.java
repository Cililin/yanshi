package com.yanshi.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;

/**
 * 知识点关联Mapper接口
 */
@Mapper
public interface KnowledgeRelationMapper extends BaseMapper<com.yanshi.entity.KnowledgeRelation> {

    /**
     * 获取知识点的关系
     */
    List<com.yanshi.entity.KnowledgeRelation> getRelationsByPointId(Long pointId);
}
