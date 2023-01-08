from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from Models import Pair
from tabulate import multiline_formats, tabulate

from ...Decorations import Colorize, Colors

multiline_formats["rounded_outline"] = "rounded_outline"
multiline_formats["simple_outline"] = "simple_outline"
multiline_formats["rounded_grid"] = "rounded_grid"


@dataclass
class Schema:
    sort_index: int
    name: str
    display_name: str

    def __init__(self, sort_index: int, name: str, display_name: str = "") -> None:
        self.sort_index = sort_index
        self.name = name
        self.display_name = display_name if display_name else name

    def set_display_name(self, name: str):
        self.display_name = name

    def __lt__(self, name: str):
        self.set_display_name(name)
        return self


@dataclass
class Table:
    Header: str
    Divider: str
    Footer: str
    dimension: Pair
    cursor: list[int]
    rows: list[Row]
    schema: list[Schema]
    columns: Optional[list[Schema]]

    def __init__(self, data: list, columns: list = []) -> None:

        if columns == []:
            ordered_data = data
        else:
            ordered_data = [
                {key.display_name: data[i][key.name] for key in columns}
                for i in range(len(data))
            ]

        self.schema, data_list = retrofiy_list(ordered_data)
        self.dimension = Pair(len(data_list) - 1, len(data_list[0]))

        table = tabulate(
            data_list,
            headers=self.schema,
            maxcolwidths=40,
            showindex="always",
            tablefmt="rounded_grid",
        )

        # print(table)
        self.Header, self.Divider, self.Footer = get_trims(table)
        self.rows = [
            Row(r)
            for r in table.split(self.Header)[1]
            .split(self.Footer)[0]
            .split(self.Divider)
        ]

    def __str__(self) -> str:

        print("dimension", self.dimension)

        output = []

        for column in self.schema:
            print(column)

        for idx, r in enumerate(self.rows):
            if idx == 0:
                output.append(self.Header)
                output.append(str(r))
                # output.append(self.Divider)

                output.append(self.Footer)
                output.append(self.Header)

            elif idx in range(2, len(self.rows)):
                output.append(self.Divider)
                output.append(str(r))
            else:
                output.append(str(r))

        output.append(self.Footer)

        return "\n".join(output)

    def select(self, x: int, y: int):

        x += 1
        y += 1

        if x >= len(self.rows):
            print(x, len(self.rows))
            return

        if y > len(self.schema) + 1:
            y = len(self.schema) + 1
            print(y, len(self.schema))
            return

        for row in self.rows[x].cells:
            row[y] = Colorize(
                str(row[y]), background=Colors.BG.LIGHT_GRAY, style=Colors.MD.BLINK
            )


@dataclass
class Row:
    cells: list[list[str]]
    subtable: Table | None
    row_span: int = -1

    def __init__(self, row: str) -> None:
        lrows: list[str] = row.split("\n")
        # print(lrows)
        self.cells = []
        for r in lrows:
            if r:
                self.cells.append(r.split("│"))

        row_span = len(lrows)
        self.subtable = None

        # print(self.cells)

    def __str__(self) -> str:
        return "\n".join(["│".join(r) for r in self.cells])


def retrofiy_list(data: list):
    if data:
        return [key for key in data[0].keys()], [item.values() for item in data]
    else:
        return [], []


def get_trims(table: str):

    new_table = []
    rows = table.split("\n")

    header = rows[0:3]

    header_top_trim = rows[0]
    header_bottom_trim = rows[2]
    footer_trim = rows[-1]

    return header_top_trim, header_bottom_trim, footer_trim


def render(table, x: int, y: int):
    table.select(x, y)
    return str(table)
