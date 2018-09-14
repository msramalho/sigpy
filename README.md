# sigpy
Python Lib and interface to interact with sigarra web platform

> Grows inconsistent as sigarra evolves, so... pretty consistent 😏

JSON example with explanation
```python
{
            "url": "student",
            "picture": "picture",  # route name for getting pictures
            "attributes": {
                "name": {"css": "div.estudante-info-nome"},  # if not class in attribute
                "id": {"css": "div.estudante-info-numero a"},
                "email": {"derivate": "up%s@fe.up.pt", "from": ["id"]},  # derivate from tuple #TODO: some students hay have different emails
                "courses": {
                    "model": "course",  # model works as class
                    "list": True,  # omission means single
                    "css": "div.estudante-lista-curso-activo",
                    "attributes": {
                        "name": {"css": "div.estudante-lista-curso-nome"},
                        "institution": {"css": "div.estudante-lista-curso-instit"},
                        "id": {"regex": ".*pv_curso_id=(\d+).*"},  # if there is an anchor
                        "enrolled": {"xpath": ".//td[text()='Ano da primeira inscrição:']/following::td[1]"},
                        "year": {"xpath": ".//td[text()='Ano curricular atual:']/following::td[1]"},
                        "state": {"xpath": ".//td[text()='Estado atual:']/following::td[1]"}
                    }
                },
                "inactive_courses": {
                    "model": "course",
                    "list": True,  # omission means single
                    "css": "div.tabela-longa",
                    "attributes": {
                        "name": {"css": "td.t.k"},
                        "id": {"regex": ".*pv_curso_id=(\d+).*"},  # if there is an anchor
                        "institution": {"xpath": ".//tr[@class='i']/td[2]/a/@title"},
                        "old_id": {"css": "td.l"},
                        "type": {"css": "td.t", "index": 2},
                        "started": {"css": "td.l", "index": 1}
                    }
                }
            }
        }
```