<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink" >
    
    <xsl:variable name="q_abstracts"><xsl:apply-templates select="article" mode="count_abstracts"></xsl:apply-templates></xsl:variable>
    <xsl:variable name="q_back"><xsl:apply-templates select="article" mode="count_back_elements"></xsl:apply-templates></xsl:variable>
    <xsl:variable name="q_body_fn"><xsl:apply-templates select="article" mode="count_body_fn"></xsl:apply-templates></xsl:variable>
    <xsl:variable name="q_subarticle"><xsl:apply-templates select="article" mode="count_subarticle"></xsl:apply-templates></xsl:variable>
    <xsl:variable name="q_history">1</xsl:variable>
    <xsl:variable name="body_index"><xsl:value-of select="$q_abstracts"/></xsl:variable>
    
    <xsl:template match="article" mode="count_abstracts">
        <xsl:choose>
            <xsl:when test=".//sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]">
                <xsl:apply-templates select=".//sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]" mode="count_abstracts"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select=".//article-meta" mode="count_abstracts"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="*" mode="count_abstracts">
        <xsl:value-of select="count(.//abstract)+count(.//trans-abstract)"></xsl:value-of>
    </xsl:template>
    
    <xsl:template match="article" mode="count_back_elements">
        <xsl:choose>
            <xsl:when test=".//sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]">
                <xsl:apply-templates select=".//sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]" mode="count_back_elements"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="count(back/*)"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="article" mode="count_subarticle">
        <xsl:value-of select="count(.//sub-article[@article-type!='translation' and @xml:lang=$TEXT_LANG])"/>
    </xsl:template>
    
    <xsl:template match="article" mode="count_body_fn">
        <xsl:choose>
            <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG]//body//p/fn">1</xsl:when>
            <xsl:when test="./body//p/fn">1</xsl:when>
            <xsl:otherwise>0</xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="sub-article[@article-type='translation']" mode="count_back_elements">
        <xsl:choose>
            <xsl:when test="back/ref-list">
                <xsl:value-of select="count(back/*)"/>
            </xsl:when>
            <xsl:when test="../back/ref-list">
                <xsl:value-of select="count(back/*)+1"/>
            </xsl:when>
            <xsl:otherwise><xsl:value-of select="count(back/*)"/></xsl:otherwise>
        </xsl:choose>       
    </xsl:template>
        
    <xsl:template match="*" mode="text-body">
        <div class="articleSection">
            <xsl:attribute name="data-anchor"><xsl:choose>
                <xsl:when test=".//abstract"><xsl:apply-templates select="body" mode="generated-label"/></xsl:when>
                <xsl:otherwise><xsl:apply-templates select="." mode="text-labels">
                    <xsl:with-param name="text" select="@article-type"/>
                </xsl:apply-templates></xsl:otherwise>
            </xsl:choose></xsl:attribute>
            <!-- FIXME: body ou sub-article/body -->
            <a name="articleSection{$body_index}"/>
            <xsl:choose>
                <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG]">
                    <xsl:apply-templates select=".//sub-article[@xml:lang=$TEXT_LANG]//body/*"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:apply-templates select="./body/*"/>                    
                </xsl:otherwise>
            </xsl:choose>            
        </div>
    </xsl:template>
    
    <xsl:template match="sec[@sec-type]" mode="number">
        <xsl:param name="sec_id"/>
        <xsl:if test="@sec-type=$sec_id"><xsl:value-of select="number(position()-1)"/></xsl:if>
    </xsl:template>
    
    <xsl:template match="body" mode="number">
        <xsl:param name="sec_id"/>
        <xsl:apply-templates select=".//sec[@sec-type]" mode="number">
            <xsl:with-param name="sec_id"><xsl:value-of select="$sec_id"/></xsl:with-param>
        </xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="body/sec[@sec-type]">
        <xsl:variable name="item"><xsl:apply-templates select="../../body" mode="number">
            <xsl:with-param name="sec_id"><xsl:value-of select="@sec-type"/></xsl:with-param>
        </xsl:apply-templates></xsl:variable>
        <a name="as{$body_index}-heading{$item}"/>
        
        <xsl:apply-templates select="*|text()"/>
    </xsl:template>
    
    <xsl:template match="body/sec/title">
        <h1>
            <xsl:apply-templates select="*|text()"/>
        </h1>
    </xsl:template>
    
    <xsl:template match="body/sec[@sec-type]/title">
        <h1 id="text-{../@sec-type}">
            <xsl:apply-templates select="*|text()"/>
        </h1>
    </xsl:template>
    
    <xsl:template match="body/sec/sec/title">
        <xsl:param name="position"></xsl:param>
        
        <h2>
            <xsl:apply-templates select="*|text()"/>
        </h2>
    </xsl:template>
            
    <xsl:template match="sig-block">
        <p class="articleSignature">
            <xsl:apply-templates select="*"></xsl:apply-templates>
        </p>
    </xsl:template>
    
    <xsl:template match="sig">
        <xsl:choose>
            <xsl:when test="position()=1">
                <xsl:apply-templates></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <small><xsl:apply-templates></xsl:apply-templates></small>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
</xsl:stylesheet>