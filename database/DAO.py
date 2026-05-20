from database.DB_connect import DBConnect
from model.artista import Artista
from model.compensi import Compensi
from model.genere import Genere


class DAO():
    @staticmethod
    def getAllGeneri():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """SELECT *
                    FROM genre"""
        cursor.execute(query)

        result = []

        for row in cursor:
            result.append(Genere(**row))

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getAllArtisti():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """select * 
                    from artist a"""
        cursor.execute(query)

        result = []

        for row in cursor:
            result.append(Artista(**row))

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getArtisti(genere):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """select a.ArtistId , a.Name 
                    from (select distinct(a.ArtistId)
                    from track t, genre g , artist a, album a2 
                    where t.genreId = %s and t.GenreId = g.GenreId and t.AlbumId = a2.AlbumId and a2.ArtistId = a.ArtistId ) t, artist a
                    where a.ArtistId = t.ArtistId"""
        cursor.execute(query, (genere,))

        result = []

        for row in cursor:
            result.append(Artista(**row))

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getEdges():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """select i2.CustomerId, a.ArtistId, t.GenreId, a.Name, (i.UnitPrice * i.Quantity) as costo
                    from invoiceline i, invoice i2, track t, artist a, album a2 
                    where i.InvoiceId = i2.InvoiceId and i.TrackId = t.TrackId and t.AlbumId = a2.AlbumId and a2.ArtistId = a.ArtistId"""
        cursor.execute(query)

        result = []

        for row in cursor:
            result.append(Compensi(**row))

        cursor.close()
        conn.close()

        return result


# select distinct(a.ArtistId)
# from track t, genre g , artist a, album a2
# where t.genreId = 1 and t.GenreId = g.GenreId and t.AlbumId = a2.AlbumId and a2.ArtistId = a.ArtistId
#
# select a.ArtistId , a.Name
# from (select distinct(a.ArtistId)
# from track t, genre g , artist a, album a2
# where t.genreId = 2 and t.GenreId = g.GenreId and t.AlbumId = a2.AlbumId and a2.ArtistId = a.ArtistId ) t, artist a
# where a.ArtistId = t.ArtistId
#
# select i2.CustomerId, a.ArtistId, a.Name, (i.UnitPrice * i.Quantity) as costo
# from invoiceline i, invoice i2, track t, artist a, album a2
# where i.InvoiceId = i2.InvoiceId and i.TrackId = t.TrackId and t.AlbumId = a2.AlbumId and a2.ArtistId = a.ArtistId
# group by i2.CustomerId, a.ArtistId, a.Name
#
# select a.ArtistId, a.Name, count(*)
# from invoiceline i, invoice i2, track t, artist a, album a2
# where i.InvoiceId = i2.InvoiceId and i.TrackId = t.TrackId and t.AlbumId = a2.AlbumId and a2.ArtistId = a.ArtistId
# group by a.ArtistId

