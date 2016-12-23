<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <h2>Tuits Sobre Interjet</h2>
  <table border="3">
    <tr bgcolor=" #0315ac">
      <th style="text-align:center">Text</th>
      <th style="text-align:center">Sentimiento</th>
      <th style="text-align:center">Día</th>
    </tr>
    <xsl:for-each select="tuits/tuit">
    <tr>
      <td><xsl:value-of select="text" /></td>
      <td><xsl:value-of select="sent" /></td>
      <td><xsl:value-of select="day" /></td>
    </tr>
    </xsl:for-each>
  </table>
</xsl:template>
</xsl:stylesheet> 


***************************************************************
<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<tuits>
	<tuit>
		<text>@interjet DM para mensaje directo soy el PR de @laloariaswuu #Ladywuuu</text>
		<sent>NEUTRA</sent>
		<day>Martes</day>
	</tuit>
	<tuit>
		<text>RT @interjet: Estamos buscando a Mika, multiplicamos todos nuestros esfuerzos para localizarla. #BuscandoaMika https://t.co/7HbGOUZcqJ</text>
		<sent>NEUTRA</sent>
		<day>Martes</day>
	</tuit>
</tuits>
