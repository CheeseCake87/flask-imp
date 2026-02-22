import typing as t

from flask import Response


class ValidCheckpoint(t.Protocol):
    def action(
        self,
        fail_url: t.Optional[t.Union[str, t.Callable[[], t.Any]]] = None,
        fail_json: t.Optional[t.Dict[str, t.Any]] = None,
        fail_response: t.Optional[t.Callable[[], Response]] = None,
        fail_status: int = 403,
        pass_url: t.Optional[t.Union[str, t.Callable[[], t.Any]]] = None,
        message: t.Optional[str] = None,
        message_category: str = "message",
        disable_default_fail: bool = False,
    ) -> t.Any: ...

    def pass_(self) -> bool: ...
