import codecs
import csv

from fastapi import File
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.core.exceptions import UserNotFound
from app.crud.crud_figures import CrudMultiLineFigure
from app.crud.crud_user import CrudUser
from app.schemas.figures import MultiLineFigureCreate


class CreateMultiLineFigure:
    def __init__(
            self, figure_data: dict, file: File, user_uuid: UUID, db: Session
    ) -> None:
        self.figure_data = figure_data
        self.file = file
        self.user_uuid = user_uuid
        self.db = db
        self.instance = None

    def perform(self) -> bool:
        self._validate_user_uuid()
        x_axis, datasets = self._create_data()
        figure = MultiLineFigureCreate(
            user_uuid=self.user_uuid,
            x_axis=x_axis,
            datasets=datasets,
            **self.figure_data
        )
        self.instance = CrudMultiLineFigure.create(db=self.db, obj_in=figure)

        return True

    def _validate_user_uuid(self):
        user = CrudUser.get_by_uuid(uuid=self.user_uuid, db=self.db)
        if not user:
            raise UserNotFound(message="User not found.")

    def _create_data(self):
        csv_reader = csv.reader(codecs.iterdecode(self.file, "utf-8"))
        headers = next(csv_reader)
        y_axis_list = [
            int(num) for num in self.figure_data["y_axis_columns"].split(",")
        ]
        x_axis_column = self.figure_data["x_axis_column"]
        x_axis = headers[x_axis_column::]
        # y_axis = [name for num in y_axis_list for name in headers[num - 1]]

        datasets = dict()

        for row in csv_reader:
            datasets[row[x_axis_column - 1]] = [row[num - 1] if row[num - 1] != '' else None for num in y_axis_list]
        return x_axis, datasets


class PrebuildMultiLineFigure:
    def __init__(
            self, figure_data: dict, file: File, user_uuid: UUID, db: Session
    ) -> None:
        self.figure_data = figure_data
        self.file = file
        self.user_uuid = user_uuid
        self.db = db
        self.instance = None

    def perform(self) -> bool:
        self._validate_user_uuid()
        x_axis, datasets = self._create_data()
        figure = MultiLineFigureCreate(
            user_uuid=self.user_uuid,
            x_axis=x_axis,
            datasets=datasets,
            **self.figure_data
        )
        self.instance = figure

        return True

    def _validate_user_uuid(self):
        user = CrudUser.get_by_uuid(uuid=self.user_uuid, db=self.db)
        if not user:
            raise UserNotFound(message="User not found.")

    def _create_data(self):
        csv_reader = csv.reader(codecs.iterdecode(self.file, "utf-8"))
        headers = next(csv_reader)
        y_axis_list = [
            int(num) for num in self.figure_data["y_axis_columns"].split(",")
        ]
        x_axis_column = self.figure_data["x_axis_column"]
        x_axis = headers[x_axis_column::]
        # y_axis = [name for num in y_axis_list for name in headers[num - 1]]

        datasets = dict()

        for row in csv_reader:
            datasets[row[x_axis_column - 1]] = [row[num - 1] for num in y_axis_list]
        return x_axis, datasets
