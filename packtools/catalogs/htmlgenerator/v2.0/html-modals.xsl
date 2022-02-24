<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="article" mode="article-modals">
        <!--
            Cria todos os modals do documento
        -->
        <xsl:variable name="translation" select=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']"/>

        <!-- modal do contribs -->
        <xsl:apply-templates select="." mode="modal-contribs"/>

        <!-- modal que apresenta juntos figuras, tabelas e fórmulas -->
        <xsl:apply-templates select="." mode="modal-grouped-figs-tables-schemes"/>

        <!-- cria um modal para cada figura, tabela e fórmula existente no body-->
        <xsl:apply-templates select="front" mode="individual-modal"/>

        <xsl:choose>
            <xsl:when test="$translation">
                <xsl:apply-templates select="$translation" mode="individual-modal"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="body" mode="individual-modal"/>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:apply-templates select="back" mode="individual-modal"/>

        <!-- cria um modal para como citar -->
        <xsl:apply-templates select="." mode="modal-how2cite"/>
    </xsl:template>

    <xsl:template match="front | body | back | sub-article" mode="individual-modal">
        <!-- cria um modal para cada figura, tabela e fórmula existente no body-->
        <xsl:apply-templates select=".//*[fig]" mode="fig-modal"></xsl:apply-templates>
        <xsl:apply-templates select=".//table-wrap[@id] | .//table-wrap-group[@id]" mode="modal"/>
        <xsl:apply-templates select=".//disp-formula[@id]" mode="modal"/>
    </xsl:template>

    <xsl:template match="article" mode="modal-grouped-figs-tables-schemes">
        <!--
            Modal que apresenta juntos figuras, tabelas e fórmulas presentes
            em um dado idioma do texto do artigo
        -->
        <!-- FIXME -->
        <xsl:variable name="total_figs">
            <xsl:apply-templates select="." mode="get-total-figs"/>
        </xsl:variable>
        <xsl:variable name="total_tables">
            <xsl:apply-templates select="." mode="get-total-tables"/>
        </xsl:variable>
        <xsl:variable name="total_formulas">
            <xsl:apply-templates select="." mode="get-total-formulas"/>
        </xsl:variable>

        <xsl:if test="number($total_figs) + number($total_tables) + number($total_formulas) &gt; 0">
             <div class="modal fade ModalDefault" id="ModalTablesFigures" tabindex="-1" role="dialog" aria-hidden="true">
                 <div class="modal-dialog">
                     <div class="modal-content">
                         <div class="modal-header">
                             <button type="button" class="close" data-dismiss="modal">
                                 <span aria-hidden="true">&#xd7;</span>
                                 <span class="sr-only">
                                     <xsl:apply-templates select="." mode="interface">
                                         <xsl:with-param name="text">Close</xsl:with-param>
                                     </xsl:apply-templates>
                                 </span>
                             </button>
                             <h4 class="modal-title"><xsl:value-of select="$graphic_elements_title"/></h4>
                         </div>
                         <div class="modal-body">
                             <ul class="nav nav-tabs md-tabs" role="tablist">
                                <xsl:if test="number($total_figs) &gt; 0">
                                    <!--
                                        cria aba com rótulo "Figures" e quantidade de figuras
                                    -->
                                    <li role="presentation" class="col-md-4 col-sm-4 active">
                                         <a href="#figures" aria-controls="figures" role="tab" data-toggle="tab">
                                             <xsl:apply-templates select="." mode="interface">
                                                 <xsl:with-param name="text">Figures</xsl:with-param>
                                             </xsl:apply-templates>
                                             (<xsl:value-of select="$total_figs"/>)
                                         </a>
                                     </li>
                                 </xsl:if>
                                 <xsl:if test="number($total_tables) &gt; 0">
                                     <!--
                                        cria aba com rótulo "Tables" e quantidade de tabelas
                                    -->
                                     <li role="presentation">
                                         <xsl:attribute name="class">col-md-4 col-sm-4 <xsl:if test="number($total_figs) = 0"> active</xsl:if></xsl:attribute>
                                         <a href="#tables" aria-controls="tables" role="tab" data-toggle="tab">
                                             <xsl:apply-templates select="." mode="interface">
                                                 <xsl:with-param name="text">Tables</xsl:with-param>
                                             </xsl:apply-templates>
                                             (<xsl:value-of select="$total_tables"/>)
                                         </a>
                                     </li>
                                 </xsl:if>
                                 <xsl:if test="number($total_formulas) &gt; 0">
                                     <!--
                                        cria aba com rótulo "Scheme" e quantidade de fórmulas
                                    -->
                                     <li role="presentation">
                                         <xsl:attribute name="class">col-md-4 col-sm-4<xsl:if test="number($total_figs) + number($total_tables) = 0"> active</xsl:if></xsl:attribute>

                                         <a href="#schemes" aria-controls="schemes" role="tab" data-toggle="tab">
                                             <xsl:apply-templates select="." mode="interface">
                                                 <xsl:with-param name="text">Formulas</xsl:with-param>
                                             </xsl:apply-templates>
                                             (<xsl:value-of select="$total_formulas"/>)
                                         </a>
                                     </li>
                                 </xsl:if>
                             </ul>
                             <div class="clearfix"></div>
                             <div class="tab-content">
                                 <xsl:if test="number($total_figs) &gt; 0">
                                    <!--
                                        cria o conteúdo da aba com rótulo "Figures"
                                    -->
                                     <div role="tabpanel" class="tab-pane active" id="figures">
                                         <xsl:apply-templates select="." mode="generic-tab-content">
                                            <xsl:with-param name="tab_content_type">figures</xsl:with-param>
                                         </xsl:apply-templates>
                                     </div>
                                 </xsl:if>
                                 <xsl:if test="number($total_tables) &gt; 0">
                                    <!--
                                        cria o conteúdo da aba com rótulo "Tables"
                                    -->
                                     <div role="tabpanel">
                                         <xsl:attribute name="class">tab-pane <xsl:if test="number($total_figs) = 0"> active</xsl:if></xsl:attribute>
                                         <xsl:attribute name="id">tables</xsl:attribute>

                                         <xsl:apply-templates select="." mode="generic-tab-content">
                                            <xsl:with-param name="tab_content_type">tables</xsl:with-param>
                                         </xsl:apply-templates>
                                     </div>
                                 </xsl:if>
                                 <xsl:if test="number($total_formulas) &gt; 0">
                                    <!--
                                        cria o conteúdo da aba com rótulo "Formulas"
                                    -->
                                     <div role="tabpanel">
                                         <xsl:attribute name="class">tab-pane <xsl:if test="number($total_figs) + number($total_tables) = 0"> active</xsl:if></xsl:attribute>
                                         <xsl:attribute name="id">schemes</xsl:attribute>

                                         <xsl:apply-templates select="." mode="generic-tab-content">
                                            <xsl:with-param name="tab_content_type">schemes</xsl:with-param>
                                         </xsl:apply-templates>
                                     </div>
                                 </xsl:if>
                             </div>
                         </div>
                     </div>
                 </div>
             </div>
         </xsl:if>
    </xsl:template>

    <xsl:template match="article" mode="generic-tab-content">
        <xsl:param name="tab_content_type"/>

        <xsl:variable name="translation" select=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']"/>

        <xsl:choose>
            <xsl:when test="$translation">
                <xsl:apply-templates select="front | $translation | back" mode="generic-tab-content">
                    <xsl:with-param name="tab_content_type" select="$tab_content_type"/>
                </xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="front | body | back" mode="generic-tab-content">
                    <xsl:with-param name="tab_content_type" select="$tab_content_type"/>
                </xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="sub-article | front | body | back" mode="generic-tab-content">
        <xsl:param name="tab_content_type"/>
        <!--
        Seleciona os elementos que contém "fig",
        para criar o conteúdo de cada fig no Modal na aba "Figures"
        -->
        <xsl:choose>
            <xsl:when test="$tab_content_type='figures'">
                <xsl:apply-templates select=".//*[fig]" mode="figs-tab-content"/>
            </xsl:when>
            <xsl:when test="$tab_content_type='tables'">
                <xsl:apply-templates select=".//table-wrap-group[table-wrap] | .//*[table-wrap and name()!='table-wrap-group']/table-wrap" mode="tab-content"/>
            </xsl:when>
            <xsl:when test="$tab_content_type='schemes'">
                <xsl:apply-templates select=".//disp-formula[@id]" mode="tab-content"/>
            </xsl:when>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="*[fig]" mode="fig-modal">
        <!--
        cria o conteúdo de uma figura no Modal na aba "Figures"
        -->
        <xsl:choose>
            <xsl:when test="name()='fig-group'">
                <xsl:apply-templates select="." mode="modal"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select=".//fig" mode="modal"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="*[fig]" mode="figs-tab-content">
        <!--
        cria o conteúdo de uma figura no Modal na aba "Figures"
        -->
        <xsl:choose>
            <xsl:when test="name()='fig-group'">
                <xsl:apply-templates select="." mode="tab-content"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select=".//fig" mode="tab-content"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="fig-group[@id] | fig" mode="tab-content">
        <!--
            Para fig-group e fig, cria no conteúdo da ABA "Figures":
            - a miniatura

            Para fig-group:
            - legendas de uma figura (label e caption em mais de um idioma)

            Para fig:
            - legenda de uma figura (label e caption em um idioma)
        -->
        <div class="row fig">
            <!-- miniatura -->
            <xsl:variable name="location">
                <xsl:apply-templates select="alternatives | graphic" mode="file-location-thumb"/>
            </xsl:variable>
            <div class="col-md-4">
                <a data-toggle="modal" data-target="#ModalFig{@id}">
                    <div>
                        <xsl:choose>
                            <xsl:when test="$location != ''">
                                <xsl:attribute name="class">thumbImg</xsl:attribute>
                                <img>
                                    <xsl:attribute name="src"><xsl:value-of select="$location"/></xsl:attribute>
                                </img>
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
            <!-- legenda(s) -->
            <xsl:apply-templates select="." mode="tab-content-label-and-caption"></xsl:apply-templates>
        </div>
    </xsl:template>

    <xsl:template match="fig-group | table-wrap-group" mode="tab-content-label-and-caption">
        <!--
            cria as legendas de uma figura no conteúdo da ABA "Figures"
            cria no conteúdo da ABA "Tables" as legendas de uma tabela
        -->
        <xsl:apply-templates select="fig | table-wrap" mode="tab-content-label-and-caption"/>
    </xsl:template>

    <xsl:template match="fig | table-wrap" mode="tab-content-label-and-caption">
        <!--
            Cria a legenda de uma figura no conteúdo da ABA "Figures" ou
            Cria a legenda de uma tabela no conteúdo da ABA "Tables"
        -->
        <div class="col-md-8">
            <xsl:apply-templates select="." mode="label-caption-thumb"></xsl:apply-templates>
        </div>
    </xsl:template>

    <xsl:template match="table-wrap-group[table-wrap] | table-wrap[not(@xml:lang)]" mode="tab-content">
        <!--
            Para table-wrap-group e table-wrap, cria no conteúdo da ABA "Tables":
            - a miniatura

            Para table-wrap-group:
            - legendas de uma tabela em mais de 1 idioma
            Para table-wrap:
            - legenda de uma tabela em 1 idioma
        -->
        <div class="row table">
            <!-- miniatura -->
            <div class="col-md-4">
                <a data-toggle="modal" data-target="#ModalTable{@id}">
                    <div class="thumbOff">
                        Thumbnail
                        <div class="zoom"><span class="sci-ico-zoom"></span></div>
                    </div>
                </a>
            </div>
            <!-- legenda -->
            <xsl:apply-templates select="." mode="tab-content-label-and-caption"></xsl:apply-templates>
        </div>
    </xsl:template>

    <xsl:template match="disp-formula[@id]" mode="tab-content">
        <!--
            cria no conteúdo da ABA "Scheme" a miniatura e legenda de uma fórmula
        -->
        <div class="row fig">
            <!-- miniatura -->
            <xsl:variable name="location"><xsl:apply-templates select="." mode="file-location"/></xsl:variable>
            <div class="col-md-4">
                <a data-toggle="modal" data-target="#ModalScheme{@id}">
                    <div>
                        <xsl:choose>
                            <xsl:when test="graphic">
                                <xsl:attribute name="class">thumbImg</xsl:attribute>
                                <img>
                                    <xsl:attribute name="src"><xsl:value-of select="$location"/></xsl:attribute>
                                </img>
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
            <!-- legenda -->
            <xsl:apply-templates select="." mode="tab-content-label-and-caption"></xsl:apply-templates>
        </div>
    </xsl:template>

    <xsl:template match="disp-formula[@id]" mode="tab-content-label-and-caption">
        <!--
            cria no conteúdo da ABA "Schemes" a legenda de uma fórmula
        -->
        <div class="col-md-8">
            <xsl:apply-templates select="label"></xsl:apply-templates>
        </div>
    </xsl:template>

    <xsl:template match="article" mode="get-total-figs">
        <xsl:variable name="translation" select=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']"/>

        <xsl:variable name="f"><xsl:apply-templates select="front" mode="get-total-figs"/></xsl:variable>
        <xsl:variable name="bk"><xsl:apply-templates select="back" mode="get-total-figs"/></xsl:variable>
        <xsl:variable name="b">
        <xsl:choose>
            <xsl:when test="$translation">
                <xsl:apply-templates select="$translation" mode="get-total-figs"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="body" mode="get-total-figs"/>
            </xsl:otherwise>
        </xsl:choose>
        </xsl:variable>
        <xsl:value-of select="number($f)+number($b)+number($bk)"/>
    </xsl:template>

    <xsl:template match="article" mode="get-total-tables">
        <xsl:variable name="translation" select=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']"/>

        <xsl:variable name="f"><xsl:apply-templates select="front" mode="get-total-tables"/></xsl:variable>
        <xsl:variable name="bk"><xsl:apply-templates select="back" mode="get-total-tables"/></xsl:variable>
        <xsl:variable name="b">
        <xsl:choose>
            <xsl:when test="$translation">
                <xsl:apply-templates select="$translation" mode="get-total-tables"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="body" mode="get-total-tables"/>
            </xsl:otherwise>
        </xsl:choose>
        </xsl:variable>
        <xsl:value-of select="number($f)+number($b)+number($bk)"/>
    </xsl:template>

    <xsl:template match="sub-article | front | body | back" mode="get-total-figs">
        <xsl:value-of select="count(.//fig-group[@id]/fig[@xml:lang][1]) + count(.//fig[not(@xml:lang)])"/>
    </xsl:template>

    <xsl:template match="sub-article | front | body | back" mode="get-total-tables">
        <xsl:value-of select="count(.//table-wrap-group) + count(.//*[table-wrap and name()!='table-wrap-group']//table-wrap)"/>
    </xsl:template>

    <xsl:template match="sub-article | front | body | back" mode="get-total-formulas">
        <xsl:value-of select="count(.//disp-formula[@id])"/>
    </xsl:template>
</xsl:stylesheet>