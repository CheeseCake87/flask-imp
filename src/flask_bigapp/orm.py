import typing as t

from sqlalchemy import select, update, insert, delete, desc, asc  # type: ignore
from sqlalchemy.orm import Session  # type: ignore


class CrudMixin:
    __id_field__: str
    __session__: Session

    @classmethod
    def create(
            cls,
            values: t.Optional[t.Dict[str, t.Any]] = None,
            batch: t.Optional[t.List[t.Dict[str, t.Any]]] = None,
            wash_attributes: bool = False,
            ignore_attributes: t.Optional[t.List[str]] = None,
    ):
        if batch is not None:
            new_batch = []
            if wash_attributes:
                for item in batch:
                    temp_item = {**item}
                    for key, value in item.items():
                        if ignore_attributes:
                            if key in ignore_attributes:
                                del temp_item[key]
                                continue
                        if not hasattr(cls, key):
                            del temp_item[key]
                    new_batch.append(temp_item)

            process_batch = batch if not wash_attributes else new_batch
            result = cls.__session__.scalars(
                insert(cls).returning(cls),
                process_batch
            )
            cls.__session__.commit()
            return result.all()

        if values:
            temp_values = {**values}
        else:
            temp_values = {}

        if wash_attributes and values is not None:
            for key, value in values.items():
                if not hasattr(cls, key):
                    del temp_values[key]

        if ignore_attributes is not None and values is not None:
            for key in ignore_attributes:
                if key in values:
                    del temp_values[key]

        result = cls.__session__.scalar(
            insert(cls).returning(cls).values(**temp_values)  # type: ignore
        )
        cls.__session__.commit()
        return result

    @classmethod
    def read(
            cls,
            id_: t.Optional[int] = None,
            field: t.Optional[tuple] = None,
            fields: t.Optional[t.Dict[str, t.Any]] = None,
            all_rows: bool = False,
            order_by: t.Optional[str] = None,
            order_desc: bool = False,
            _updating: bool = False,
            _deleting: bool = False,
            _auto_output: bool = True
    ):
        if _updating:
            base_query = update(cls)  # type: ignore
        elif _deleting:
            base_query = delete(cls)  # type: ignore
        else:
            if order_by is not None:
                column = getattr(cls, order_by)
                if order_desc:
                    base_query = select(cls).order_by(desc(column))  # type: ignore
                else:
                    base_query = select(cls).order_by(asc(column))  # type: ignore
            else:
                base_query = select(cls)  # type: ignore

        if all_rows:
            return cls.__session__.scalars(base_query).all()

        if id_ is not None:
            kwargs = {cls.__id_field__: id_}
            base_query = base_query.filter_by(**kwargs)
            if _updating or _deleting:
                return base_query
            if _auto_output:
                return cls.__session__.scalars(base_query).one_or_none()
            return cls.__session__.scalars(base_query)

        if field is not None:
            base_query = base_query.filter_by(**{field[0]: field[1]})
            if _updating or _deleting:
                return base_query
            if _auto_output:
                return cls.__session__.scalars(base_query).all()
            return cls.__session__.scalars(base_query)

        if fields is not None:
            base_query = base_query.filter_by(**fields)
            if _updating or _deleting:
                return base_query
            if _auto_output:
                return cls.__session__.scalars(base_query).all()
            return cls.__session__.scalars(base_query)

    @classmethod
    def update(
            cls,
            values: dict,
            id_: t.Optional[int] = None,
            field: t.Optional[tuple] = None,
            fields: t.Optional[t.Dict[str, t.Any]] = None,
            return_updated: bool = False,
            wash_attributes: bool = False,
            ignore_attributes: t.Optional[t.List[str]] = None,
    ):
        if values:
            temp_values = {**values}
        else:
            temp_values = {}

        if wash_attributes:
            for key, value in values.items():
                if not hasattr(cls, key):
                    del temp_values[key]

        if ignore_attributes is not None and values is not None:
            for key in ignore_attributes:
                if key in values:
                    del temp_values[key]

        query = cls.read(id_=id_, field=field, fields=fields, _updating=True).values(temp_values)
        if return_updated:
            result = cls.__session__.execute(query.returning(cls)).scalars().all()
            cls.__session__.commit()
            return result
        cls.__session__.execute(query)
        cls.__session__.commit()
        return True

    @classmethod
    def delete(
            cls,
            id_: t.Optional[int] = None,
            field: t.Optional[tuple] = None,
            fields: t.Optional[t.Dict[str, t.Any]] = None,
            return_deleted: bool = False
    ):
        query = cls.read(id_=id_, field=field, fields=fields, _deleting=True)
        if return_deleted:
            result = cls.__session__.execute(query.returning(cls)).scalars().all()
            cls.__session__.commit()
            return result[0] if len(result) > 0 else result
        cls.__session__.execute(query)
        cls.__session__.commit()
        return True
