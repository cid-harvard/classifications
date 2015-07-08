Original data from INEGI’s Marco Geoestadistico Nacional: “Catálogo Único de
Claves de Áreas Geoestadísticas Estatales, Municipales y Localidades”.

Main page: http://www.inegi.org.mx/geo/contenidos/geoestadistica/catalogoclaves.aspx
Downloads page: http://geoweb.inegi.org.mx/mgn2k/catalogo.jsp
File link: http://geoweb.inegi.org.mx/mgn2kData/catalogos/cat_localidad_MAY2015.zip

File was unzipped and converted from dbf to csv with:`ogr2ogr -f “csv”
cat_localidad_MAY2015.csv cat_localidad_MAY2015.dbf -lco ENCODING=”latin-2”`.
