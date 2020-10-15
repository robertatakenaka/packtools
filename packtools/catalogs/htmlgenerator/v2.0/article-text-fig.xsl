<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml"
    version="1.0">

    <xsl:template match="fig | fig-group">
        <!--
        Cria a miniatura no texto completo, que ao ser clicada mostra a figura
        ampliada
        --> 
        <xsl:variable name="location">
            <xsl:apply-templates select="alternatives | graphic" mode="file-location-thumb"/>
        </xsl:variable>
        <xsl:variable name="figid">
            <xsl:choose>
                <xsl:when test="@id"><xsl:value-of select="@id"/></xsl:when>
                <xsl:otherwise>IDMISSING</xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <div class="row fig" id="{$figid}">
            <a name="{$figid}"></a>
            <div class="col-md-4 col-sm-4">
                <a href="" data-toggle="modal" data-target="#ModalFig{$figid}">
                    <div>
                        <xsl:choose>
                            <xsl:when test="$location != ''">
                                <xsl:attribute name="class">thumb</xsl:attribute>
                                <xsl:attribute name="style">background-image: url(<xsl:value-of select="$location"/>);</xsl:attribute>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="class">thumbOff</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
                        Thumbnail
                        <div class="zoom"><span class="sci-ico-zoom"></span></div>
                    </div>
                </a>
            </div>
            <div class="col-md-8 col-sm-8">
                <xsl:apply-templates select="." mode="label-caption-thumb"></xsl:apply-templates>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="fig-group" mode="label-caption">
        <xsl:apply-templates select="fig[@xml:lang=$TEXT_LANG]" mode="label-caption"></xsl:apply-templates>
    </xsl:template>

</xsl:stylesheet>