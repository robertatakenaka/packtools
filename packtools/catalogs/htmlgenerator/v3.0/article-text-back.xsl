<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/article-text-back.xsl"/>

    <xsl:template match="*[title] | *[label] | *[@fn-type] | corresp" mode="back-section-menu">
        <xsl:variable name="name" select="@fn-type"/>
        <!-- cria menu somente para o primeiro ref-list (há casos de série de ref-list) -->       
        <xsl:if test="not(preceding-sibling::node()) or preceding-sibling::*[1][@fn-type!=$name]">
            <!-- manter pareado class="articleSection" e data-anchor="nome da seção no menu esquerdo" -->
            <xsl:attribute name="class">articleSection</xsl:attribute>
            <xsl:attribute name="data-anchor">
                <xsl:apply-templates select="." mode="back-section-title"/>
            </xsl:attribute>
        </xsl:if>
    </xsl:template>

    <xsl:template match="*" mode="author-notes-content">
        <xsl:apply-templates select="*[name()!='label']|text()"/>
    </xsl:template>

</xsl:stylesheet>