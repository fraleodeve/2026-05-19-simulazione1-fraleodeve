from dataclasses import dataclass

@dataclass
class Compensi:
    CustomerId: int
    ArtistId: int
    GenreId: int
    Name: str
    costo: float