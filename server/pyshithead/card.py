from dataclasses import dataclass
from enum import IntEnum
from typing import Optional

from pyshithead import ALL_RANKS, BIGGEST_RANK


class Suit(IntEnum):
    TILES = 1
    HEART = 2
    CLOVERS = 3
    PIKES = 4


class Choice(IntEnum):
    HIGHER = 3
    LOWER = 4


class SpecialRank(IntEnum):
    RESET = 2
    INVISIBLE = 5
    HIGHLOW = 7
    SKIP = 8
    BURN = 10


class BurnEvent(IntEnum):
    NO = 1
    YES = 2


class RankType(IntEnum):
    """
    TOPRANK: standard; all cards "">="" are valid incl. 2,5,10
    KEEPCURRENT: invisible
    HIGHER=Choice.HIGHER: all cards ">=" are valid (excl. 2,5)
    LOWER=Choice.LOWER: all cards <= are valid (excl 10)
    """

    TOPRANK = 1
    KEEPCURRENT = 2
    HIGHER = Choice.HIGHER
    LOWER = Choice.LOWER


@dataclass
class RankEvent:
    rank_type: RankType
    top_rank: int

    def get_valid_ranks(self, current_valid_ranks: Optional[set[int]] = None) -> set[int]:
        valid_ranks: set[int] = set()
        if self.rank_type == RankType.TOPRANK:
            valid_ranks.update(
                [int(SpecialRank.RESET), int(SpecialRank.INVISIBLE), int(SpecialRank.BURN)]
            )
            valid_ranks.update([i for i in range(self.top_rank, BIGGEST_RANK + 1)])
        elif self.rank_type == RankType.HIGHER:
            valid_ranks.update([i for i in range(int(SpecialRank.HIGHLOW), BIGGEST_RANK + 1)])
        elif self.rank_type == RankType.LOWER:
            valid_ranks.update(
                [
                    i
                    for i in range(
                        2,
                        int(SpecialRank.HIGHLOW) + 1,
                    )
                ]
            )
        elif self.rank_type == RankType.KEEPCURRENT:
            if current_valid_ranks is None:
                valid_ranks.update(ALL_RANKS)
            else:
                valid_ranks.update(current_valid_ranks)
        return valid_ranks


@dataclass(frozen=True)
class Card:
    rank: int
    suit: Suit

    def __hash__(self):
        return hash(str(self.rank) + str(self.suit))

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit
