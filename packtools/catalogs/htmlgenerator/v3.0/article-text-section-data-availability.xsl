<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/article-text-section-data-availability.xsl"/>

    <xsl:template match="article | sub-article" mode="doc-version-data-availability">
        <xsl:apply-templates select="body | back" mode="data-availability"/>
    </xsl:template>

    <xsl:template match="article" mode="data-availability">
        <xsl:choose>
            <xsl:when test="sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']">
                <!-- sub-article -->
                <xsl:apply-templates select="sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']" mode="doc-version-data-availability"/>
            </xsl:when>
            <xsl:otherwise>
                <!-- article -->
                <xsl:apply-templates select="." mode="doc-version-data-availability"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="body | back" mode="data-availability">
        <xsl:apply-templates select="sec//sec[@sec-type='data-availability']" mode="back-section"/>
    </xsl:template>

</xsl:stylesheet>