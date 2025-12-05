from pathlib import Path
import sys
from typing import Final, NamedTuple, Optional, Self, final, override


def part1(contents: str) -> int:
    top, bottom = contents.strip().split("\n\n")
    ranges: Final[list[range]] = []
    for line in top.split():
        parts = line.split("-")
        ranges.append(range(int(parts[0]), int(parts[1]) + 1))

    num_fresh_ingredients = 0
    for ingredient_id in bottom.split():
        if any(int(ingredient_id) in range_ for range_ in ranges):
            # print(ingredient_id)
            num_fresh_ingredients += 1

    return num_fresh_ingredients


@final
class Range(NamedTuple):
    start: int
    end: int  # inclusive
    
    @override
    def __contains__(self, other: object) -> bool:
        if not isinstance(other, int):
            return False
        return other in range(self.start, self.end + 1)
    
    @override
    def __len__(self) -> int:
        return self.end - self.start + 1
    
    def overlaps(self, other: Self) -> bool:
        return self.start in other or self.end in other or other.start in self or other.end in self
    
    def overlaps_or_adjacent(self, other: Self) -> bool:
        """Check if ranges overlap or are immediately adjacent."""
        return (self.start in other or self.end in other or 
                other.start in self or other.end in self or
                self.end + 1 == other.start or other.end + 1 == self.start)


@final
class RangeContainer:
    def __init__(self, *args: Range) -> None:
        self._ranges: Final[list[Range]] = list(args)
    
    @override
    def __str__(self) -> str:
        return ", ".join(
            f"[{r.start}, {r.end}]" for r in self._ranges
        )
        
    def __len__(self) -> int:
        return sum(len(r) for r in self._ranges)
    
    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RangeContainer):
            return False
        return self._ranges == other._ranges

    def merge(self, range_: Range) -> None:
        if not self._ranges:
            self._ranges.append(range_)
            return
        
        first: Optional[int] = None
        second: Optional[int] = None
        for i, r in enumerate(self._ranges):
            if first is None and r.end + 1 >= range_.start:
                first = i
                continue
            if first is not None and r.start <= range_.end + 1:
                second = i
        
        if first is not None and second is not None:
            # Merge across ranges.
            new_range: Final = Range(self._ranges[first].start, self._ranges[second].end)
            for i in reversed(range(first, second + 1)):
                self._ranges.pop(i)
            self._ranges.insert(first, new_range)

        did_overlap = False
        for i, r in enumerate(self._ranges):
            if r.overlaps_or_adjacent(range_):
                did_overlap = True
                self._ranges[i] = Range(
                    start=min(self._ranges[i].start, range_.start),
                    end=max(self._ranges[i].end, range_.end),
                )
                break
        
        if not did_overlap:
            for i, r in enumerate(self._ranges):
                if r.start > range_.start:
                    self._ranges.insert(i, range_)
                    return
            self._ranges.append(range_)


def part2(contents: str) -> int:
    top, _ = contents.strip().split("\n\n")
    ranges: Final[list[Range]] = []
    for line in top.split():
        parts = line.split("-")
        ranges.append(Range(start=int(parts[0]), end=int(parts[1])))
        
    container: Final = RangeContainer()
    for range_ in ranges:
        container.merge(range_)
    return len(container)


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file>", file=sys.stderr)
        sys.exit(1)
    path: Final = Path(sys.argv[1])
    contents: Final = path.read_text(encoding="utf-8")
    print(part2(contents))
    


if __name__ == "__main__":
    main()
